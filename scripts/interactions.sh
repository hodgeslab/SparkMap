#!/bin/bash

#  condense single SAM file into id, chromosome #, positional information, DNA sequence, and directional strand
awk '{print $1,$3,$4,$2,$5;}' $1 > pair.sam

# Sort according to read id
sort -V -k1 pair.sam > pair_sorted.sam

paste -d " "  - - < pair_sorted.sam > pair_sorted_merge.sam
awk '{if($1 eq $6 && $5>= 30 && $10 >= 30 && substr($2,1,3) == "chr" && substr($7,1,3) == "chr" && $3 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) print $2,$3,$4,$7,$8,$9}' pair_sorted_merge.sam > $2
