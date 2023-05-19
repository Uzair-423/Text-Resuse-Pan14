import sys

f1 = './dataset/src/source-document00860.txt'
f2 = './dataset/susp/suspicious-document00006.txt'

f = open(f1,'r')
raw = f.read()
string = ""
print("\n")
for index,char in enumerate(raw):
    if index >=int(sys.argv[1]) and index<int(sys.argv[1])+int(sys.argv[2]):
        string+=char
f.close()
print(string)
print("\n")
f = open(f2,'r')
raw = f.read()
string = ""
for index,char in enumerate(raw):
    if index >=int(sys.argv[3]) and index<int(sys.argv[3])+int(sys.argv[4]):
        string+=char
f.close()
print(string)