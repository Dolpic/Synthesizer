
class MidiHandler:

    @staticmethod
    def handle(input):

        if input.poll():
            status, note, velocity = input_device.read(1)[0][0]

            if DEBUG :
                print(f"status:{status}, note:{note}, velocity:{velocity}") 
                
        """
        # Tools
        if status == 176:
            if note == 114:
                self.stop()
            elif note >=22 and note <= 29:
                ...

        # Notes
        if note >= 0 and note <= 127:
            # Down
            if status == 144:
                ...
                
            # Up
            elif status == 128:
                ...
        """