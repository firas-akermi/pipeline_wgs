#!/usr/bin/env python3
# Firas Akermi
rule clinsv_bw:
    input:
        bam = "{output_path}/{analysis}/CNV/{analysis}_merged.bam",
        ped= rules.generate_ped.output.ped
    output:
         path = "{output_path}/{analysis}/CNV/bw/",
         SV = "{output_path}/{analysis}/CNV/bw/SVs/"
    params:
        lumpy = config["clinsv_bw"]["lumpy"],
        ref = config["clinsv_bw"]["OPTIONS"]       
       
    shell:
        '''
        clinsv -r bigwig -i "{input.bam}" -ref {params.ref} -p {wildcards.output_path}/{wildcards.analysis}/CNV/ -l {params.lumpy}
        '''
