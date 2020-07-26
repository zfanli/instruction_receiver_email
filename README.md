# instruction receiver email

Scripts for read emails and extract instructions.

## Read mails

Read mails from remote server using IMAP protocol.

### Configuration

Copy `config_tmp.yml` as `config.yml` and fill up the contents follow the keys.

#### `email_config`

- `protocol`

Only `IMAP` for now.

- `imap_server`

The hostname of your email server. For read mails.

- `imap_port`

The port number of your email server. For read mails.

- `smtp_server`

The hostname of your email server. For send mails.

- `smtp_port`: 789

The port number of your email server. For send mails.

- `username`

The email username.

- `password`

The password.

#### `allow_list`

The list of all the email addresses which is allowed to send the instructions.

Mails from the senders not listed in `allow_list` will be ignored.
