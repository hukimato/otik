class Decoder:
    signature = bytearray('Ъь', 'utf-8')
    version = 0
    algo_compression_with_context = None
    algo_compression_without_context = None
    algo_loss_protection = None
    encryption = None

    def get_meta_data(self, file_meta_data):
        self.signature = file_meta_data[0:4]
        self.version = file_meta_data[4:6]
        self.algo_compression_without_context = file_meta_data[8]
        self.algo_compression_with_context = file_meta_data[9]
        self.algo_loss_protection = file_meta_data[10]
        self.encryption = file_meta_data[11]

    def decode(self, file_name):
        file = open(file_name, 'rb')
        file_bytes = file.read()
        archived_files_data = file_bytes[12::]

        self.get_meta_data(file_bytes[0:12])

        while archived_files_data:
            file_size = int.from_bytes(archived_files_data[0:4], 'big')
            next_file_offset = int.from_bytes(archived_files_data[4:12], 'big')
            file_data_offset = int.from_bytes(archived_files_data[12:20], 'big')

            file_bytes = archived_files_data[20:file_size+20]
            file_string = file_bytes.decode('utf-8')
            file_string = file_string.split('|', 1)
            with open('output/'+file_string[0], 'w') as f:
                f.write(file_string[1])

            archived_files_data = archived_files_data[next_file_offset-1:]





