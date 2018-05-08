## Reproduction of: The Return of Coppersmith's Attack: Practical Factorization of Widely Used RSA Moduli (ACM CCS 2017)

In their publication, Nemec et al. have shown that keys generated in cryptographic
smartcards using cryptographic hardware of Infineon Technologies AG (at least since 2012) are based on constructed primes 
(as opposed to randomly chosen primes).

They have shown that the primes are constructed as follows:
 
P = k * M + (65537^a mod  M)

where M is known. They reduced the necessary effort of factorizing a 
a given Modulus N down to the search of a proper tuple (k,a).
 
To find out if a certain Modulus is vulnerable, their algorithm searches for the 
existence of a discrete logarithm: log_65537(N) mod M. 
Nemec et.al. used the Pohlig-Hellman algorithm to find such logarithms.

Chapters (2.3.2 and 2.3.3) describe the factorization of weak Moduli N.

Along with the paper, the authors provided an online test suite (available [here](https://keytester.cryptosense.com/)) to test
own keys (Moduli) for vulnerability and Python code implementing fingerprints, but not factorization. 
In this experiment, we run the python version of the fingerprinting and factorization algorithm they provided with their
paper. 

Note: 
Some interesting resource have been found on the internet:
 [Blogpost by D. Bernstein and T. Lange](https://blog.cr.yp.to/20171105-infineon.html) on the cr.yp.to blog to find out whether the authors leaked information when announcing that there was a vulnerability. In addition, they provide the SageMath sourcecode of
 their optimized attack. We also tested the code. The output can be seen at ./result/SageMath
 [Wikipedia article](https://en.wikipedia.org/wiki/ROCA_vulnerability) about this weakness.

## Experiment Setup

### Experiment Content

We first try the experiment using the provided data and then generate our own data and test it again.

We perform some fingerprint detection using all provided data.
We perform fingerprinting on provided self generated vulnerable and non-vulnerable keys and on ten chosen popular websites on the internet.
We run the attack implemented in SageMath by [Daniel Bernstein and Tanja Lange](https://blog.cr.yp.to/20171105-infineon4.txt) 
on vulnerable and non-vulnerable keys. 

### Hardware/Software

#### Our Hardware:

Intel Core i7-6700HQ, 8GB DDR4 UDIMM RAM (NON-ECC)

#### Our Software:
Windows 10, Python version: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:53:40) [MSC v.1500 64 bit (AMD64)] on win32

		
## Experiment Assumptions

- No considerable assumptions

## Preconditions

-roca-detect library would normally be needed. Instead, it is delivered within the code to make it easier to see the sourcecode.
-python modules: gmpy2 and sympy for the generation of vulnerable keys

## Experiment Steps

### Test fingerprinting with original data
	python test_fingerprint.py
	python test_tls.py
	python detect.py

### Testing fingerprinting with custom data

#### Testing tls fingerprinting with Top10 most visited Websites (APR 2018)
	python detect_tls.py ..\..\data\tlslist_top10.txt 
	
#### Generating custom non vulnerable keys
	python generate_non_vulnerable_key.py 512 > ..\data\non_vulnerable_keys\custom_mod1_512.txt
	python generate_non_vulnerable_key.py 768 > ..\data\non_vulnerable_keys\custom_mod2_768.txt
	python generate_non_vulnerable_key.py 1024 > ..\data\non_vulnerable_keys\custom_mod3_1024.txt
	python generate_non_vulnerable_key.py 2048 > ..\data\non_vulnerable_keys\custom_mod4_2048.txt
	python generate_non_vulnerable_key.py 4096 > ..\data\non_vulnerable_keys\custom_mod5_4096.txt

#### Testing custom non vulnerable keys
	python detect.py ..\..\data\non_vulnerable_keys\ 
	
#### Generating custom vulnerable keys
	python generate_vulnerable_key.py 512 > ..\data\vulnerable_keys\custom_mod1_512.txt
	python generate_vulnerable_key.py 768 > ..\data\vulnerable_keys\custom_mod2_768.txt
	python generate_vulnerable_key.py 1024 > ..\data\vulnerable_keys\custom_mod3_1024.txt
	python generate_vulnerable_key.py 2048 > ..\data\vulnerable_keys\custom_mod4_2048.txt
	python generate_vulnerable_key.py 4096 > ..\data\vulnerable_keys\custom_mod5_4096.txt

#### Testing custom vulnerable keys
	python detect.py ..\..\data\vulnerable_keys\custom_mod1.txt 
	
#### Factorizing a custom (generated) 2048 Bit vulnerable key
	Start SageMath
	run "attack.sage"

#### Factorizing own custom X Bit vulnerable keys
	run:
	python generate_vulnerable_key_show_primes.py
	
	Copy the primes into the file: attack_fixed_prime.sage (after "p=" and "q=", or n after "n=")
 	
	Start SageMath
	run "attack_fixed_primes.sage"
	
	Note: This is not a full attack, as some information (u,v) about the primes is already known which would have to be searched for in a real attack.
		
## Results

see : 
./result/result_output.txt
./result/SageMath/*

