#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Firas Akermi 
# 2022/05/09
# python3
#Script for creating snakemake config file 
from __future__ import unicode_literals
from datetime import datetime
import json
import argparse
import os
import glob
############
def create_json(INPUT_PATH,OUTPUT_PATH,SNAKEMAKE_RULES,REFERENCE_VCF_Path,BED_Path,Fasta_Path,
                Sample_Path,old_pipelines,Reference, Version, Run, Alias, Target, Disease, Sample,
                 Type, Date, analysis_name,fasta_name,bed_name,ref_vcf_name,user,ip,
                 s3_bucket,base_bam,prefix_analysis,suffix_analysis,vcf_hg002_path,vcf_hg002_name,
                 bed_hg002_path,bed_hg002_name,sv_vcf_query_path,sv_vcf_query_name,Env,tool):
    data_config= {}
    data_config["general_path"]={
        "INPUT_PATH":INPUT_PATH,
        "OUTPUT_PATH": OUTPUT_PATH,
        "SNAKEMAKE_RULES": SNAKEMAKE_RULES,
        "REFERENCE_VCF_Path": REFERENCE_VCF_Path,
        "BED_Path": BED_Path,
        "Fasta_Path":Fasta_Path,
        "Sample_Path": Sample_Path,
        "base_bam":base_bam,
        "old_pipelines":old_pipelines,
        "vcf_hg002_path":vcf_hg002_path,
        "bed_hg002_path":bed_hg002_path,
        "sv_query_path":sv_vcf_query_path
    }
    data_config["general_information"]={
        "Description": "This script creates a config file for variant calling validation",
        "Run": Run,
        "Alias": Alias,
        "Target": Target,
        "Disease": Disease,
        "Sample": Sample,
        "Type":Type,
        "Date":Date,
        "Version": Version,
        "Full_name": analysis_name,
        "Reference": Reference,
        "Environnement":Env,
        "Fasta_reference": fasta_name,
        "Bed_file_name": bed_name,
        "VCF_reference": ref_vcf_name,
        "prefix_analysis":prefix_analysis,
        "suffix_analysis": suffix_analysis,
        "bed_hg002_file_name":bed_hg002_name,
        "vcf_hg002_file_name":vcf_hg002_name,
        "sv_query_name":sv_vcf_query_name,
        "tool":tool
    }
    data_config["Variant_Scores"]={
        "Variant": [
            "SNP_INDEL_ALL",
            "SNP_INDEL_het",
            "SNP_INDEL_homalt",
            "SNP_INDEL_hetalt",
            "SNP_INDEL_het_homalt",
            "SNP_ALL",
            "SNP_het",
            "SNP_homalt",
            "SNP_hetalt",
            "SNP_het_homalt",
            "INDEL_ALL",
            "INDEL_het",
            "INDEL_homalt",
            "INDEL_hetalt",
            "INDEL_het_homalt"
        ],
        "Scores": [
            "TP",
            "FN",
            "FP",
            "FNP",
            "FNT",
            "FPP",
            "FPT"
        ],
    }
    data_config['scripts']={
    "extract_script": INPUT_PATH+"/script/extraction.py",
    "create_form":INPUT_PATH+"/script/create_report.py",
    "S3_hapy":INPUT_PATH+"/script/aws_s3_hap.py",
    "hapy_stats_S3":INPUT_PATH+"/script/hapy_stats_S3.py",
    "hapy_S3_csv":INPUT_PATH+"/script/csv_hapy_to_s3.py",
    "witty_S3_csv":INPUT_PATH+"/script/witty_to_csv.py"
    }
    data_config['S3']={
    "USER":user,
    "IP":ip,
    "Bucket_name":user+'-'+s3_bucket,
    
    }
    data_config["SNP_INDEL_ALL"]={
    "TP":  '-i'+" ' "+'BD[0]="TP"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP"'+" ' ",
    }
#
    data_config["SNP_INDEL_het"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && BLT[0]="het"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BLT[0]="het"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BLT[1]="het"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BLT[0]="het"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BLT[0]="het" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BLT[1]="het" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="het"'+" ' ",
    }
#
    data_config["SNP_INDEL_homalt"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && BLT[0]="homalt"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BLT[0]="homalt"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BLT[1]="homalt"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BLT[0]="homalt"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BLT[0]="homalt" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BLT[1]="homalt" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="homalt"'+" ' ",
    }
    data_config["SNP_INDEL_hetalt"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && BLT[0]="hetalt"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BLT[0]="hetalt"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BLT[1]="hetalt"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BLT[0]="hetalt"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BLT[0]="hetalt" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BLT[1]="hetalt" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="hetalt"'+" ' ",
    }
    data_config["SNP_INDEL_het_homalt"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && (BLT[0]="homalt" || BLT[0]="het")'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && (BLT[0]="het" || BLT[0]="homalt")'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && (BLT[1]="het" || BLT[1]="homalt")'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && (BLT[0]="het" || BLT[0]="homalt")'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && (BLT[0]="homalt" || BLT[0]="het") && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && (BLT[1]="het" || BLT[1]="homalt") && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && (BLT[1]="het"|| BLT[1]="homalt" )'+" ' ",
    }
    data_config["SNP_ALL"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && BVT[0]="SNP"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BVT[0]="SNP"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BVT[0]="SNP"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="SNP" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BVT[1]="SNP"'+" ' ",
    }
