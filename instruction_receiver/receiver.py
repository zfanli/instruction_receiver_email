import imaplib
import yaml
import email


class Receiver:
    """Mail receiver and parser."""

    def __init__(self, config):
        """Initialize receiver."""

        try:
            with open(config, "r") as f:
                self.config = yaml.load(f, Loader=yaml.BaseLoader)
                # Get configs
                email_config = self.config["email_config"]
                server = email_config["imap_server"]
                port = email_config["imap_port"]
                username = email_config["username"]
                password = email_config["password"]
                # Setup email client
                self.server = imaplib.IMAP4_SSL(server, port)
                self.server.login(username, password)
        except Exception as e:
            print(f"Initialization with config {config} failed.")
            print(e)

    @staticmethod
    def charset(lines):
        """Get charset from response.
        
        It seems Message.get_charset() does not work expectedly,
        so just get it from raw data directly."""

        encode = "utf-8"
        for line in lines:
            if b"charset" in line:
                encode = line.decode("utf-8").split('"')[-2]
        return encode

    @staticmethod
    def decode(header):
        """Decode header string use built-in function."""

        h = email.header.decode_header(header)
        result = []
        for item in h:
            val, encode = item
            if encode is None:
                if type(val) != str:
                    val = val.decode("utf-8")
                result.append(val)
            else:
                result.append(val.decode(encode))
        return "".join(result)

    @staticmethod
    def get_payload(msg, charset):
        """Get payload from Message object."""

        result = []
        for part in msg.walk():
            # multipart/* are just containers
            if part.get_content_maintype() == "multipart":
                continue
            elif part.get_content_maintype() == "application":
                # Ignore attachments
                if part.get_content_subtype() == "octet-stream":
                    continue
            result.append(part.get_payload(decode=True).decode(charset))
        return result

    def read(self):
        """Entrypoint."""

        # Use inbox
        self.server.select("INBOX")
        # Fetch unread mails only
        status, messages = self.server.search(None, "INBOX", "(UNSEEN)")
        # Get message ids
        messages = messages[0].split()
        print("Unread mails:", len(messages))
        # Read mails from oldest to newest
        for id in messages:
            # fetch the email message by id
            _typ, msg = self.server.fetch(id, "(RFC822)")
            # Get message response
            msg = msg[0][1]
            # Get charset
            charset = self.charset(msg.split(b"\r\n"))
            # Parse mail
            msg = email.message_from_string(msg.decode(charset))
            # Check if should process
            if self.filter(msg):
                # Process
                self.parse(msg, charset)
                # Mark this mail as read
                # self.seen(i)
        self.close()

    def filter(self, msg):
        """Filter out message by config."""

        allow_list = self.config["allow_list"]
        sender = self.decode(msg["From"])
        for e in allow_list:
            if e in sender:
                return True
        return False

    def parse(self, msg, charset):
        """Main processing."""

        print(self.decode(msg["From"]), self.decode(msg["Subject"]))
        # Shortest one is the one should to be parsed
        payload = self.get_payload(msg, charset)
        body = None
        for item in payload:
            if body is None or len(body) > len(item):
                body = item
        print(body)

    def seen(self, id):
        """Mark mail as read."""

        self.server.store(id, "+FLAGS", "\Seen")

    def close(self):
        """Clean up."""

        self.server.close()
        self.server.logout()


if __name__ == "__main__":
    # Test
    receiver = Receiver("config.yml")
    receiver.read()
