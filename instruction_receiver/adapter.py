class Adapter:
    count = 0

    def send_instruction(self, instruction):
        # Send instruction
        self.count += 1
        return ("ok", {"code": "normal"}) if self.count % 2 == 0 else ("ng", {})
