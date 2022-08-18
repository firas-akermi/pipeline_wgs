#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Firas Akermi 
# 2022/05/09
# python3
#Script for creating snakemake config file 
from __future__ import unicode_literals
from datetime import datetime
import json
import os
import argparse
import sys
import glob
############
data_config= {}
data_config["general_path"]={
    "INPUT_PATH": "/scratch2/tmp/fakermi/pipeline_validation_happy",
    "OUTPUT_PATH": "/scratch2/tmp/fakermi/pipeline_validation_happy/data",
    "SNAKEMAKE_RULES": "/scratch2/tmp/fakermi/pipeline_validation_happy/Rules",
    "REFERENCE_VCF_Path": "/scratch2/tmp/vsaillour/reference/GIAB_reference_NA12878_HG001_GRCh38/edit_chr_vs",
    "BED_Path": "/scratch2/tmp/vsaillour/reference/GIAB_reference_NA12878_HG001_GRCh38/edit_chr_vs",
    "Fasta_Path": "/data/annotations/Human/GRCh38/index/sorted_primary_assemblies",
    "Sample_Path": "/scratch2/tmp/fakermi/"}
data_config["general_information"]={
        "Description": "This script creates a config file for variant calling validation",
        "Run": "A00666",
        "Alias": "0012",
        "Target": "WGS",
        "Disease": "MR",
        "Sample": "FS00505001",
        "Type": "index",
        "Date": "21042022",
        "Version": "v3.3.1",
        "Full_name": "A00666_0012_WGS_MR_FS00505001_index_21042022_final",
        "Reference": "grch38",
        "Fasta_reference": "GRCh38.92",
        "Bed_file_name": "HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7",
        "VCF_reference": "HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer"
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
        ]
    }
data_config["scripts"]={
        "extract_script": "/scratch2/tmp/fakermi/pipeline_validation_happy/script/extraction.py",
        "create_form": "/scratch2/tmp/fakermi/pipeline_validation_happy/script/create_report.py"
    }
