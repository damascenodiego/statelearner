#!/bin/bash

start_dir=$(pwd)
statelearner_dir=~/openssl
config_dir=~/openssl/config
results_dir=~/openssl/results

# Get a list of version that passed the sanity check
list=$(cat sanity_check.txt|grep -B 1 Application|grep -v Application|grep -v "\-\-"|awk '{print $2}')

# Learn all implementations that passed the sanity check
for i in ${list};
	do
	version=$i
	echo "Learning ${version}";

	# Check if configuration file exists
	if [ ! -e "${config_dir}/config_${version}_server.properties" ]
		then
		echo "No corresponding configuration file found";
		exit
	fi

	# Check if version was not learned yet
	if [ ! -e "${result_dir}/${version}_server_clienthelloreset_modifiedwmethod_2/learnedModel.dot" ]
		then
		echo "No learnedModel.dot exists for ${version}. Start learning"
		cd ${statelearner_dir};
		java -jar stateLearner-0.0.2-SNAPSHOT.jar "${config_dir}/config_${version}_server.properties";
		cd ${start_dir}
	else
		echo "learnedModel.dot exists for ${version}"
	fi
done
