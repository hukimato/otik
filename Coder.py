from Huffman import Huffman_Decoding, Huffman_Encoding

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
        result_byte_code = self.fill_meta_data(0)
        result_compressed_byte_code = self.fill_meta_data()

        for file in self.files:
            with open(file, 'rb') as f:
                file_data = f.read()

                file_byte_code = bytearray()
                file_byte_code.extend(len(file_data).to_bytes(8, 'big'))  # Размер файла
                file_byte_code.extend(int(0).to_bytes(8, 'big'))  # Размер данных для декода
                file_byte_code.extend(int(0).to_bytes(1, 'big'))  # Размер данных для декода
                file_byte_code.extend(int(0).to_bytes(1, 'big'))  # Размер данных для декода
                file_byte_code.extend((len(file.encode('utf-8')) + 1).to_bytes(2, 'big'))

                file_byte_code.extend(bytes(file, 'utf-8'))  # Имя файла
                file_byte_code.extend(bytes('|', 'utf-8'))  # Разделитель (| запрещена в названиях файлов)
                file_byte_code.extend(file_data)  # Данные файла

                result_byte_code.extend(file_byte_code)
        
        if (self.algo_compression_without_context != 0):
            for file in self.files:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    
                    compressed_file_data, data_offset, codes, codes_offset = self.compression(file_data)

                    file_byte_code = bytearray()
                    file_byte_code.extend(len(compressed_file_data).to_bytes(8, 'big'))  # Размер файла
                    file_byte_code.extend(len(codes).to_bytes(8, 'big'))  # Размер данных для декода
                    file_byte_code.extend(data_offset.to_bytes(1, 'big'))  # Размер данных для декода
                    file_byte_code.extend(codes_offset.to_bytes(1, 'big'))  # Размер данных для декода
                    file_byte_code.extend((len(file.encode('utf-8')) + 1).to_bytes(2, 'big'))

                    file_byte_code.extend(bytes(file, 'utf-8'))  # Имя файла
                    file_byte_code.extend(bytes('|', 'utf-8'))  # Разделитель (| запрещена в названиях файлов)
                    file_byte_code.extend(compressed_file_data)  # Данные файла
                    file_byte_code.extend(codes)  # Данные для декода из сжатого файла

                    result_compressed_byte_code.extend(file_byte_code)

            print('Compressed: ', len(result_compressed_byte_code))
            print('Uncompressed: ', len(result_byte_code))
            if (len(result_compressed_byte_code) < len(result_byte_code)):
                result_byte_code = result_compressed_byte_code

        my_file = open('archive.myfile', 'wb')
        my_file.write(result_byte_code)
        # print(result_byte_code)
        my_file.close()

    def compression(self, file_data):
        [data, codes] = Huffman_Encoding(file_data)
        
        data.reverse()
        data_offset_bits = data.fill()
        data.reverse()

        codes.reverse()
        codes_offset_bits = codes.fill()
        codes.reverse()


        return data.tobytes(), data_offset_bits, codes.tobytes(), codes_offset_bits

    def fill_meta_data(self, algo_compression_manual=None):
        my_file_byte_code = self.signature[:]  # Сигнатура
        my_file_byte_code.extend(self.version.to_bytes(2, 'big'))  # Версия
        my_file_byte_code.extend(int(0).to_bytes(2, 'big'))  # Резерв
        my_file_byte_code.extend(self.algo_compression_without_context.to_bytes(1, 'big'))  # код алгоритма
        my_file_byte_code.extend(self.algo_compression_with_context.to_bytes(1, 'big'))  # код алгоритма
        my_file_byte_code.extend(self.algo_loss_protection.to_bytes(1, 'big'))  # код алгоритма
        my_file_byte_code.extend(self.encryption.to_bytes(1, 'big'))  # код алгоритма
        # Записано 11 байт
        return my_file_byte_code
