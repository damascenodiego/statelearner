#!/bin/bash

for i in ~/openssl/results/openssl-1.1.1f__t* ; do
  ~/opt/python3.6/bin/python log2tab.py -i $i/tlssul.log  -d $i/learnedModel.dot;
done

~/opt/python3.6/bin/python ./merge_df.py  -d ~/openssl/results/ -p openssl-1.1.1f__ -c ~/openssl/src/build_params.conf 