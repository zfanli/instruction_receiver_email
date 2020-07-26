from instruction_receiver.receiver import Receiver

if __name__ == "__main__":
    # Test
    receiver = Receiver("config.yml")
    receiver.read()
