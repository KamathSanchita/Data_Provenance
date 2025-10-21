# Data_Provenance
This repository is creatd to share the knowledge of working with sequences that are received from sequencing companies.

a. Checking the integrity of all the sequences.
	To avoide corrupted files from further analysis, here we are checking the integrity of the sequences base on its md5checksum hashes.
	Sequencing companies usually provide alist of md5sum values all the sequences wen generated. The idea is to generate the same for downloaded sequences and then to compare them. 
	The script ```check_md5sum.py``` does this job and outputs a file which has failed this check. 
b. Merging the sequences.
c. COunting reads in sequences.
