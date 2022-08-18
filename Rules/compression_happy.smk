#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule compression_happy:
    input:
        i1= rules.write_hapy_to_csv.output.o,
        i2="{output_path}/{analysis}/happy/"

    output:
        "{output_path}/{analysis}/happy.tar.gz"
    shell:
        '''
        tar -czvf {output}  {input.i2}
        '''