#
    data_config["SNP_het"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && BVT[0]="SNP" && BLT[0]="het"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BLT[0]="het" && BVT[0]="SNP"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[1]="het"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BLT[0]="het" && BVT[0]="SNP"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="SNP" && BLT[0]="het" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[1]="het" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="het" && BVT[1]="SNP"'+" ' ",
    }
#
    data_config["SNP_homalt"]={
    "TP":  '-i'+" ' "+'BD[0]="TP" && BVT[0]="SNP" && BLT[0]="homalt"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BLT[0]="homalt" && BVT[0]="SNP"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[1]="homalt"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BLT[0]="homalt" && BVT[0]="SNP"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="SNP" && BLT[0]="homalt" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[1]="homalt" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="homalt" && BVT[1]="SNP"'+" ' ",
    }
#
    data_config["SNP_hetalt"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="SNP" && BLT[0]="hetalt"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BLT[0]="hetalt" && BVT[0]="SNP"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[1]="hetalt"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BLT[0]="hetalt" && BVT[0]="SNP"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="SNP" && BLT[0]="hetalt" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && BLT[1]="hetalt" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="hetalt"&& BVT[1]="SNP"'+" ' ",
    }
#
    data_config["SNP_het_homalt"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="SNP" && (BLT[0]="homalt" || BLT[0]="het")'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && (BLT[0]="homalt" || BLT[0]="het") && BVT[0]="SNP"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && (BLT[1]="het" || BLT[1]="homalt")'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && (BLT[0]="homalt" || BLT[0]="het") && BVT[0]="SNP"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="SNP" && (BLT[0]="homalt" || BLT[0]="het") && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="SNP" && (BLT[1]="het" || BLT[1]="homalt") && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && (BLT[1]="het" || BLT[1]="homalt" ) && BVT[1]="SNP"'+" ' ",
    }
#
    data_config["INDEL_ALL"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="INDEL"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BVT[0]="INDEL" '+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BVT[1]="INDEL"'+" ' ",
    }
#
    data_config["INDEL_het"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="INDEL" && BLT[0]="het"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BLT[0]="het"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[1]="het"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BVT[0]="INDEL" && BLT[0]="het"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BLT[0]="het" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[1]="het" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="het" && BVT[1]="INDEL"'+" ' ",
    }
#
    data_config["INDEL_homalt"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="INDEL" && BLT[0]="homalt"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BLT[0]="homalt"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[1]="homalt"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BVT[0]="INDEL" && BLT[0]="homalt"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BLT[0]="homalt" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[1]="homalt" && BLT[0]="nocall" '+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="homalt" && BVT[1]="INDEL"'+" ' ",
    }
#
    data_config["INDEL_hetalt"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="INDEL" && BLT[0]="hetalt"'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BLT[0]="hetalt"'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[1]="hetalt"'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BVT[0]="INDEL" && BLT[0]="hetalt"'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && BLT[0]="hetalt" && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && BLT[1]="hetalt" && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BD[1]="FP" && BLT[1]="hetalt" && BVT[1]="INDEL"'+" ' ",
    } 
