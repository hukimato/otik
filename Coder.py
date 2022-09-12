class Coder:
    signature = bytearray('Ъь', 'utf-8')

    def __init__(self, version, algo_compression_with_context, algo_compression_without_context, algo_loss_protection, encryption):
        self.version = int(version)
        self.algo_compression_with_context = int(algo_compression_with_context)
        self.algo_compression_without_context = int(algo_compression_without_context)
        self.algo_loss_protection = int(algo_loss_protection)
        self.encryption = int(encryption)
        self.files = []

    def code(self, file_names):
        self.files = file_names

        result_byte_code = self.fill_meta_data()

        for file in self.files:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_data = self.compression(file_data)
                file_length = len(file_data)

                file_byte_code = bytearray()

                file_byte_code.extend(file_length.to_bytes(4, 'big'))
                file_byte_code.extend((file_length + 32 + file_length % 8 + 8).to_bytes(8, 'big'))
                file_byte_code.extend(int(8).to_bytes(8, 'big'))
                print(file_byte_code)

                file_byte_code.extend(bytes(file, 'utf-8'))
                file_byte_code.extend(bytes('|', 'utf-8'))
                file_byte_code.extend(file_data)

                while len(file_byte_code) < file_length + 20 + file_length % 8 + 8:
                    file_byte_code.append(0)

                result_byte_code.extend(file_byte_code)

        my_file = open('archive.myfile', 'wb')
        my_file.write(result_byte_code)
        my_file.close()


    def compression(self, file_data):
        return file_data

    def fill_meta_data(self):
        my_file_byte_code = self.signature  # 4 bytes

        my_file_byte_code.extend(self.version.to_bytes(2, 'big'))

        my_file_byte_code.extend(int(0).to_bytes(2, 'big'))

        my_file_byte_code.extend(self.algo_compression_without_context.to_bytes(1, 'big'))
        my_file_byte_code.extend(self.algo_compression_with_context.to_bytes(1, 'big'))
        my_file_byte_code.extend(self.algo_loss_protection.to_bytes(1, 'big'))
        my_file_byte_code.extend(self.encryption.to_bytes(1, 'big'))  # 12 bytes

        return my_file_byte_code