#Authors: Daniel J. Bernstein and Tanja Lange
#Origin:https://blog.cr.yp.to/20171105-infineon4.txt

from sage.doctest.util import Timer

t = Timer()


L = 27771430913146044712156219115012732149015337058745243774375474371978395728107173008782747458575903820497344261101333156469136833289328084229401057505005215261077328417649807720533310592783171487952296983742789708502518237023426083874832018749447215424764928016413509553872836856095214672430
L *= 701 # if 701 is included
g = Mod(65537,L)

pmin = 3*2**1022
pmax = 4*2**1022

t.start()
u = lift(g^randrange(L))
p = 138472867001226056688919061611763715886326314687010168342424329134694501818063936561789831478686372727696077151064170096254865415391899366619089195251977905552486507278878974714226935680943493078368502677778581241305013109280851852405795580792068141722958815059914298166141587146929575396990834469426812358209
print 'time for first prime',t.stop().cputime

t.start()
u = lift(g^randrange(L))
q = 284865139573088696324861426747848592043117862335400667794718725930060674847566730090480108679083107768767399686545490965417403252963754798767527741789030609657657271843591424036462042752864380737757880177772566468323044186226561212226421065970426800031669099925721498463945514943501052597657296138714115583477
print 'time for second prime',t.stop().cputime

n = p * q
print 'public key',n

smooth = 2^7*3^3*5^2*7*11*13*17*19*23
print 'smooth',smooth
def smoothorder(l):
  return smooth % Mod(g,l).multiplicative_order() == 0

v = prod(l for l,e in factor(L) if smoothorder(l))
print 'v=',v
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