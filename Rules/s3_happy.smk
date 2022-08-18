#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule s3_happy:
    input:
        i1= rules.compression_happy.output,
    output:
        "{output_path}/{analysis}_happy_done.txt"
    params:
        script = config["scripts"]["S3_hapy"],
        user = config["S3"]["USER"],
        adress_ip = config["S3"]["IP"],
        Bucket = config["S3"]["Bucket_name"],
        tar_name = lambda wildcards: "{}.tar.gz".format(wildcards.analysis),
        key = lambda wildcards:"MR/Pipeline_{}/{}/".format(Version, config['general_information']["tool"])
    shell:
        '''
        python3 {params.script} -u {params.user} -ip {params.adress_ip}   -f {input.i1} -b {params.Bucket} -k {params.key} -n {params.tar_name} > {output}
        '''
