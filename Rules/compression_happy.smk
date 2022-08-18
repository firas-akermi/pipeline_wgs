#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule compression_happy:
    input:
        i1= rules.write_hapy_to_csv.output.o,
        i2="{output_path}/{analysis}/happy/",
        i3=rules.stats_hapy_to_s3.output.o,
        i4=rules.Mise_en_forme_sous_format_csv.output

    output:
        "{output_path}/{analysis}/happy.tar.gz"
    shell:
        '''
        tar -czvf {output}  {input.i2}
        '''