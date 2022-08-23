#!/usr/bin/env python3
# Firas Akermi
rule Indexation_de_fichier_VCF:
    input:
        "{output_path}/{analysis}/{analysis}.vcf.gz"
    output:
        "{output_path}/{analysis}/{analysis}.vcf.gz.tbi"
    shell:
        "tabix -f {input} > {output}" 


