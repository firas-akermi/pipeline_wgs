#!/usr/bin/env python3
# Firas Akermi
rule info_extraction:
    input:
        VCF_hapy = expand("{input_path}/output/{sample}_hapy.vcf.gz",input_path=input_path,sample=full_name),
    output:
        tmp = "{input_path}/output/{sample}_hapy_inter.text",
        stat = "{input_path}/stats/{sample}_hapy_stats.csv",
    params:
        script = config["scripts"]["extract_script"]
    shell:'''
        python {params.script} --input {input.VCF_hapy} --output1 {output.tmp} --output2 {output.stat}
         '''
