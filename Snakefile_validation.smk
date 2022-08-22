#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
workdir: config["general_path"]["OUTPUT_PATH"]+'/'+config["general_information"]["Full_name"]
import csv
import re
from os import listdir
from os.path import isfile, join
import os
import json
from datetime import datetime
##########################
start_time = datetime.now()
input_path = config["general_path"]["INPUT_PATH"]
output_path = config["general_path"]["OUTPUT_PATH"]
rulePath = config["general_path"]["SNAKEMAKE_RULES"]
REFERENCE_VCF_Path = config["general_path"]["REFERENCE_VCF_Path"]
BED_Path = config["general_path"]["BED_Path"]
Fasta_Path = config["general_path"]["Fasta_Path"]
Sample_Path = config["general_path"]["Sample_Path"]
##########################
Sample = config["general_information"]["Sample"]
Target = config["general_information"]["Target"]
Type = config["general_information"]["Type"]
Date = config["general_information"]["Date"]
Version = config["general_information"]["Version"]
Run = config["general_information"]['Run']
GS = config["general_information"]["Reference"]
scores = config["Variant_Scores"]["Scores"]
variants =config["Variant_Scores"]["Variant"]
ref_vcf_name = config["general_information"]["VCF_reference"]
bed_file_name = config["general_information"]["Bed_file_name"]
fasta_file_name = config["general_information"]["Fasta_reference"]
full_name = config["general_information"]["Full_name"]
bam_files = config["bam_options"]["paths"]
sv_vcf_path=config["general_path"]["vcf_hg002_path"]
sv_vcf_name=config["general_information"]["vcf_hg002_file_name"]
sv_bed_path=config["general_path"]["bed_hg002_path"]
sv_bed_name=config["general_information"]["bed_hg002_file_name"]
vcf_sv_query_path=config["general_path"]["sv_query_path"]
vcf_sv_query_name=config["general_information"]["sv_query_name"]
tool=config['general_information']['tool']
############################################
include: rulePath + '/Compression_vcf_rule.smk',
include: rulePath + '/Indexing_vcf_tabix.smk',
include: rulePath + '/happy_vcf_rule.smk',
include: rulePath + '/indexing_hap.py_output.smk',
include: rulePath + '/variant_all.smk',
include: rulePath + '/grep.smk',
include: rulePath + '/form.smk',
include: rulePath + '/report.smk',
include: rulePath + "/stats_hapy_to_s3.smk",
include: rulePath + '/write_hapy_to_csv.smk',
include: rulePath + '/compression_happy.smk',
include: rulePath + '/s3_happy.smk',
include: rulePath + '/merge_bam.smk',
include: rulePath + '/generate_ped.smk',
include: rulePath + '/clinsv_bw.smk',
include: rulePath + '/clinsv_lumpy.smk',
include: rulePath + '/clinsv_cnvnator.smk',
include: rulePath + '/clinsv_annotate.smk',
include: rulePath + '/clinsv_prioritize.smk',
include: rulePath + '/clinsv_qc.smk',
include: rulePath + '/compression_clinsv.smk',
include: rulePath + '/s3_clinsv.smk',
include: rulePath + '/witty.smk',
include: rulePath + '/witty_csv.smk',
include: rulePath + '/compression_witty.smk',
include: rulePath + '/s3_witty.smk'
#######Hap.py##############
bgzip = expand("{output_path}/{analysis}/{analysis}.vcf.gz",output_path=output_path, analysis = full_name)
tabix = expand("{output_path}/{analysis}/{analysis}.vcf.gz.tbi",output_path=output_path, analysis = full_name)
hapy= expand("{output_path}/{analysis}/happy/{analysis}.vcf.gz", output_path=output_path, analysis = full_name)
hapy_index=expand("{output_path}/{analysis}/happy/{analysis}.vcf.gz.tbi",output_path=output_path, analysis = full_name)
vcf_all = expand("{output_path}/{analysis}/happy/{variant}/{score}.vcf", output_path=output_path, analysis = full_name,variant= variants, score = scores)
grep = expand("{output_path}/{analysis}/happy/{variant}/{score}.txt", output_path=output_path, analysis = full_name,variant= variants, score = scores)
form = expand("{output_path}/{analysis}/happy/Statistics.csv",output_path=output_path, analysis = full_name)
rapport = expand("{output_path}/{analysis}/happy/Rapport.html",output_path=output_path, analysis = full_name)
s3_stats=expand("{output_path}/{analysis}_hapy_stats_done.txt",output_path=output_path, analysis = full_name)
csv_s3 = expand("{output_path}/{analysis}_happy_csv_done.txt",output_path=output_path, analysis = full_name)
compress_hapy = expand("{output_path}/{analysis}/happy.tar.gz",output_path=output_path, analysis = full_name)
s3_hapy = expand("{output_path}/{analysis}_happy_done.txt",output_path=output_path, analysis = full_name)
########clinsv############
merge = expand("{output_path}/{analysis}/CNV/{analysis}_merged.bam",output_path=output_path,analysis = full_name)
ped = expand("{output_path}/{analysis}/CNV/sampleInfo.ped",output_path=output_path,analysis = full_name)
clinsv_bw = expand("{output_path}/{analysis}/CNV/bw/",output_path=output_path,analysis = full_name)
clinsv_lumpy = expand("{output_path}/{analysis}/CNV/lumpy/",output_path=output_path,analysis = full_name)
clinsv_cnvnator = expand("{output_path}/{analysis}/CNV/cnvnator/",output_path=output_path,analysis = full_name)
clinsv_annotate = expand("{output_path}/{analysis}/CNV/annotate/",output_path=output_path,analysis = full_name)
clinsv_prioritize = expand("{output_path}/{analysis}/CNV/SV-CNV.vcf",output_path=output_path,analysis = full_name)
clinsv_qc = expand("{output_path}/{analysis}/CNV/results",output_path=output_path,analysis = full_name)
compress_clinsv = expand("{output_path}/{analysis}/ClinSV.tar.gz",output_path=output_path,analysis = full_name)
s3_clinsv = expand("{output_path}/{analysis}_ClinSV_done.txt",output_path=output_path,analysis = full_name)
###########Wittyer###############
witty = expand("{output_path}/{analysis}/Witty/",output_path=output_path,analysis = full_name)
witty_csv= expand("{output_path}/{analysis}_Witty_csv_done.txt",output_path=output_path,analysis = full_name)
compress_witty = expand("{output_path}/{analysis}/Wittyer.tar.gz",output_path=output_path,analysis = full_name)
s3_witty = expand("{output_path}/{analysis}_witty_done.txt",output_path=output_path,analysis = full_name)
if tool =='Hap.py':
    print("Running {} ....".format(tool))
    rule all:              
        input: 
            #bgzip,
            #hapy,
            #vcf_all,
            #form,
            #rapport
            #csv_s3,
            #compress_hapy,
            s3_hapy
elif tool == 'ClinSV':
    print("Running {} ....".format(tool))
    rule all:              
        input: 
            #ped,
            #clinsv_bw,
            #clinsv_lumpy,
            #clinsv_cnvnator,
            #clinsv_annotate,
            #clinsv_prioritize,
            #clinsv_qc,
            #compress_clinsv,
            s3_clinsv
elif tool =='Witty':
    print("Running {} ....".format(tool))
    rule all:              
        input: 
            #witty,
            #witty_csv,
            #compress_witty,
            s3_witty 
else:
    raise ValueError("Tool {} not recognized: Supported tools are Hap.py, ClinSV and Wittyer".format(tool))

end_time = datetime.now()
print('Pipeline Duration: {}'.format(end_time - start_time))

