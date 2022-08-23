#!/usr/bin/env python3
# Firas Akermi
rule Compression_de_fichier_VCF:
    input:
        expand("{sample_path}/{analysis}.vcf",sample_path=Sample_Path,analysis=full_name)
    output:
        "{output_path}/{analysis}/{analysis}.vcf.gz"      
    shell:
        "bgzip -c {input} > {output}" 


