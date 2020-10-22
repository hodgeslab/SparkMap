#Example using Bowtie2
pipenv run python pairspark.py /s1/snagaraj/project_env/SRR639031_1.fastq /s1/snagaraj/project_env/SRR639031_2.fastq file:/s1/snagaraj/sam_folder/pair 20G 100G 100 3 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -p 3 -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome --interleaved -" Y

#$1 $2 $3
