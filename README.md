# Data_Provenance
This repository is created to share the knowledge of working with sequences received from sequencing companies.

a. Checking the integrity of all the sequences.
	To prevent corrupted files from further analysis, we are checking the integrity of the sequences based on their MD5 checksums.
	Sequencing companies usually provide a list of MD5sum values for all the sequences generated. The idea is to generate the same for downloaded sequences and then compare them. 
	The script ```check_md5sum.py``` does this job and outputs a file that has failed this check. 

	''' Usage 
	python verify_md5_fastq_from_pdf.py \
  -p /path/to/reference_hashes.pdf \
  -i /path/to/fastq_files/ \
  -o /path/to/output/md5_check_results.tsv'''

b. Merging the sequences.
c. Counting reads in sequences.
