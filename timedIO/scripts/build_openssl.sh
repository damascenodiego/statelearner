#!/bin/bash

src_dir=~/openssl/src

echo "===Building OpenSSL binaries==="

# Make sure perl is in the right place
if [ ! -e "/usr/local/bin/perl" ] 
	then
	echo "Perl not found in /usr/local/bin";
	echo "Try running:";
	echo "sudo ln -s /usr/bin/perl /usr/local/bin/perl";
	exit
fi

# If compilation failed try removing crypto/bn/bn_prime.h
# http://arstechnica.com/civis/viewtopic.php?f=16&t=252612

cd src_dir

# Clean and build all
for i in $(ls openssl-*.tar.gz);
	do
        version=$(basename $i .tar.gz);
	echo $i;
	# Check if the executable is already there
	if [ ! -e "${version}/apps/openssl" ]
		then
		echo "Unpacking"
		tar zxf $i;
		cd ${version};
                echo "Building"
		# Cleanup in case there are some old leftovers
		make clean;
                # Small tweak necessary for older OpenSSL versions
		sed -i 's/m486/m64/g' Configure; 
		# Configure so all versions compile
                ./config no-asm no-shared -fPIC;
		make;
		cd ${src_dir}
	else
		echo "Nothing to do. Executable already exists."
	fi
done
