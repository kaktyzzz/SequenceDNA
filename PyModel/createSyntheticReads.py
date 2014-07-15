from random import randint

DNALength = 50
ReadsLength = 5
m = DNALength * 3

nucl = ['A', 'C', 'G', 'T']

s = ''
for i in range(0, DNALength):
    s += nucl[randint(0,3)]

f = open('syntheticDNA.txt', 'w')
f.write(s + '\n')
f.close()

f = open('reads.txt', 'w')
for i in range(0, m):
    #l = randint(-2, 2) + ReadsLength
    l = ReadsLength
    p = randint(0, DNALength - l)
    f.write(s[p:l+p] + '\n')
    #print(str(p) + ' ' + s[p:l+p])

f.close()