#
    data_config["INDEL_het_homalt"]={
    "TP": '-i'+" ' "+'BD[0]="TP" && BVT[0]="INDEL" && (BLT[0]="homalt" || BLT[0]="het")'+" ' ",
    "FN": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && (BLT[0]="het" || BLT[0]="homalt")'+" ' ", 
    "FP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && (BLT[1]="het" || BLT[1]="homalt")'+" ' ",
    "FNP": '-i'+" ' "+'BD[0]="FN" && BLT[1]="nocall" && BVT[0]="INDEL" && (BLT[0]="het" || BLT[0]="homalt")'+" ' ",
    "FNT": '-i'+" ' "+'BD[0]="FN" && BVT[0]="INDEL" && (BLT[0]="homalt" || BLT[0]="het") && BD[1]="FP" && BLT[1]!="nocall"'+" ' ",
    "FPP": '-i'+" ' "+'BD[1]="FP" && BVT[1]="INDEL" && (BLT[1]="het" || BLT[1]="homalt") && BLT[0]="nocall"'+" ' " ,
    "FPT": '-i'+" ' "+'BD[0]="FN" && BLT[0]!="nocall" && BVT[1]="INDEL" && BD[1]="FP" && (BLT[1]="het" || BLT[1]="homalt" )'+" ' ",
    }
    data_config["clinsv_bw"]= {
        "OPTIONS": "/data/annotations/Human/GRCh38/index/clinSV/1.0/refdata-b38",
        "lumpy": "5"

    }
    data_config["sambamba_merge_clinsv"]={
        "OPTIONS": "-t 4"
    }
    data_config["witty"]={
        "options": "-em"
    }
    full_path=base_bam +'/' + prefix_analysis +'/' + suffix_analysis + "/chr_*/*markdup.bam"
    print(full_path)
    liste = glob.glob(r'{}'.format(full_path))
    print(liste)
    data_config["bam_options"]={
        "paths":[i.split('.')[0] for i in liste]
    }


    json_obejct = json.dumps(data_config, indent = 4)
    with open(INPUT_PATH+"/pipeline_config/config.json",'w') as outfile:
        outfile.write(json_obejct)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Python script to create config file")
    parser.add_argument("-i","--input_path",help="Working directory", type = str, required= True)
    parser.add_argument("-o","--output_path",help="Output path", type =str, required= True)
    parser.add_argument("-s","--snakemake_rules_path",help="Snakemake rules path", type =str,required= True)
    parser.add_argument("-r","--reference_vcf_path",help="Gold standard VCF path for hap.py analysis hg001", type =str,required= False)
    parser.add_argument("-b","--bed_path",help="Gold standard Bed file path for hap.py analysis hg001", type =str,required= False)
    parser.add_argument("-f","--reference_fasta_path",help="Reference genome path for hap.py analysis", type =str,required= False)
    parser.add_argument("-e","--sample_path",help="Sample VCF path for hap.py analysis", type =str,required= False)
    parser.add_argument("-ref","--reference",help='Reference name e.g NA12878', type =str,required= True)
    parser.add_argument("-V","--Version",help="Variant calling pipeline verssion e.g 3.0.0", type =str,required= True)
    parser.add_argument("-R","--Run", help="Run Id",type =str,required= True)
    parser.add_argument("-A","--Alias",help="Alias", type =str,required= True)
    parser.add_argument("-T","--Target",help="Target e.g WGS", type =str,required= True)
    parser.add_argument("-D","--Disease",help="Disease e.g MR", type =str,required= True)
    parser.add_argument("-S","--Sample",help="Analysed sample name", type =str,required= True)
    parser.add_argument("-t","--Type",help="Type e.g index", type =str,required= True)
    parser.add_argument("-d","--Date",help="Analysis date e.g 01/01/2022", type =str,required= True)
    parser.add_argument("-an","--Analysis_name",help="analysis full name", type =str,required= True)
    parser.add_argument("-GSF","--Fasta_reference",help="Fasta file name",type =str,required= False)
    parser.add_argument("-GSB","--Gold_standard_bed",help="Bed File name hg001",type =str,required= False)
    parser.add_argument("-GSV","--Gold_standard_vcf",help="VCF Standard file name hg001",type =str,required= False)
    parser.add_argument("-od","--old_pipelines",help="Old pipelines summary results",type =str,nargs='+',required= False)
    parser.add_argument("-u","--user",help="S3 user name", type = str, required= True)
    parser.add_argument("-ip","--endpoint",help="path to json containing ip adresses", type = str, required= False)
    parser.add_argument("-bn","--bucket_name",help="S3 Bucket name", type = str, required= True)
    parser.add_argument("-bam","--bams_base", help="bam file base directory",type = str, required= False)
    parser.add_argument("-prefix","--prefix_analysis",help="bam files prefix", type = str, required= False)
    parser.add_argument("-suffix","--suffix_analysis",help="bam files suffix", type = str, required= False)
    parser.add_argument("-pvcfhg002","--vcfhg002_path",help="Standard vcf hg002", type = str, required= False)
    parser.add_argument("-nvcfhg002","--vcfhg002_name",help="standard hg002 VCf file name", type = str, required= False)
    parser.add_argument("-nbedhg002","--bedhg002_name",help="standard hg002 bed file name", type = str, required= False)
    parser.add_argument("-pbedhg002","--pbedhg002_path",help="standard hg002 bed file path", type = str, required= False)
    parser.add_argument("-query_sv_path","--vcf_query_sv_path",help="path to  vcf query for witty", type = str, required= True)
    parser.add_argument("-query_sv_name","--vcf_query_sv_name",help="query vcf name for witty", type = str, required= False)
    parser.add_argument("-Enviro","--Environnement",help="Calculation environment", type = str, required= True)
    parser.add_argument("-too","--tools", help="tool to run Hapy, ClinSV or Witty",type = str, required= True)





    args = parser.parse_args()
    create_json(args.input_path, args.output_path, args.snakemake_rules_path,
                args.reference_vcf_path, args.bed_path, args.reference_fasta_path, 
                args.sample_path,args.old_pipelines, args.reference,args.Version,args.Run,
                args.Alias, args.Target, args.Disease, args.Sample, args.Type, args.Date,
                args.Analysis_name,args.Fasta_reference,args.Gold_standard_bed,args.Gold_standard_vcf,args.user,args.endpoint,
                args.bucket_name,args.bams_base,args.prefix_analysis,args.suffix_analysis,
                args.vcfhg002_path,args.vcfhg002_name,args.pbedhg002_path,args.bedhg002_name,args.vcf_query_sv_path,args.vcf_query_sv_name,
                args.Environnement,args.tools)
    


