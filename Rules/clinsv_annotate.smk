#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule clinsv_annotate:
    input:
        bam = "{output_path}/{analysis}/CNV/{analysis}_merged.bam",
        cnvnator_path = rules.clinsv_cnvnator.output.path,
        bw_path = rules.clinsv_bw.output.path,
        lumpy_path = rules.clinsv_lumpy.output.path
    output:
         path = "{output_path}/{analysis}/CNV/annotate/"
    params:
        lumpy = config["clinsv_bw"]["lumpy"],
        ref = config["clinsv_bw"]["OPTIONS"]       
       
    shell:
        '''
        clinsv -r annotate -i "{input.bam}" -ref {params.ref} -p {wildcards.output_path}/{wildcards.analysis}/CNV/ -l {params.lumpy}
        '''