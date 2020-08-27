#!/bin/bash

src_dir=~/openssl/src

echo "===Downloading OpenSSL sources==="
cd ${src_dir}
wget -r -N -nd ftp://anonymous:pwd@ftp.openssl.org/source/
