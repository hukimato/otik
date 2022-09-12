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

        file_size = int.from_bytes(archived_files_data[0:4], 'little')
        next_file_offset = int.from_bytes(archived_files_data[4:12], 'little')
        file_data_offset = int.from_bytes(archived_files_data[12:20], 'little')
        print(file_size, file_data_offset, next_file_offset)
        # while len(archived_files_data) > 0:
        #     file_size = int.from_bytes(archived_files_data[0:4], 'big')
        #     next_file_offset = int.from_bytes(archived_files_data[4:12], 'big')
        #     file_data_offset = int.from_bytes(archived_files_data[12:20], 'big')
        #     print(file_size, file_data_offset, next_file_offset)
        #     archived_files_data = archived_files_data[next_file_offset::]





