#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule Indexation_de_fichier_VCF_de_Benchmarking:
    input:
        "{output_path}/{analysis}/happy/{analysis}.vcf.gz"
    output:
        "{output_path}/{analysis}/happy/{analysis}.vcf.gz.tbi"
    shell:
        "tabix -f {input}" 