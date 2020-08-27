#!/bin/bash

config_dir=~/openssl/config
src_dir=~/openssl/src
scripts_dir=~/openssl/scripts
learner_dir=~/openssl
results_dir=~/openssl/results

cd ${src_dir}
# Generate configuration file for found openssl executables
port=4000
for i in $(ls openssl-*/openssl-*/apps/openssl|sort --version-sort); 
	do 
	version=${i%%/*};
	config_file="${config_dir}/config_${version}_server.properties"

	echo "Generating server configuration file for ${version} on port ${port}";

	cp "${scripts_dir}/config_openssl_server_template.properties" ${config_file};

	sed -i "s#{IMPL_DIR}#${src_dir}#g" ${config_file};
	sed -i "s#{IMPL_PATH}#${i}#g" ${config_file};
    sed -i "s#{LEARNER_DIR}#${learner_dir}#g" ${config_file};
    sed -i "s#{RESULTS_DIR}#${results_dir}#g" ${config_file};
  	sed -i "s/{VERSION}/${version}/g" ${config_file};
   	sed -i "s/{PORT}/${port}/g" ${config_file};

	let "port += 1"
done

# port=5000
# for i in $(ls openssl-*/openssl-*/apps/openssl|sort --version-sort);
#         do
# 	version=${i%%/*};
#         config_file="${config_dir}/config_${version}_client.properties"

#         echo "Generating client configuration file for ${version} on port ${port}";

#         cp "${scripts_dir}/config_openssl_client_template.properties" ${config_file};

# 	sed -i "s#{IMPL_DIR}#${src_dir}#g" ${config_file};
#         sed -i "s#{LEARNER_DIR}#${learner_dir}#g" ${config_file};
#         sed -i "s#{RESULTS_DIR}#${results_dir}#g" ${config_file};
#       	sed -i "s/{VERSION}/${version}/g" ${config_file};
#        	sed -i "s/{PORT}/${port}/g" ${config_file};

# 	let "port += 1"
# done
