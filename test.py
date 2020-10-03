f = open('vocab.txt', 'r', encoding="utf8")
data_1 = [x for x in f.readlines() if len(x.split()) >= 2]
f.close()

f = open('words.txt', 'r', encoding="utf8")
data_2 = [x for x in f.readlines() if len(x.split()) >= 2]
f.close()

data = data_1 + data_2

f = open('baru.txt', 'w', encoding="utf8")
for kata in data:
    f.write(kata)
f.close()
