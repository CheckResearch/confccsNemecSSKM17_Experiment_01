
echo Test fingerprinting with original data
	cd code\originalcode
	python test_fingerprint.py
	python test_tls.py
	python detect.py

echo Test fingerprinting with custom data

echo Test tls fingerprinting with Top10 most visited Websites (APR 2018)
	python detect_tls.py ..\..\data\tlslist_top10.txt 
	
echo Generating custom non vulnerable keys
	cd ..
	python generate_non_vulnerable_key.py 512 > ..\data\non_vulnerable_keys\custom_mod1_512.txt
	python generate_non_vulnerable_key.py 768 > ..\data\non_vulnerable_keys\custom_mod2_768.txt
	python generate_non_vulnerable_key.py 1024 > ..\data\non_vulnerable_keys\custom_mod3_1024.txt
	rem python generate_non_vulnerable_key.py 2048 > ..\data\non_vulnerable_keys\custom_mod4_2048.txt
	rem this costs quite a lot of resources (at least in this non-optimized implementation). uncomment if you have a lot of time or computing power
	rem python generate_non_vulnerable_key.py 4096 > ..\data\non_vulnerable_keys\custom_mod5_4096.txt

echo Test custom non vulnerable keys
	cd originalcode
	python detect.py ..\..\data\non_vulnerable_keys\ 
	
echo Generating custom vulnerable keys
	cd ..
	python generate_vulnerable_key.py 512 > ..\data\vulnerable_keys\custom_mod1_512.txt
	python generate_vulnerable_key.py 768 > ..\data\vulnerable_keys\custom_mod2_768.txt
	python generate_vulnerable_key.py 1024 > ..\data\vulnerable_keys\custom_mod3_1024.txt
	rem python generate_vulnerable_key.py 2048 > ..\data\vulnerable_keys\custom_mod4_2048.txt
	rem	python generate_vulnerable_key.py 4096 > ..\data\vulnerable_keys\custom_mod5_4096.txt
	
echo Test custom vulnerable keys
	cd originalcode
	python detect.py ..\..\data\vulnerable_keys\
	
echo "Done Testing. If you want to run attacks, you have to install SageMath and copy-paste the SageMath scripts into the shell. You may also modify the primes if you want."
