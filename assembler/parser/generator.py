class Generator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.labels = {}
        self.instruction_counter = 0

    def __enter__(self):
        self.f = open(self.file_path, "wb")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        #reloop over file and replace necessary labels
        self.f.close()

    def write_instruction(self, instruction_token):
        # if labeled, at to label table
        # switch on operation type
            # write appropriate bytes
        # increase instruction_counter
        print("GENERATOR SAYS: not implemented")
