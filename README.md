# SparkMap
A novel framework to speed up short read alignment using Apache Spark.
SparkMap produces large speed increases for:
- [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml), [BBMAP](https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbmap-guide/), and [HISAT2](http://daehwankimlab.github.io/hisat2/download/) for single-end mapping
- [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) for paired-end mapping

SparkMap can also function with [TopHat](https://ccb.jhu.edu/software/tophat/index.shtml) and works well with [STAR](https://physiology.med.cornell.edu/faculty/skrabanek/lab/angsd/lecture_notes/STARmanual.pdf) when large numbers of machines are available.*

## Installation

SparkMap requires the following dependencies to run:
- Python 3.7 with numpy(> 1.16.4), progressbar2(>3.50.1) , pydoop( > 2.0.0), py4j(> 0.10.7), pyinstaller(>3.6), python-utils(>2.4.0)
- Apache Spark ( > 2.4.3) with findspark( > 1.3.0)
- Hadoop (> 3.1.2)
- Unix sorting. Install GNU core utilities if running on MacOS.

It is also recommended that you run SparkMap in Linux and on a compute cluster.

To download SparkMap, make sure you have the appropriate permissions and then follow these instructions.

First, download the SparkMap repository as a zip file. If needed, send the zip file from your local machine to your computer cluster using scp:

```
scp /path/to/SparkMap-master.zip username@IP:/path/to/directory
```

Unzip it with the following command.

```
unzip SparkMap-master.zip
```

Next, configure your system to make the dependencies accessible. You can either install the dependencies system-wide or through [Pipenv](https://thoughtbot.com/blog/how-to-manage-your-python-projects-with-pipenv). With Pipenv, instead of running python ...., you will run pipenv run python ...

## Configuration Information


First, download Hadoop and Spark, if you have not done so already. We recommend this guide for Spark installation: https://www.linode.com/docs/databases/hadoop/install-configure-run-spark-on-top-of-hadoop-yarn-cluster/ and this guide for Hadoop installation: https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/.

Add these user specific configurations to your .bash_profile.

|                | CONFIGURATIONS                                                                |
|----------------|-------------------------------------------------------------------------------|
| PATH           | ADD SPARKMAP INSTALLATION FOLDER AND LOCATIONS OF SPARK AND HADOOP TO PATH    |                              
| PYTHONPATH     | PATH TO PYTHON3.7                                                             |                 
| JAVA_HOME      | PATH TO JAVA JDK FOR HADOOP                                                   |                            
| HADOOP_CONF_DIR| $HADOOP_HOME:/etc/hadoop                                                      |                        
| SPARK_HOME     | PATH TO SPARK INSTALLATION                                                    |                          
| LD_LIBRARY_PATH| $HADOOP_HOME:/lib/native:$LD_LIBRARY_PATH                                     |                               
|  HADOOP_HOME   | PATH TO HADOOP INSTALLTION                                                    |


Add these user specific configurations to your .bashrc


|                   | CONFIGURATIONS                                                                |
|-------------------|-------------------------------------------------------------------------------|
| PATH              | ADD $HADOOP_HOME/bin and $HADOOP_HOME/sbin to PATH                            |                              
| HADOOP_MAPRED_HOME| $HADOOP_HOME                                                                  |                 
| HADOOP_COMMON_HOME| $HADOOP_HOME                                                                  |                            
| HADOOP_HDFS_HOME  | $HADOOP_HOME                                                                  |                        
| YARN_HOME         | $HADOOP_HOME                                                                  |                                     
| HADOOP_HOME       | PATH TO HADOOP INSTALLTION                                                    |

Check out a full listing of Spark configurations here: https://spark.apache.org/docs/latest/configuration.html

The config directory should only be used as a supplementary resource to edit config files in your $HADOOP_HOME/etc/hadoop directory and your $SPARK_HOME/conf directory.

## Usage Guidelines

### Getting a Reference Genome and Fastq/FASTA files

Skip this step if you already have a Reference Genome and Fastq/FASTA paired-end reads from an experiment. Otherwise, continue if you are using data from online.
Input: Can start with an SRA format (if using online data), but convert to the FastQ file type using fastq dump.
Ex: Fastq-dump --split-files --fasta {Accession #}

Find a genome index online(widely available - [bowtie2](https://support.illumina.com/sequencing/sequencing_software/igenome.html), as a reference genome or build your own.

### Install your mapper as an executable

### Starting Hadoop and Spark

In order to use Hadoop Distributed File System(HDFS), run start-all.sh in the $HADOOP_HOME/sbin directory to start all Hadoop Daemons.

Start the Spark Driver by running start-all.sh in the $SPARK_HOME/sbin directory to start the Spark master and all Spark workers.

### Mapper-Specific Options

Please look at the mapper-specific manuals (linked above) for specific mapper syntax.

However, all mappers should be run with configurations to accept input through STDIN and output their reads to STDOUT. They should also be run locally as an executable and explicitly specify the number of parallel search threads needing to be launched. To run paired-end mapping, please remember to specify interleaved FASTQ input for your mapper.

If you are running Bowtie2 or HISAT2, please explicitly specify the number of parallel search threads using the -p flag.
If you are using BBMAP, please remember to explicitly specify the number of search threads, the java minimum and maximum heap space, the build type, and the path to your prebuilt index. This means that running BBMAP involves creation of the genome index beforehand rather than in-memory. Additionally, make sure that there is a SPACE between the / and align2.BBMap class call as shown in scripts/singlespark.sh for BBMAP.

*If you are using STAR with SparkMap, make sure to set the number of executor instances equal to the number of machines/nodes that you have on your computer cluster. If you do not you will run into executor-level errors!!!

### Running SparkMap in single-end mode

1) Edit singlespark.sh file with parameters in the following format:

   python singlespark.py full_path_to_fastq_directory  full_path_to_sam_output_directory  memory_to_Executor(in GB) driver_Memory(in GB) max_cores_for_process executor_instances      mapper_specific_options mapper_type (max_BBMAP) logging
   
   NOTE: If you are using BBMAP, make sure to specify an additional parameter, max_BBMAP, which indicates the maximum number of partitions you would like to use for your run. This    is needed because BBMAP is RAM intensive and so may run out of RAM if mapping is done on a large dataset with a large number of partitions. For reference, with 3                  executor instances, 3 machines, and 55 cores/250 GB of free RAM per machine, a maximum of 30 partitions could be utilized for mapping. The maximum number of partitions will be    proportional to the number of partitions being sent to each executor instance and amount of RAM. For example, in the aforementioned setup, 10 partitions would be sent to          each executor instance/machine. Loading the genome index and mapping the 10 partitions with 2 parallel search threads per partition on each machine used around 200 GB of RAM.
   
   Make sure that the full_path_to_sam_output_directory contains the prefix file: and that the SAM output directory does not already exist(remove it if it does). Executor and        driver memory should end with G to indicate Gigabytes or MB to indicate megabytes. The logging parameter should be passed either a Y or N for Yes or No. 
   
   Example: python singlespark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:/s1/snagaraj/output/single 20G 100G 100 2 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -p 2 -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome -" 
   
   See sample run file in scripts/singlespark.sh file for further examples.

2) Run "chmod +x singlespark.sh" to give permissions

3) Run ./singlespark.sh to run Spark as an interactive process or run "nohup ./singlespark.sh" to run Spark as a background process.

4) Go into your local output directory and run ``` cat * > combined_sam_file ``` to combine the blocks into a single file.


### Running SparkMap in paired-end mode

1) Edit pairspark.sh file with parameters in the following format:

   python pairspark.py full_path_to_fastq_mate1_directory full_path_to_fastq_mate2_directory full_path_to_sam_output_directory memory_to_Executor(in GB) driver_Memory(in GB)          max_cores_for_process executor_instances mapper_specific_options logging
   
   Make sure that the full_path_to_sam_output_directory contains the prefix file: and that the SAM output directory does not already exist(remove it if it does). Executor and        driver memory should end with G to indicate Gigabytes or MB to indicate megabytes.
   The logging parameter should be passed either a Y or N for Yes or No. 
   
   Example: python pairspark.py /s1/snagaraj/project_env/SRR639031_1.fastq /s1/snagaraj/project_env/SRR639031_2.fastq file:/s1/snagaraj/output/pair 20G 100G 100 2 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -p 2 -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome --interleaved -"


2) Run "chmod +x pairspark.sh" to give permissions

