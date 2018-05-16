#Authors: Daniel J. Bernstein and Tanja Lange
#Origin:
from sage.doctest.util import Timer
t = Timer()

L = 27771430913146044712156219115012732149015337058745243774375474371978395728107173008782747458575903820497344261101333156469136833289328084229401057505005215261077328417649807720533310592783171487952296983742789708502518237023426083874832018749447215424764928016413509553872836856095214672430
L *= 701 # if 701 is included
g = Mod(65537,L)

pmin = 3*2**1022
pmax = 4*2**1022

t.start()
u = lift(g^randrange(L))
while True:
  p = 213211959403723720593564350106648494433706268495979589249641302288994301654725678343131948034469207037400911420669861233177540504625637368454622982848015321135645440003949434103479083682001429015945532031691407138958823955531962509970072346872497990178798054883093979504734857210282722002505527566811055945297
  if p.is_prime(): break
print 'time for first prime',t.stop().cputime

t.start()
u = lift(g^randrange(L))
while True:
  q = 301769683940153557539380123630591002144240940468170259156391235157482409167508972355609834603392886909148116332445972889232251396391493807850871112947559788253765961098613901329895549273394971532829781657912664369679161004586796555573559819873919182388451113808891348060923238587196255167447069863039797454307
  if q.is_prime(): break
print 'time for second prime',t.stop().cputime

n = p * q
print 'public key',n

smooth = 2^7*3^3*5^2*7*11*13*17*19*23
print 'smooth',smooth
def smoothorder(l):
  return smooth % Mod(g,l).multiplicative_order() == 0

v = prod(l for l,e in factor(L) if smoothorder(l))
print v
u = p % v
print 'p residue class',(p-u)/v

t.start()

H = 10 + 2**1021 // v
u += floor((7*2**1021) // v) * v

w = lift(1/Mod(v,n))

R.<x> = QQ[]
f = (w*u+H*x)/n
g = H*x

k = 3
m = 7
print 'multiplicity',k
print 'lattice rank',m

basis = [f^j for j in range(0,k)] + [f^k*g^j for j in range(m-k)]
basis = [b*n^k for b in basis]
basis = [b.change_ring(ZZ) for b in basis]

M = matrix(m)
for i in range(m):
  M[i] = basis[i].coefficients(sparse=False) + [0]*(m-1-i)
print 'time for creating matrix',t.stop().cputime

t.start()
M = M.LLL()
print 'time for basis reduction',t.stop().cputime

Q = sum(z*(x/H)^i for i,z in enumerate(M[0]))

for r,multiplicity in Q.roots():
  print 'root is',r
  if u+v*r > 0:
    g = gcd(n,u+v*r)
    if g > 1: print 'successful factorization',[g,n/g]