#!/usr/bin/env python3
# Firas Akermi
rule compression_happy:
    input:
        i1= rules.write_hapy_to_csv.output.o,
        i2 = rules.stats_hapy_to_s3.output
    output:
        "{output_path}/{analysis}/happy.tar.gz"
    shell:
        '''
        tar -czvf {output}  -C {wildcards.output_path}/{wildcards.analysis}/ happy
        '''