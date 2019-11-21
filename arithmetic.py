from math import floor, ceil
from sys import stdout as so
from bisect import bisect

def encode(x, p):

    precision = 32
    one = int(2**precision - 1)
    quarter = int(ceil(one/4))
    half = 2*quarter
    threequarters = 3*quarter


    p = dict([(a,p[a]) for a in p if p[a]>0])

    f = [0]
    for a in p: # for every probability in p
        f.append(p[a] + f[-1])
    f.pop()

    f = dict([(a,mf) for a,mf in zip(p,f)])
    
    y = [] # initialise output list
    lo,hi = 0,one # initialise lo and hi to be [0,1.0)
    straddle = 0 # initialise the straddle counter to 0

    
    for k in range(len(x)): # for every symbol
        if k % 100 == 0:
            so.write('Arithmetic encoded %d%%    \r' % int(floor(k/len(x)*100)))
            so.flush()
        lohi_range = (hi - lo) +1
        lo = int(ceil(lo + (f[x[k]]*lohi_range)))
        hi = int(floor(lo + (p[x[k]]*lohi_range)))
        if (lo == hi):
            raise NameError('Zero interval!')

        while True:
            if hi < half: # if lo < hi < 1/2
 
                y.append(0)
                for i in range(straddle):
                    y.append(1)
                straddle =0
            elif lo >= half: # if hi > lo >= 1/2
                y.append(1)
                # ...  extend 'straddle' zeros
                for i in range(straddle):
                    y.append(0)
                straddle = 0

                lo = lo - half
                hi = hi-half
            elif lo >= quarter and hi < threequarters: # if 1/4 < lo < hi < 3/4
                straddle+=1
                # ...
                lo = lo-quarter
                hi = hi-quarter
                # ...  subtract 'quarter' from lo and hi
            else:
                break # we break the infinite loop if the interval has reached an un-stretchable state
            lo *= 2
            # ...  multiply hi by 2 and add 1 (I DON'T KNOW WHY +1 IS NECESSARY BUT IT IS. THIS IS MAGIC.
            hi = (2*hi) + 1
    straddle += 1 # adding 1 to straddle for "good measure" (ensures prefix-freeness)
    if lo < quarter: # the position of lo determines the dyadic interval that fits
        y.append(0)
        for i in range(straddle):
            y.append(1)
    else:
        y.append(1)
        for i in range(straddle):
            y.append(0)


    return(y)

def decode(y,p,n):
    precision = 32
    one = int(2**precision - 1)
    quarter = int(ceil(one/4))
    half = 2*quarter
    threequarters = 3*quarter

    p = dict([(a,p[a]) for a in p if p[a]>0])
    
    alphabet = list(p)
    f = [0]
    for a in p:
        f.append(f[-1]+p[a])
    f.pop()

    p = list(p.values())

    y.extend(precision*[0]) # dummy zeros to prevent index out of bound errors
    x = n*[0] # initialise all zeros 

    # initialise by taking first 'precision' bits from y and converting to a number
    value = int(''.join(str(a) for a in y[0:precision]), 2) 
    y_position = precision # position where currently reading y
    lo,hi = 0,one

    x_position = 0
    while 1:
        if x_position % 100 == 0:
            so.write('Arithmetic decoded %d%%    \r' % int(floor(x_position/n*100)))
            so.flush()

        lohi_range = hi - lo + 1
        a = bisect(f, (value-lo)/lohi_range) - 1
        x[x_position] = alphabet[a]
        
        lo = lo + int(ceil(f[a]*lohi_range))
        hi = lo + int(floor(p[a]*lohi_range))
        if (lo == hi):
            raise NameError('Zero interval!')

        while True:
            if hi < half:
                # do nothing
                pass
            elif lo >= half:
                lo = lo - half
                hi = hi - half
                value = value - half
            elif lo >= quarter and hi < threequarters:
                lo = lo - quarter
                hi = hi - quarter
                value = value - quarter
            else:
                break
            lo = 2*lo
            hi = 2*hi + 1
            value = 2*value + y[y_position]
            y_position += 1
            if y_position == len(y):
                break
        
        x_position += 1    
        if x_position == n or y_position == len(y):
            break
        
    return(x)
