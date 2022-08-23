#!/usr/bin/env python3
# Firas Akermi
rule clinsv_lumpy:
    input:
        path = rules.clinsv_bw.output.path,
        bam = "{output_path}/{analysis}/CNV/{analysis}_merged.bam"
    output:
         path = "{output_path}/{analysis}/CNV/lumpy/"
    params:
        lumpy = config["clinsv_bw"]["lumpy"],
        ref = config["clinsv_bw"]["OPTIONS"]
       
    shell:
        '''
        clinsv -r lumpy -i "{input.bam}" -ref {params.ref} -p {wildcards.output_path}/{wildcards.analysis}/CNV/ -l {params.lumpy}
        '''