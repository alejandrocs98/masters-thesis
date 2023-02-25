#!/bin/bash
for i in $(ls genomes-proteins); do
	name=$(basename $i _aa.fasta);
	carve $i -g LB --fbc2 -o gsmms/$name.xml;
done

carve -r genomes-proteins/*.fasta -g LB --fbc2 -o gsmms/;