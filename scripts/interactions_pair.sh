#!/bin/bash

# Script to create single file with all interactions data from 2 single-end SAM files

#  extract important information from sam file
awk '{print $1,$3,$4,$2,$5;}' $1 > sam
awk '{print $1,$3,$4,$2,$5;}' $2 > sam_1
 
# Sort according to read id
sort -V -k1 sam > sorted_sam
sort -V -k1 sam_1 > sorted_sam_1


paste sorted_sam sorted_sam_1 > sorted

#check appropriate conditions for pairing of interacting reads
awk '{if($1 eq $6 && $5>= 30 && $10 >= 30 && substr($2,1,3) == "chr" && substr($7,1,3) == "chr" && $3 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) print $2,$3,$4,$7,$8,$9}'  sorted  > $3
