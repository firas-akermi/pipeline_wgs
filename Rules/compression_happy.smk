#!/usr/bin/env python3
# Firas Akermi
rule compression_happy:
    input:
        i1= rules.Analyse_des_resultats_et_generation_du_rapport_html.output.o1,
        i2= rules.Analyse_des_resultats_et_generation_du_rapport_html.output.o2,
        i3= rules.write_hapy_to_csv.output.o,
        14 = rules.stats_hapy_to_s3.output
    output:
        "{output_path}/{analysis}/happy.tar.gz"
    shell:
        '''
        tar -czvf {output}  {input.i2}
        '''