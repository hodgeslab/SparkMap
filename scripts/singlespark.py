import findspark
findspark.init()
from pyspark import SparkConf, SparkContext, TaskContext, SparkFiles
import math
import os
import time
from pyspark.sql import SQLContext
import subprocess
import sys
import pydoop.hdfs as hdfs
import logging

fq_input = sys.argv[1]
direc_path = sys.argv[2]
exec_mem = sys.argv[3]
driver_mem = sys.argv[4]
max_cores = sys.argv[5]
exec_instances = sys.argv[6]
options = sys.argv[7]
mapper_name = sys.argv[8]
if mapper_name == "BBMAP":
   max_BBMAP = sys.argv[9]
   bool_log = sys.argv[10]
else:
   bool_log = sys.argv[9]

conf = SparkConf().setAppName("SingleSparkAligner")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', exec_mem).set('spark.driver.memory', driver_mem).set("spark.cores.max", max_cores).set("spark.executor.instances", exec_instances)
sc = SparkContext.getOrCreate(conf=conf)
sc.setLogLevel("ERROR")

if bool_log == "Y":
   logging.basicConfig(filename='singlespark.log', filemode='w', level=logging.INFO)
   logging.getLogger().setLevel(logging.INFO)
   logging.info(sc.getConf().getAll())

subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user"])
subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", fq_input, "/user/data" ])

if bool_log == "Y":
   logging.info("SAM Output Directory %s" % (direc_path))
    
fq_input = fq_input.split('/')
test_len = len(fq_input) - 1
end_input = fq_input[test_len]

input_file = "hdfs:/user/data/" + end_input

# Uncomment for process timing
start = time.time()
# create key-value pair with (read on line, line number)
zipped_input = (sc.textFile(input_file)).zipWithIndex()

add = zipped_input.keyBy(lambda x: math.floor(x[1]/4))
if bool_log == "Y":
   temp = add.takeOrdered(4)
   str_temp = ("\n".join([",".join(map(str, item)) for item in temp]))
   logging.info("Zipped FastQ \n%s" % (str_temp))

# Combine all strings with the same key together
def joining_func(line):
    sort_tup = sorted(line[1], key = lambda x: x[1])
    return '\n'.join([y[0] for y in sort_tup])

#Group all lines with the same Key and join them together by their original position in the file
rdd_add = add.groupByKey().map(joining_func)
if bool_log == "Y": 
   temp = rdd_add.takeOrdered(4)
   str_temp = ("\n".join(["".join(map(str, item)) for item in temp]))
   logging.info("Grouped and Joined Output \n%s" % (str_temp))

instances = int(exec_instances)
if mapper_name == "STAR":
 rdd_add = rdd_add.coalesce(instances)
 if bool_log == "Y":
    logging.info("Coalescing to %s partitions with STAR" %  (str(instances)))


parts = int(max_cores)
if mapper_name == "BBMAP" and parts >= int(max_BBMAP):
   int_BBMAP = int(max_BBMAP)
   rdd_add = rdd_add.coalesce(int_BBMAP)
   if bool_log == "Y":
      logging.info("Coalescing to %s partitions with BBMAP" % (max_BBMAP))


#starts mapper with parameters to index and options.
try:
    alignment_pipe = rdd_add.pipe(options)
except:
    if bool_log == "Y":
       logging.error("Could not perform mapping. Check syntax of mapper options")
    print("Could not perform mapping. Check syntax of mapper options")
    quit()

if bool_log == "Y":
   temp = alignment_pipe.take(4)
   str_temp = ("\n".join(["".join(map(str, item)) for item in temp]))
   logging.info("Mapper Output \n%s" % (str_temp))

if bool_log == "Y":
   logging.info("Number of Partitions: %s" % (str(alignment_pipe.getNumPartitions())))

counter = alignment_pipe.count()
counter = int(counter)
if counter == 0:
   print("ERROR: Could not perform mapping. Check syntax of mapper options and spark executor logs(located at $SPARK_HOME/work) for errors. If you are running BBMAP, please decrease the max_BBMAP parameter.")
   if bool_log == "Y":
      logging.error("Could not perform mapping. Check syntax of mapper options and spark executor logs(located at $SPARK_HOME/work) for errors. If you are running BBMAP, please decrease the max_BBMAP parameter.")
   quit()
else:
   if bool_log == "Y":
      logging.info("Number of Reads: %s" % (str(counter)))


#Collecting output and maintaining parallelization while writing to local file
alignment_pipe.saveAsTextFile(direc_path)

#Uncomment if you want to record process timing
end = time.time()
if bool_log == "Y":
   logging.info("Runtime: %s" % (str(end-start)))
sc.stop()
