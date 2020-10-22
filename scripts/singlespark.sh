#Example using Bowtie2
pipenv run python singlespark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:/s1/snagaraj/sam_folder/singlet 20G 100G 100 3 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -p 3 -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome -" Bowtie2 N 

#Example using HISAT2
#pipenv run python singlespark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:/s1/snagaraj/sam_folder/singlet 20G 100G 100 2 "/s1/snagaraj/hisat2/hisat2 --no-hd --no-sq -p 3 -x /s1/snagaraj/grch38/genome -" HISAT2 Y

#Example using BBMAP
#pipenv run python singlespark.py /s1/snagaraj/project_env/rna_1.fq file:/s1/snagaraj/sam_folder/single 60G 100G 165 3 "java -ea -Xmx45912m -Xms30312m -cp /s1/snagaraj/bbmap/current/ align2.BBMap build=1 overwrite=true fastareadlen=500 in=stdin.fq out=stdout ref=/s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome.fa interleaved=false path=/s1/snagaraj/bbmap build=1 t=2" BBMAP 29 Y

#Example using STAR
#pipenv run python singlespark.py /s1/snagaraj/project_env/rna_3.fq file:/s1/snagaraj/sam_folder/star1 60G 100G 165 3 "/s1/snagaraj/star/source/STAR --runMode alignReads --runThreadN 50 --readFilesIn /dev/stdin --readFilesType Fastx SE --genomeDir /s1/snagaraj/starg --outStd SAM" STAR Y


#$1 $2 $3
