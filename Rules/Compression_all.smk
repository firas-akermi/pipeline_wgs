#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule compression:
    input:
        i1="{output_path}/{analysis}/",
        i2=rules.Analyse_des_resultats_et_generation_du_rapport_html.output.o1,
        i3=rules.clinsv_qc.output.vcf
    output:
        "{output_path}/{analysis}/{analysis}_all.tar.gz"
    shell:'''
        tar -czvf {output} {input.i1}
        '''