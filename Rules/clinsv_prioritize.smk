#!/usr/bin/env python3
# Firas Akermi
rule clinsv_prioritize:
    input:
        bam = "{output_path}/{analysis}/CNV/{analysis}_merged.bam",
        annontate_flag = rules.clinsv_annotate.output,
        bw_path = rules.clinsv_bw.output.path
    output:
        vcf = "{output_path}/{analysis}/CNV/SV-CNV.vcf"
    params:
        lumpy = config["clinsv_bw"]["lumpy"],
        ref = config["clinsv_bw"]["OPTIONS"]       
       
    shell:
        '''
        clinsv -r prioritize -i "{input.bam}" -ref {params.ref} -p {wildcards.output_path}/{wildcards.analysis}/CNV/ -l {params.lumpy}
        cp {wildcards.output_path}/{wildcards.analysis}/CNV/SVs/joined/SV-CNV.vcf {output.vcf}
        '''