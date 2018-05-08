import random
import math
import copy
import sys
import gmpy2 as g
import sympy.ntheory as nt
import argparse

'''
Original Code by "basavesh": https://gist.github.com/basavesh/3885594
and Matus Nemec et al.

In this version, findAPrime is changed so that the primes generated are vulnerable
to the ROCA attack.

Modifications and additional code by Bernhard Brenner
'''


def euclid(a, b):
    '''returns the Greatest Common Divisor of a and b'''
    a = abs(a)
    b = abs(b)
    # make sure the algorithms still works even when
    # some negative numbers are passed to the program

    if a < b:
        a, b = b, a

    while b != 0:
        a, b = b, a % b

    return a


def coprime(L):
    '''returns 'True' if the values in the list L are all co-prime
       otherwier, it returns 'False'. '''

    for i in range(0, len(L)):
        for j in range(i + 1, len(L)):
            if euclid(L[i], L[j]) != 1:
                return False

    return True


def extendedEuclid(a, b):
    '''return a tuple of three values: x, y and z, such that x is
       the GCD of a and b, and x = y * a + z * b'''
    footprint = []

    # the boolean flag is used to make sure this function can return
    # right answer no matter which is bigger.
    if a < b:
        isASmallerThanB = True
        a, b = b, a
    else:
        isASmallerThanB = False
    while b != 0:
        footprint.append((a % b, 1, a, -(a // b), b))
        # for each tuple in list footprint
        # footprint[i][0] == footprint [i][1] * footprint[i][2]
        #                  + footprint [i][3] * foorprint[i][4]
        # and
        # footprint[i][4] == footprint[i+1][0]
        # this two equations are key to generate the linear combination
        # of a and b so that the result will be their GCD (or GCF).
        a, b = b, a % b

    # Start work backward to compute the linear combination
    # of a and b so that this combination gives the GCD of a and b
    footprint.reverse()
    footprint.pop(0)
    # print (footprint)
    x = footprint[0][1]
    y = footprint[0][3]
    # print (x, y)
    for i in range(1, len(footprint)):
        x_temp = x
        y_temp = y
        x = y_temp * footprint[i][1]
        y = y_temp * footprint[i][3] + x_temp
        # print (x, y)

    if (isASmallerThanB != True):
        return (a, x, y)
    else:
        return (a, y, x)


def modInv(a, m):
    '''returns the multiplicative inverse of a in modulo m as a
       positve value between zero and m-1'''
    # notice that a and m need to co-prime to each other.
    if coprime([a, m]) == False:
        return 0
    else:
        linearcombination = extendedEuclid(a, m)
        return linearcombination[1] % m


def crt(L):
    '''takes in a list of two or more tuples, ie
              L = [(a0, n0), (a1,n1),(a2,n2)...(ak nk)]
       if the n-s are not co-prime, this function prints an error message to
       the screen and returns -1. Otherwise it continues with the Chinese
       Remainder theorem, finding a value for x to return which satisfies
                    x = ai(  mod ni)
       for all tuples in the list L. This value must be between 0 and N-1
       where N is the product of all the n in the list L'''
    NList = []
    for item in L:
        NList.append(item[1])
    if coprime(NList) == False:
        print ("The input is not valid!")
        return -1
    else:
        bigN = 1
        for numbers in NList:
            bigN *= numbers
    CRTresult = 0
    for item in L:
        ai = item[0]
        Ci = bigN // item[1]
        # print (Ni, ai)
        Yi = extendedEuclid(Ci, item[1])
        # print (Ci, item[1])
        CRTresult += ai * Ci * Yi[1]
    return CRTresult % bigN


# start of second project *****************************

def extractTwos(m):
    '''m is a positive integer. A tuple (s, d) of integers is returned
    such that m = (2 ** s) * d.'''
    # the problem can be break down to count how many '0's are there in
    # the end of bin(m). This can be done this way: m & a stretch of '1's
    # which can be represent as (2 ** n) - 1.
    assert m >= 0
    i = 0
    while m & (2 ** i) == 0:
        i += 1
    return (i, m >> i)


def int2baseTwo(x):
    '''x is a positive integer. Convert it to base two as a list of integers
    in reverse order as a list.'''
    # repeating x >>= 1 and x & 1 will do the trick
    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse

def getM(n):
    p = 1
    for i in range(0, n):
        p = p * lowPrimes[i]
    return p

def random_from_interval(random_state, low, high, m=32):
    M = int(g.ceil(g.log2(high)))
    random = g.mpz_urandomb(random_state, M + m)
    c = g.add(g.f_mod(random, g.add(g.sub(high, low), 1)), low)
    return c


def random_prime(random_state, m, generator, power_range, multiple_range):
    random_power = random_from_interval(random_state, power_range[0], power_range[1])
    random_multiple = random_from_interval(random_state, multiple_range[0], multiple_range[1])

    candidate = g.powmod(generator, random_power, m) + random_multiple * m
    while not g.is_prime(candidate):
        candidate += m

    return candidate	

def prime_default(length):
	if length >= 3968:
		return 1427  # real bound 3968
	if length >= 1984:
		return 701  # 701 is used from 1984 rather than 2048
	if length >= 992:
		return 353  # 353 is used from 992 rather than 1024
	if length >= 512:
		return 167
	return 167  # no data for <512, but that doesn't matter anyway


def findAVulnerablePrime(bitSize):
	generator=65537
	m = nt.primorial(prime_default(bitSize), False)

	max_order = nt.totient(m)
	max_order_factors = nt.factorint(max_order)

	order = element_order_general(generator, m, max_order, max_order_factors)
	order_factors = nt.factorint(order)

	power_range = [0, order-1]	
	min_prime = g.bit_set(g.bit_set(g.mpz(0), bitSize // 2 - 1), bitSize // 2 - 2)  # g.add(pow(g.mpz(2), (length / 2 - 1)), pow(g.mpz(2), (length / 2 - 2)))
	max_prime = g.bit_set(min_prime, bitSize // 2 - 4)  # g.sub(g.add(min_prime, pow(g.mpz(2), (length / 2 - 4))), g.mpz(1))
	multiple_range = [g.f_div(min_prime, m), g.c_div(max_prime, m)]

	random_state = g.random_state(random.SystemRandom().randint(0, 2**256))

	
	return random_prime(random_state, nt.primorial(prime_default(bitSize), False),generator, power_range, multiple_range)



def element_order_general(element, modulus, order, order_decomposition):
    if element == g.mpz(1):
        return 1  # by definition
    if g.powmod(element, order, modulus) != g.mpz(1):
        return None  # not an element of the group
    for factor, power in order_decomposition.items():
        for p in range(1, power + 1):
            next_order = g.div(order, factor)
            if g.powmod(element, next_order, modulus) == g.mpz(1):
                order = next_order
            else:
                break
    return order



def newKey(bitSize):
	''' Try to find two large pseudo primes roughly between a=size/2 and b=size/2+1.
	Generate public and private keys for RSA encryption.
	Raises ValueError if it fails to find one'''
	a=math.floor(bitSize/2)
	b=math.floor(bitSize/2)+1


	p = findAVulnerablePrime(bitSize)
	while True:
		q = findAVulnerablePrime(bitSize + 2)
		if q != p:
			break

	n = p * q
	m = (p - 1) * (q - 1)
	while True:
		e = random.randint(1, m)
		if coprime([e, m]):
			break
	d = modInv(e, m)
	return (n, e, d)


def string2numList(strn):
    '''Converts a string to a list of integers based on ASCII values'''
    # Note that ASCII printable characters range is 0x20 - 0x7E
    returnList = []
    for chars in strn:
        returnList.append(ord(chars))
    return returnList


def numList2string(L):
    '''Converts a list of integers to a string based on ASCII values'''
    # Note that ASCII printable characters range is 0x20 - 0x7E
    returnList = []
    returnString = ''
    for nums in L:
        returnString += chr(nums)
    return returnString


def numList2blocks(L, n):
    '''Take a list of integers(each between 0 and 127), and combines them into block size
    n using base 256. If len(L) % n != 0, use some random junk to fill L to make it '''
    # Note that ASCII printable characters range is 0x20 - 0x7E
    returnList = []
    toProcess = copy.copy(L)
    if len(toProcess) % n != 0:
        for i in range(0, n - len(toProcess) % n):
            toProcess.append(random.randint(32, 126))
    for i in range(0, len(toProcess), n):
        block = 0
        for j in range(0, n):
            block += toProcess[i + j] << (8 * (n - j - 1))
        returnList.append(block)
    return returnList


def blocks2numList(blocks, n):
    '''inverse function of numList2blocks.'''
    toProcess = copy.copy(blocks)
    returnList = []
    for numBlock in toProcess:
        inner = []
        for i in range(0, n):
            inner.append(numBlock % 256)
            numBlock >>= 8
        inner.reverse()
        returnList.extend(inner)
    return returnList


def encrypt(message, modN, e, blockSize):
    '''given a string message, public keys and blockSize, encrypt using
    RSA algorithms.'''
    cipher = []
    numList = string2numList(message)
    numBlocks = numList2blocks(numList, blockSize)
    for blocks in numBlocks:
        cipher.append(g.powmod(blocks, e, modN))
    return cipher


def decrypt(secret, modN, d, blockSize):
    '''reverse function of encrypt'''
    numBlocks = []
    numList = []
    for blocks in secret:
        numBlocks.append(g.powmod(blocks, d, modN))
    numList = blocks2numList(numBlocks, blockSize)
    message = numList2string(numList)
    return message



if __name__ == '__main__':

	try:
		bitsize=int(sys.argv[1])
	except:
		print "Usage: ./"+sys.argv[0]+" $bitsize"   
		sys.exit(0)
	bitSize=int(sys.argv[1])

	(n, e, d) = newKey(bitSize)

	message = "This is a testmessage"
	origlen = len(message)
	# print(message)
	cipher = encrypt(message, n, e, 16)
	# print(cipher)
	decryptedMessage = decrypt(cipher, n, d, 16)[:origlen]

	if (message == decryptedMessage):
		print(hex(n))
	else:
		print("Got an error. Please try again!")

