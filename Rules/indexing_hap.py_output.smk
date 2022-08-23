#!/usr/bin/env python3
# Firas Akermi
rule Indexation_de_fichier_VCF_de_Benchmarking:
    input:
        "{output_path}/{analysis}/happy/{analysis}.vcf.gz"
    output:
        "{output_path}/{analysis}/happy/{analysis}.vcf.gz.tbi"
    shell:
        "tabix -f {input}" 