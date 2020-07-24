#!/bin/bash

start_dir=$(pwd)
src_dir=~/openssl/src
statelearner_dir=~/openssl/

cd ${src_dir}
# Check all versions for which we have the openssl executable
port=4500
for i in $(ls openssl-*/apps/openssl|sort --version-sort); 
	do 
	version=${i%%/*}; 
	echo "Checking ${version}";
	cd ${statelearner_dir};
	java -cp stateLearner-0.0.1-SNAPSHOT.jar nl.cypherpunk.statelearner.tls.TLSTestService localhost ${port} "${start_dir}/${version}/apps/openssl s_server -key ${statelearner_dir}/server.key -cert ${statelearner_dir}/server.crt -CAfile ${statelearner_dir}/cacert.pem -accept ${port} -www";
	cd ${src_dir};
	let "port += 1"
done

cd ${start_dir}
