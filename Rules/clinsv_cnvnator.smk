#!/usr/bin/env python3
# Firas Akermi
rule clinsv_cnvnator:
    input:
        bam = "{output_path}/{analysis}/CNV/{analysis}_merged.bam",
        bw_path = rules.clinsv_bw.output.path,
        lumpy_path= rules.clinsv_lumpy.output.path
    output:
         path = "{output_path}/{analysis}/CNV/cnvnator/"
    params:
        lumpy = config["clinsv_bw"]["lumpy"],
        ref = config["clinsv_bw"]["OPTIONS"]       
       
    shell:
        '''
        clinsv -r cnvnator -i "{input.bam}" -ref {params.ref} -p {wildcards.output_path}/{wildcards.analysis}/CNV/ -l {params.lumpy}
        '''