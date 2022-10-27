import math
from collections import Counter

file_name = '../test3.txt'

with open(file_name, 'rb') as file:
    file_bytes = file.read()

    pairs = []
    for index in range(len(file_bytes) - 2):
        pairs.append([file_bytes[index], file_bytes[index + 1]])
    print(pairs)

    dic = {}
    for word in set(file_bytes):
        inner_dic = {}
        for pair in pairs:
            if pair[0] == word:
                num = pairs.count(pair)
                inner_dic[pair[1]] = num
        dic[word] = inner_dic

    ##################### Длина файла в первичном алфавите ###############################
    print(f'Длинай файла в байтах: {len(file_bytes)}')

    counter = Counter(file_bytes)

    ##################### Вхождение подстрок ###############################
    print('Вхождение подстрок')
    for key in dic.keys():
        print(f'{key} => {dic[key]}')

    ##################### Вхождение подстрок начинающихся с Аi ###############################
    print('Вхождение подстрок начинающихся с символа')
    for key in dic.keys():
        print(f'{key} => {sum(dic[key].values())}')

    print('Безусловная вероятность')
    for key in counter.keys():
        print(f'P({key}) = {counter[key]/256}')


    print('Условная вероятность')
    for byte1 in set(file_bytes):
        for byte2 in set(file_bytes):
            if pairs.count([byte1, byte2]) != 0:
                print(f'P({byte1}|{byte2}) = {(pairs.count([byte1, byte2]))/(counter[byte2])}')


    print("Кол-во информации")
    N = 256
    i = math.log2(N)
    K = len(file_bytes)
    print(f'Кол-во информации = {K*i}')