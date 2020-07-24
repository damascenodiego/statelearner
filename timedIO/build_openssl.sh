#!/bin/bash

src_dir=~/openssl/src

echo "===Building OpenSSL binaries==="

# If compilation failed try removing crypto/bn/bn_prime.h
# http://arstechnica.com/civis/viewtopic.php?f=16&t=252612

cd ${src_dir}

# Clean and build all
for i in $(ls openssl-*.tar.gz);
	do
  version=$(basename $i .tar.gz);
	echo $i;
	# Check if the executable is already there
	while read p; do
		_id=`echo $p |cut -d\; -f1`
		_conf=`echo $p |cut -d\; -f2`
		if [ ! -e "${version}/apps/openssl" ]
			then
      echo "################################################################"
			echo "Unpacking ${version}__${_id}"
			mkdir -p ./${version}__${_id}/
			tar -C ./${version}__${_id}/ -zxf $i;
			cd ./${version}__${_id}/${version};
      echo "Building"
			# Cleanup in case there are some old leftovers
			make clean > ../clean.log 2> ../clean.err;
      # Small tweak necessary for older OpenSSL versions
			sed -i 's/m486/m64/g' Configure;
			# Configure so all versions compile
			echo no-shared ${_conf} -fPIC |tee ../parameters.log
      ./config no-shared ${_conf} -fPIC > ../config.log 2> ../config.err;
			make  > ../make.log 2> ../make.err;
			cd ${src_dir}
			echo "################################################################"
		else
		  echo "Nothing to do. Executable already exists."
		fi
	done < build_params.conf
done
