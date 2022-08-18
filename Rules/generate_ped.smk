#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule generate_ped:
    input:
        "{output_path}/{analysis}/CNV/{analysis}_merged.bam"
    output:
        ped = "{output_path}/{analysis}/CNV/sampleInfo.ped"
    shell:
        '''
        echo -e "Fam001\t1\t0\t0\t2\t0" > {output.ped}
        '''