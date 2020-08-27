#!/bin/bash

results_dir=~/openssl/results

echo "Experiment;Version;Time (ms);Time (sec);Time (min);Membership queries (cache);Membership queries (SUL);Equivalence queries (cache);Equivalence queries (SUL);States;Rounds;MD5 learnedModel.dot"

cd ${results_dir}
for i in $(ls);
	do
	if [ -e "$i/learnedModel.dot" ]
	then
		version=${i#*-}
		version=${version%_server_clienthelloreset_modifiedwmethod_2}
                version=${version%_client_modifiedwmethod_2}
		time=$(grep 'Total time' $i/learner.log|awk '{print $4}')
                equivQueriesCache=$(grep -F 'equivalence queries to cache' $i/learner.log|awk '{print $7}')
		equivQueriesSUL=$(grep -F 'equivalence queries to SUL' $i/learner.log|awk '{print $7}')
		memQueriesCache=$(grep 'membership queries to cache' $i/learner.log|awk '{print $7}')
                memQueriesSUL=$(grep 'membership queries to SUL' $i/learner.log|awk '{print $7}')
		states=$(grep 'States in final hypothesis' $i/learner.log|awk '{print $6}')
		rounds=$(grep -F 'Rounds []' $i/learner.log|awk '{print $4}')
		md5=$(md5sum $i/learnedModel.dot|awk '{print $1}')
		echo "$i;$version;${time::-1};$(expr ${time::-1} / 1000);$(expr ${time::-1} / 60000);$memQueriesCache;$memQueriesSUL;$equivQueriesCache;$equivQueriesSUL;$states;$rounds;$md5"
	fi
done
