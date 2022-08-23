#!/usr/bin/env python3
# Firas Akermi
rule compression_clinsv:
    input:
        i1= rules.clinsv_qc.output.vcf,
        i2= "{output_path}/{analysis}/CNV/"
    output:
        "{output_path}/{analysis}/ClinSV.tar.gz"
    shell:
        '''
        tar --exclude= {input.i2}*.bam --exclude= {input.i2}*.bai -czvf {output}  {input.i2}
        '''