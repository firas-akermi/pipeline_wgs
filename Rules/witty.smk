#!/usr/bin/env python3
# Firas Akermi
rule witty:
    input:
        vcf_ref= expand('{vcf_hg002_path}/{vcf_file_name}.vcf.gz',vcf_hg002_path=sv_vcf_path,vcf_file_name=sv_vcf_name),
        bed=expand('{bed_hg002_path}/{bed_file_name}.bed',bed_hg002_path=sv_bed_path,bed_file_name=sv_bed_name),
        vcf_query= expand("{query_path}/{query_name}.vcf",query_path=vcf_sv_query_path,query_name=vcf_sv_query_name)
    output:
        "{output_path}/{analysis}/Witty/"
    params:
        option=config["witty"]["options"]
    shell:
        '''
        /opt/Wittyer/Wittyer -i {input.vcf_query} -t {input.vcf_ref} {params.option} -b {input.bed} -o {output}
        '''

