#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule Comparaison_des_Haplotypes:
       input:
            VCF_Query = expand("{output_path}/{analysis}/{analysis}.vcf.gz", output_path=output_path,  analysis=full_name), 
            VCF_index = expand("{output_path}/{analysis}/{analysis}.vcf.gz.tbi", output_path =output_path,  analysis=full_name), 
            Fasta= expand("{fasta_path}/{fasta_file}.fa", fasta_path=Fasta_Path, fasta_file = fasta_file_name), 
            GIAB_vcf = expand("{ref_vcf_path}/{ref_vcf}.vcf.gz", ref_vcf_path = REFERENCE_VCF_Path,  ref_vcf = ref_vcf_name), 
            GIAB_bed = expand("{ref_bed_path}/{ref_bed}.bed",  ref_bed_path = BED_Path,  ref_bed = bed_file_name)
       output:
            "{output_path}/{analysis}/happy/{analysis}.vcf.gz"
   
       params:
            output_dir="{output_path}/{analysis}/happy/{analysis}"
           
#       conda: "py2env.yml"

       shell:
          '''
          export HGREF={input.Fasta}; 
          hap.py {input.GIAB_vcf} {input.VCF_Query} -f {input.GIAB_bed} -r {input.Fasta} -o {params.output_dir} --write-vcf 
          '''

