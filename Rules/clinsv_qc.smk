#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule clinsv_qc:
    input:
        bam = "{output_path}/{analysis}/CNV/{analysis}_merged.bam",
        vcf = "{output_path}/{analysis}/CNV/SV-CNV.vcf",
        bw_path = rules.clinsv_bw.output.path
    output:
        vcf = "{output_path}/{analysis}/CNV/results"
    params:
        lumpy = config["clinsv_bw"]["lumpy"],
        ref = config["clinsv_bw"]["OPTIONS"]       
       
    shell:
        '''
        clinsv -r qc -eval -i "{input.bam}" -ref {params.ref} -p {wildcards.output_path}/{wildcards.analysis}/CNV/ -l {params.lumpy}
        '''