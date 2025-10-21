# Data_Provenance
This repository is created to share the knowledge of working with sequences received from sequencing companies.

a. Checking the integrity of all the sequences.
	To prevent corrupted files from further analysis, we are checking the integrity of the sequences based on their MD5 checksums.
	Sequencing companies usually list MD5sum values for all the sequences generated. The idea is to create the same for downloaded sequences and then compare them. 
	The script ```check_md5sum.py``` does this job and outputs a file that has failed this check. 
```
	Usage 
	python verify_md5_fastq_from_pdf.py -p /path/to/reference_hashes.pdf -i /path/to/fastq_files -o /path/to/output/md5_check_results.tsv
```

b. Merging the sequences.
	During the sequencing process, samples can be run over multiple libraries or made multiple runs to achieve the expected number of reads per sample. Thus, multiple forward and reverse reads for the same sample could be produced.
	For sample-wise analysis, an option is to merge the reads(forward and reverse). The script ```merge_rawreads.py``` reads all the sequences, organises them into separate folders, and then merges the forward and reverse reads
	within the folder. These merged sequences can then be utilised for further analysis. 
	
	```
		Usage : 
		python organize_and_merge_fastq.py -i /path/to/fastq_folder -n 10
		n = number of charaters in the name of the sequnce which is the name of the sample.
	```
	
c. Counting reads in sequences.
	The number of reads generated per sample can be calculated to check if the sequences have the requested depth. The rationale here is to count the number of lines in a `fastq` file and divide the number by 4. This is because, 
	fastq files follow the syntax such that every four lines make up one read. Here, the script ```count_reads.py``` checks the file and provides an output file with the number of reads per input sequence.
```
	Usage :
	python count_reads_fastq.py -i /path/to/organized_fastq/
```
