from Coder import Coder
from Decoder import Decoder
import sys

'''
Формат файла
0   Сигнатура: b'\xd0\xaa\xd1\x8c' или Ъь в utf-8
4   Версия                              2 байта 
6   Резерв                              2 байта 
8   Алгоритм сжатия без контекста       1 байт
9   Алгорит сжатия с учетом контекста   1 байт
10  Алгоритм защиты от помех            1 байт
11  Алгоритм шифрования                 1 байт
12  Размер данных файла                 8 байт 
20  Размер информации для разжатия      8 байт
28  Смещение в битах на начало данных   1 байт
29  Смещение в битах на начало декомпр  1 байт
30  
Данные <исходное_имя_файла|данные файла и данные для декомпресса>
'''


def main():
    if sys.argv[1] == 'code':
        coder = Coder(0, 1, 1, 0, 0)
        coder.code(sys.argv[2::])
    if sys.argv[1] == 'decode':
        decoder = Decoder()
        decoder.decode(sys.argv[2])


main()

# decoder = Decoder()
# decoder.decode('archive.myfile')
