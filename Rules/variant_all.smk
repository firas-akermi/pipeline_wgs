#!/usr/bin/env python3
# Firas Akermi
rule Analyse_de_variants:
  input:
    i1=expand("{output_path}/{analysis}/happy/{analysis}.vcf.gz", output_path=output_path,analysis=full_name+Time),
    i2=expand("{output_path}/{analysis}/happy/{analysis}.vcf.gz.tbi", output_path=output_path,analysis=full_name+Time),
  output:
    temp("{output_path}/{analysis}/happy/{variant}/{score}.vcf"),
  params:
    x = lambda wildcards: config["{}".format(wildcards.variant)]["{}".format(wildcards.score)],
  shell:
    '''
    bcftools view -Ov -s TRUTH,QUERY {params.x} {input.i1}  > {output}
    '''             
                     
            
