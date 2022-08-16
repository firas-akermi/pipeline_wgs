#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Firas Akermi 
# 2022/05/09
# python3
#Script for creating snakemake config file 
from __future__ import unicode_literals
import json
import argparse
############
def create_json():
    cluster_config= {}
    cluster_config["__default__"] = {
    "name": "Validation pipeline hap.py",
    "tags": "snakemake,validation, MR, hap.py",
    "volume_snakemake": "snakemake",
    "volume_home": "home",
    "volume_annotations": "annotations",
    "volume_irods": "irods",
    "volume_scratch2": "scratch2",
    "cpu": 4,
    "mem": 5,
    "image": "sequoia-docker-tools/snakemake:3.9.0-4"
    }
    cluster_config["Compression_de_fichier_VCF"]={
    "name": "Compression_de_fichier_VCF",
    "tags": "snakemake,compression_bgzip_tabix",
    "cpu": 1,
    "mem": 1,
    "image": "sequoia-docker-tools/hap.py:0.3.10-3"
    }
    cluster_config["Indexation_de_fichier_VCF"]={
    "name": "Indexation_de_fichier_VCF",
    "tags": "snakemake,indexing_tabix",
    "cpu": 1,
    "mem": 1,
    "image": "sequoia-docker-tools/hap.py:0.3.10-3"
    }
    cluster_config["Comparaison_des_Haplotypes"]={
    "name": "Comparaison_des_Haplotypes",
    "tags": "snakemake,benchmarking_happy",
    "cpu": 25,
    "mem": 64,
    "image": "sequoia-docker-tools/hap.py:0.3.10-3"
    }
    cluster_config["Indexation_de_fichier_VCF_de_Benchmarking"]={
    "name": "Indexation_de_fichier_VCF_de_Benchmarking",
    "tags": "snakemake,indexing,hap.py,tabix",
    "cpu": 1,
    "mem": 1,
    "image": "sequoia-docker-tools/hap.py:0.3.10-3"
    }
    cluster_config["Analyse_de_variants"]={
    "name": "Analyse_de_variants",
    "tags": "snakemake,bcftools,happy",
    "cpu": 2,
    "mem": 4,
    "image": "sequoia-docker-tools/bcftools:1.9-1"
    }
    cluster_config["Extraction_des_informations"]={
    "name": "Extraction_des_informations",
    "tags": "snakemake,grep,bcftools,happy",
    "cpu": 2,
    "mem": 4,
    "image": "sequoia-docker-infra/debian:stretch"
    }
    cluster_config["Mise_en_forme_sous_format_csv"]={
        "name": "Mise_en_forme_sous_format_csv",
        "tags": "csv,mise_en_forme",
        "cpu": 2,
        "mem": 2,
        "image": "sequoia-docker-tools/snakemake:3.9.0-4"
    }
    cluster_config["Analyse_des_resultats_et_generation_du_rapport_html"]={
    "name": "Analyse_des_resultats_et_generation_du_rapport_html",
    "tags": "snakemake,hapy,resultat,html,visualisation",
    "cpu": 2,
    "mem": 4,
    "image": "sequoia-docker-tools/happy_validation:1.0.0"
    }
    json_obejct = json.dumps(cluster_config, indent =4)
    with open("/scratch2/tmp/fakermi/pipeline_validation_happy/cluster_config/cluster_config.json",'w') as outfile:
        outfile.write(json_obejct)
    
if __name__ == '__main__':
    create_json()
    


