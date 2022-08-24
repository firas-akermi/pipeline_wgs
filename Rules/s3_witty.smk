#!/usr/bin/env python3
# Firas Akermi
rule s3_witty:
    input:
        i1= expand("{output_path}/{analysis}/Wittyer_{date}.tar.gz",output_path=output_path,analysis = full_name+Time,date=Time)
    output:
        "{output_path}/{analysis}_witty_{date}_done.txt"
    params:
        script = config["scripts"]["S3_hapy"],
        user = config["S3"]["USER"],
        adress_ip = config["S3"]["IP"],
        Bucket = config["S3"]["Bucket_name"],
        tar_name = lambda wildcards: "{}_{date}.tar.gz".format(wildcards.analysis,wildcards.date),
        key = lambda wildcards:"MR/Pipeline_{}/{}/".format(Version, config['general_information']["tool"])
    shell:
        '''
        python3 {params.script} -u {params.user} -ip {params.adress_ip}   -f {input.i1} -b {params.Bucket} -k {params.key} -n {params.tar_name} > {output}
        '''
