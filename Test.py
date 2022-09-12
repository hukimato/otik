import filecmp

f1 = "test3.txt"
f2 = "output/test3.txt"

# shallow comparison
result = filecmp.cmp(f1, f2)
print('Сравнение мета данных файлов:' + result)
# deep comparison
result = filecmp.cmp(f1, f2, shallow=False)
print('Сравнение содержимого файлов:' + result)