data_config["SNP_INDEL_ALL"]={
        "TP": "-i ' BD[0]=\"TP\" ' ",
        "FN": "-i ' BD[0]=\"FN\" ' ",
        "FP": "-i ' BD[1]=\"FP\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" ' "
}
data_config["SNP_INDEL_het"]={
        "TP": "-i ' BD[0]=\"TP\" && BLT[0]=\"het\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BLT[0]=\"het\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BLT[1]=\"het\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"het\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BLT[0]=\"het\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BLT[1]=\"het\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"het\" ' "
}
data_config["SNP_INDEL_homalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BLT[0]=\"homalt\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BLT[0]=\"homalt\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BLT[1]=\"homalt\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"homalt\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BLT[0]=\"homalt\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BLT[1]=\"homalt\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"homalt\" ' "
}
data_config["SNP_INDEL_hetalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BLT[0]=\"hetalt\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BLT[0]=\"hetalt\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BLT[1]=\"hetalt\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"hetalt\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BLT[0]=\"hetalt\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BLT[1]=\"hetalt\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"hetalt\" ' "
}
data_config["SNP_INDEL_het_homalt"]={
        "TP": "-i ' BD[0]=\"TP\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") ' ",
        "FN": "-i ' BD[0]=\"FN\" && (BLT[0]=\"het\" || BLT[0]=\"homalt\") ' ",
        "FP": "-i ' BD[1]=\"FP\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\") ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && (BLT[0]=\"het\" || BLT[0]=\"homalt\") ' ",
        "FNT": "-i ' BD[0]=\"FN\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\") && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && (BLT[1]=\"het\"|| BLT[1]=\"homalt\" ) ' "
}
data_config["SNP_ALL"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"SNP\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BVT[0]=\"SNP\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BVT[1]=\"SNP\" ' "
}
data_config["SNP_het"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"SNP\" && BLT[0]=\"het\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BLT[0]=\"het\" && BVT[0]=\"SNP\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && BLT[1]=\"het\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"het\" && BVT[0]=\"SNP\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" && BLT[0]=\"het\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" && BLT[0]=\"het\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"het\" && BVT[1]=\"SNP\" ' "
}
data_config["SNP_homalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"SNP\" && BLT[0]=\"homalt\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BLT[0]=\"homalt\" && BVT[0]=\"SNP\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && BLT[1]=\"homalt\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"homalt\" && BVT[0]=\"SNP\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" && BLT[0]=\"homalt\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && BLT[1]=\"homalt\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"homalt\" && BVT[1]=\"SNP\" ' "
}
data_config["SNP_hetalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"SNP\" && BLT[0]=\"hetalt\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BLT[0]=\"hetalt\" && BVT[0]=\"SNP\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && BLT[1]=\"hetalt\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"hetalt\" && BVT[0]=\"SNP\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" && BLT[0]=\"hetalt\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && BLT[1]=\"hetalt\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"hetalt\"&& BVT[1]=\"SNP\" ' "
}
data_config["SNP_het_homalt"]= {
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"SNP\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") ' ",
        "FN": "-i ' BD[0]=\"FN\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") && BVT[0]=\"SNP\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\") ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") && BVT[0]=\"SNP\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"SNP\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"SNP\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\") && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\" ) && BVT[1]=\"SNP\" ' "
}
data_config["INDEL_ALL"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"INDEL\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BVT[0]=\"INDEL\"  ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BVT[1]=\"INDEL\" ' "
}
data_config["INDEL_het"]= {
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"INDEL\" && BLT[0]=\"het\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BLT[0]=\"het\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[1]=\"het\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BLT[0]=\"het\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BLT[0]=\"het\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[1]=\"het\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"het\" && BVT[1]=\"INDEL\" ' "
}
data_config["INDEL_homalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"INDEL\" && BLT[0]=\"homalt\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BLT[0]=\"homalt\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[1]=\"homalt\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BVT[0]=\"INDEL\" && BLT[0]=\"homalt\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BLT[0]=\"homalt\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[1]=\"homalt\" && BLT[0]=\"nocall\"  ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"homalt\" && BVT[1]=\"INDEL\" ' "
    }
data_config["INDEL_hetalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"INDEL\" && BLT[0]=\"hetalt\" ' ",
        "FN": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BLT[0]=\"hetalt\" ' ",
        "FP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[1]=\"hetalt\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BVT[0]=\"INDEL\" && BLT[0]=\"hetalt\" ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && BLT[0]=\"hetalt\" && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && BLT[1]=\"hetalt\" && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && BLT[1]=\"hetalt\" && BVT[1]=\"INDEL\" ' "
}
data_config["INDEL_het_homalt"]={
        "TP": "-i ' BD[0]=\"TP\" && BVT[0]=\"INDEL\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") ' ",
        "FN": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && (BLT[0]=\"het\" || BLT[0]=\"homalt\") ' ",
        "FP": "-i ' BD[1]=\"FP\" ' ",
        "FNP": "-i ' BD[0]=\"FN\" && BLT[1]=\"nocall\" && BVT[0]=\"INDEL\" && (BLT[0]=\"het\" || BLT[0]=\"homalt\") ' ",
        "FNT": "-i ' BD[0]=\"FN\" && BVT[0]=\"INDEL\" && (BLT[0]=\"homalt\" || BLT[0]=\"het\") && BD[1]=\"FP\" && BLT[1]!=\"nocall\" ' ",
        "FPP": "-i ' BD[1]=\"FP\" && BVT[1]=\"INDEL\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\") && BLT[0]=\"nocall\" ' ",
        "FPT": "-i ' BD[0]=\"FN\" && BLT[0]!=\"nocall\" && BD[1]=\"FP\" && (BLT[1]=\"het\" || BLT[1]=\"homalt\" ) ' "
}
json_obejct = json.dumps(data_config, indent =4)
with open("/scratch2/tmp/fakermi/pipeline_validation_happy/pipeline_config/config.json",'w') as outfile:
    outfile.write(json_obejct)
