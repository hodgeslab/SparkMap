#Supplmentary script to order SAM file by ReadID produced by SparkMap
#Only for Single-end mode mapping.
import sys
in_file = sys.argv[1]
delimiter = sys.argv[2]
out_file = sys.argv[3]

with open(in_file, 'r') as f:
     lines = f.read().splitlines()
tmp = in_file + ".tmp"
with open(tmp, 'w') as fp:
    for line in lines:
        part = line.split()
        id = part[0]
        end_id = id.split(delimiter)[-2]
        print(end_id + " " + line, file = fp)

f.close()
fp.close()
lines = open(tmp, 'r').readlines()
output = open(out_file, 'w')
sorted_lines =  sorted(lines, key = lambda x: int(x.split()[0]))

for line in sorted_lines:
    line = line.split()[1:]
    for element in line:
        output.write(element + '\t')
    output.write('\n')

output.close()
