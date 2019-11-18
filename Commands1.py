from trees import *
from vl_codes import shannon_fano
from random import random

p = [random() for k in range(10)]

p = dict([(chr(k+ord('a')),p[k]/sum(p)) for k in range(len(p))])
print(p)
print(f'Probability distribution: {p}\n')
c = shannon_fano(p)
print(f'Codebook: {c}\n')
xt = code2xtree(c)
print(f'Cut and paste for phylo.io: {xtree2newick(xt)}')



f = open('hamlet.txt', 'r')
hamlet = f.read()
f.close()
#print(hamlet[:294]) 

from itertools import groupby
frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies])
p = dict([(a,frequencies[a]/Nin) for a in frequencies])
print(f'File length: {Nin}')

c = shannon_fano(p)

print(xtree2newick(code2xtree(c)))

from vl_codes import vl_encode
hamlet_sf = vl_encode(hamlet,c);
print(f'Length of binary sequence: {len(hamlet_sf)}')

from vl_codes import bytes2bits, bits2bytes
hamlet_zipped = bits2bytes(hamlet_sf)
Nout = len(hamlet_zipped)
print(f'Length of compressed string: {Nout}')

from math import log2
H = lambda pr: -sum([pr[a]*log2(pr[a]) for a in pr])
print(f'Entropy: {H(p)}')

from vl_codes import vl_decode
xt = code2xtree(c)
hamlet_unzipped = vl_decode(hamlet_sf,xt)
print(f'Length of the unzipped file: {len(hamlet_unzipped)}')

print(''.join(hamlet_unzipped[:294]))




from camzip import camzip
camzip('shannon_fano', 'hamlet.txt')

from camunzip import camunzip
camunzip('hamlet.txt.czs')


from filecmp import cmp
from os import stat
from json import load
filename = 'hamlet.txt'
Nin = stat(filename).st_size
print(f'Length of original file: {Nin} bytes')
Nout = stat(filename + '.cz' + 's').st_size
print(f'Length of compressed file: {Nout} bytes')
print(f'Compression rate: {8.0*Nout/Nin} bits/byte')
with open(filename + '.czp', 'r') as fp:
	freq = load(fp)
pf = dict([(a, freq[a]/Nin) for a in freq])
print(f'Entropy: {H(pf)} bits per symbol')
if cmp(filename,filename+'.cuz'):
	print('The two files are the same')
else:
	print('The files are different')


from vl_codes import huffman
xt = huffman(p)
print(xtree2newick(xt))


from camzip import camzip
camzip('huffman', 'hamlet.txt')

from camunzip import camunzip
camunzip('hamlet.txt.czh')


from filecmp import cmp
from os import stat
from json import load
filename = 'hamlet.txt'
Nin = stat(filename).st_size
print(f'Length of original file: {Nin} bytes')
Nout = stat(filename + '.cz' + 'h').st_size
print(f'Length of compressed file: {Nout} bytes')
print(f'Compression rate: {8.0*Nout/Nin} bits/byte')
with open(filename + '.czp', 'r') as fp:
	freq = load(fp)
pf = dict([(a, freq[a]/Nin) for a in freq])
print(f'Entropy: {H(pf)} bits per symbol')
if cmp(filename,filename+'.cuz'):
	print('The two files are the same')
else:
	print('The files are different')


c = xtree2code(xt)
hamlet_huf = vl_encode(hamlet, c)
hamlet_decoded = vl_decode(hamlet_huf, xt)
print(''.join(hamlet_decoded[:294]))

hamlet_corrupted = hamlet_huf.copy()
hamlet_corrupted[400] ^= 1
hamlet_decoded = vl_decode(hamlet_corrupted, xt)
print(''.join(hamlet_decoded[:297]))



from itertools import groupby
frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies])
p = dict([(a,frequencies[a]/Nin) for a in frequencies])
print(f'File length: {Nin}')

f = [0.0]
for a in p:
	f.append(f[-1]+p[a])
f.pop()
f = dict([(a,f[k]) for a,k in zip(p,range(len(p)))])

lo, hi = 0.0, 1.0
n = 4
for k in range(n):
	a = hamlet[k]
	lohi_range = hi - lo
	hi = lo + lohi_range * (f[a] + p[a])
	lo = lo + lohi_range * f[a]
print(f'lo = {lo}, hi = {hi}, hi-lo = {hi-lo}')

from math import floor, ceil
ell = ceil(-log2(hi-lo))+2 if hi-lo > 0.0 else 96
print(bin(floor(lo*2**ell)))

from camzip import camzip
camzip('arithmetic', 'hamlet.txt')

from camunzip import camunzip
camunzip('hamlet.txt.cza')


from filecmp import cmp
from os import stat
from json import load
filename = 'hamlet.txt'
Nin = stat(filename).st_size
print(f'Length of original file: {Nin} bytes')
Nout = stat(filename + '.cz' + 'a').st_size
print(f'Length of compressed file: {Nout} bytes')
print(f'Compression rate: {8.0*Nout/Nin} bits/byte')
with open(filename + '.czp', 'r') as fp:
	freq = load(fp)
pf = dict([(a, freq[a]/Nin) for a in freq])
print(f'Entropy: {H(pf)} bits per symbol')
if cmp(filename,filename+'.cuz'):
	print('The two files are the same')
else:
	print('The files are different')


import arithmetic as arith
arith_encoded = arith.encode(hamlet, p)
arith_decoded = arith.decode(arith_encoded, p, Nin)
print('\n'+''.join(arith_decoded[:400]))