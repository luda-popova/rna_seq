#!/usr/bin/env python 

# add shebang at top of file
# shebang tells the shell how to interpret the file

# Set permission to run file
#    ls -la 
#    chmod ugo+x get_sra.py 
#    module load sratoolkit (or fastq-dump will not work)
#
import pandas as pd
import sys
import subprocess
import os.path
from shutil import copyfile

if len(sys.argv) == 1:
  print("Too few arguments ... exiting")
  sys.exit(-1)
if len(sys.argv) > 2 :
  print("Too many arguments ... ignoring extra arguments")

if os.path.isfile(sys.argv[1]) == False:
  print("SRR file not found ... exiting")
  sys.exit(-2)

# open SRR_Acc_list.txt
df = pd.read_csv(sys.argv[1],header=None)

sras = df[0].tolist()

for sra in sras:
    #testing if SRA file is already downloaded
    if os.path.isfile(sra+".sra") == True and os.path.isfile(sra+"_tmp.sra") == False:
        print(sra+".sra" " FILE ALREADY DOWNLOADED")
        continue
    #testing if both SRR and temp file exist
    elif os.path.isfile(sra+".sra") == True and os.path.isfile(sra+"_tmp.sra") == True:
        os.remove(sra+"_tmp.sra")
        continue
        
    ftp_root = "ftp://ftp-trace.ncbi.nih.gov"

    #"/sra/sra-instant/reads/ByRun/sra/{SRR|ERR|DRR}/<first 6 characters of accession>/<accession>/<accession>.sra"
    sra_path = "/sra/sra-instant/reads/ByRun/sra/{}/{}/{}/{}.sra".format(sra[0:3],sra[0:6],sra,sra)

    #print(ftp_root + sra_path)

    exit_status = subprocess.run(['wget','-c' ,'-O',sra+"_tmp.sra",ftp_root + sra_path])
    print(exit_status)
    print(exit_status.returncode)
    #subprocess.run(['fastq-dump',sra])

    if exit_status.returncode == 0:
        copyfile(sra+"_tmp.sra", sra+".sra")
    else:
        print("Did Not Copy")
    if os.path.isfile(sra+".sra") and os.path.isfile(sra+"_tmp.sra") == True:
        os.remove(sra+"_tmp.sra")

# download fastq files from sra files
for sra in sras:
    if os.path.isfile(sra+".fastq") == False:
        print("CONVERTING "+ sra+".sra"+ " TO FASTQ FILE...")
        subprocess.run(['fastq-dump',sra + ".sra"])
    else:
        print(sra + " .FASTQ ALREADY DOWNLOADED")
        continue
    
    #if os.path.isfile(sra+".fastq") == True and os.path.isfile(sra+".sra") == True:
         #os.remove(sra+".sra")
    #elif os.path.isfile(sra+".fastq") == True and os.path.isfile(sra+".sra") == False:
         #continue
         
         
# open SRR_Acc_list.txt
# use pandas
# read.csv with pandas

# for every line
#   get the SRR number
#   download the SRA file
#   convert file to fastq formatuuu


#Conda tips
#1) On osc enable python with ...
# module load python
# module load sratoolkit
#
#2) Create environment with
# conda create -n getsra
#
#3) Activate environment
# conda activate getsra
# source activate getsra

#4) Install pandas
# conda install pandas
#
#5) list environments on system
# ls ~/.conda/envs
#
# Copy and Past
# Crtl-a select all
# Ctrl-c copy
# Ctrl-v paste