3) Run ./pairspark.sh to run Spark as an interactive process or run "nohup ./pairspark.sh" to run Spark as a background process.

4) Go into your local output directory and run ``` cat * > combined_sam_file ``` to combine the blocks into a single file.

### Optimization of Spark Settings

We have found that found that setting the number of spark executor instances equal to the number of worker nodes/machines on your cluster produces optimal results. Furthermore, we have found that when using smaller numbers cores per machine(< 20) performance was optimized with 2-3 parallel search threads in the mapper-specific options for HISAT2, Tophat, and Bowtie2. For BBMAP, use 1-2 search threads for a smaller number of cores per machine. At larger numbers of cores per machine(> 20), we found that 1-2 parallel search threads worked optimally for HISAT2, Tophat, and Bowtie2. With STAR, you should set the number of threads equal to the number of cores you have available on each machine. This is because when running STAR the number of data partitions used when mapping should equal the number of executor instances you have(which you should specify as the number of machines on your cluster).

If you are familiar with Spark, you can also edit your spark-defaults.conf file and specify the spark.executor.cores parameter for further optimization.

### Validation Scripts

1) Valid_reads.sh/.py- Used to create new SAM files with only mapped reads. Can only used for single-end mapping.

2) Reorder.sh/.py - Used to create new SAM files that are ordered according to read ID. Can only be used for single-end mapping.

3) Alternatively, use the [SAMtools](http://www.htslib.org/doc/samtools-sort.html) sort to sort by chromosome position or by read number.

### Hi-C shell script usage

Use interactions.sh for single-end/locally aligned SAM files and interactions_pair.sh for paired-end SAM files. These scripts are useful to create  interactions data(Hi-C) in the form:

```Chr1 pos1 direction1(0 or 16 for Watson/Crick strand) Chr2 pos2 direction2```

interactions.sh input example: ./interactions.sh test.sam test_interactions.txt
interactions_pair.sh input example: ./interactions_pair.sh test.sam test1.sam test_interactions.txt

### Important Misc. Information

If you ask for a header in your mapper specific options, run  ```awk '!seen[$0]++' orig_file_name > new_file_name ``` to eliminate duplicate headers. Do this BEFORE running any further analyses or you will receive errors. However, we recommend generating the header separately and joining it to the mapping file as this is faster.
