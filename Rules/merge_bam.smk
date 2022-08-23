#!/usr/bin/env python3
# Firas Akermi
rule merge_bam:
    input: 
        expand("{bam_file}.bam",bam_file = bam_files)
    output:
        "{output_path}/{analysis}/CNV/{analysis}_merged.bam"
    params:
        option = config["sambamba_merge_clinsv"]["OPTIONS"]
    shell:'''
        sambamba merge {params.option} {output} {input}
        '''

