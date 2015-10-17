import codecs


enc = "cp949"
f = open("../input/tsv/paystub_201508.txt", "r")

clazz = codecs.getreader(enc)
reader = clazz(f)


out = open("../output/a.txt", "w")
clazz = codecs.getwriter("utf-8")
writer = clazz(out)

for line in reader :
    #line = reader.readline()
    print line
    writer.write(line)

reader.close()
writer.close()