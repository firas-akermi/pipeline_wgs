#!/usr/bin/env python3
# Firas Akermi
rule compression_witty:
    input:
        i1= rules.witty.output,
        i2= rules.witty_csv.output.o,
    output:
        "{output_path}/{analysis}/Wittyer.tar.gz"
    shell:
        '''
        tar -czvf {output}  {input.i1}
        '''