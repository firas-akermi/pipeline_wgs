# Pipeline de validation de détection de variant

Ce pipeline permet d'effectuer la validation de detection des variants (SNP,INDEL et SV) en utilisant 3 outils:
 [Hap.py](https://github.com/Illumina/hap.py) pour les SNPs et les INDELs
 [ClinSV](https://github.com/KCCG/ClinSV) et [Wittyer](https://github.com/Illumina/witty.er) pour les SVs.

 Le pipeline lance l'analyse selon l'outil spécifié dans le fichier config:
 Le nom de l'outil(tool) doit être mentionné dans le fichier config soit "Hap.py" ou "ClinSV" ou "Witty" pour Witty.er.
# I. Création du fichier config
 Le script argconfig_json.py permet de créer le fichier json de configuration de pipeline:
 La discription des arguments est disponible en entrant la commande suivante:
```
python3 argconfig_json.py -h
```
# I.1. Arguments obligatoires pour tous les outils

|Arguments obligatoires|  Description|                  Exemple|
|:----:|:----:|:----:|
|-i|input path|/scratch3/spim-preprod/pipeline_validation_wgs|
|-o|output path|/scratch3/spim-preprod/pipeline_validation_wgs/data|
|-s|Rules path|/scratch3/spim-preprod/pipeline_validation_wgs/Rules|
|-Enviro|Execution environment|scratch3|
|-tool|tool to launch|Hap.py|
|-ref|reference|NA12878|
|-V|version|3.3.1|
|-R|Run id|A00666|
|-A|Alias|0012|
|-T|Target|WGS|
|-D|Disease|MR|
|-S|Sample id|FS00505001|
|-t|type|index|
|-d|date|21/04/2022|
|-an|Full analysis name|A00666_0012_WGS_MR_FS00505001_index_21042022_final|
|-u|S3 user name|spim-dev|
|-ip|path to json_ip|/data/snakemake/spim-dev/boto/endpoint.json|
|-bn|S3 Bucket name|validation|

## I.2. Arguments spécifiques à Hap.py

|Arguments|   Description|    Exemple|
|:----:|:----:|:----:|
|-r|gold standard vcf path|/data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2|
|-b|gold standard bed path|/data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2|
|-e|vcf sample path|/scratch2/tmp/fakermi|
|-f|fasta path|/data/annotations/Human/GRCh38/index/sorted_primary_assemblies|
|-GSF|fasta file name|GRCh38.92|
|-GSB|standard bed file name|HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7|
|-GSV|standard vcf file name|HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer|

## I.3. Arguments spécifiques à Witty.er
Arguments|   Description|     Exemple|
|:----:|:----:|:----:|
|-pvcfhg002|Standard vcf hg002|/data/annotations/Human/hg38/references/NA24385_HG002/NISTv4.2.1|
|-nvcfhg002|standard hg002 VCf file name|HG002_GRCh38_1_22_v4.2.1_benchmark|
|-nbedhg002|standard hg002 bed file name|HG002_GRCh38_1_22_v4.2.1_benchmark_noinconsistent|
|-pbedhg002|standard hg002 bed file path|/data/annotations/Human/hg38/references/NA24385_HG002/NISTv4.2.1|
|-query_sv_path|path to  vcf query for witty|/scratch2/tmp/vsaillour/tmp/20220704_wittyer_test/A00666_0012_WGS_MR_FS00505001_index_21042022|
|-query_sv_name|query vcf name for witty|A00666_0012_WGS_MR_FS00505001_index_21042022_SV-CNV|

## I.4. Arguments spécifiques à ClinSV
Arguments|    Description|      Exemple|
|:----:|:----:|:----:|
|-bam|bam files base directory|/scratch3/spim-preprod/pipeline_trio_wgs/data|
|-prefix|bam files subdirectory|A00666_0012_WGS_MR_FS00505001_21042022|
|-suffix|bam files directory|FS00505001_S6|



# I.5. Remarques:

 Il ne faut pas spécifier les extensions des fichiers: Si on a un fichier Name.vcf.gz on donne uniquement le nom du fichier dans ce cas (Name), de même pour toutes les autres extensions (e.g bam,fa,bed...). 


 Il ne faut pas aussi ajouter un "/" à la fin d'un chemin d'accés d'un fichier: si on a un chemin "/path/to/folder/" il faut éliminer le dernier "/" -----> "/path/to/folder"


# I.6. Exemple de création du fichier config:
Ouvrir [Godocker]()

Copier la commande ci-dessous en modifiant les arguments en fonction de l'analyse souhaitée.

Sélectionner une image docker : sequoia-docker-tools/snakemake:3.9.0-4

Sélectionner les volumes: snakemake, scratch2, scratch3, home

Cliquer "Submit"

```
#!/bin/bash

python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \ 
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules\ 
-r /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-b /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-f /data/annotations/Human/GRCh38/index/sorted_primary_assemblies \
-e [Sample VCF path for hap.py analysis] \
-ref [Reference name e.g NA12878] \
-V [ Variant calling pipeline verssion e.g 3.0.0] \
-R [Run Id] -A [ALIAS] -T [Target e.g WGS] \
-D [ Disease e.g MR] -S [Analysed sample id] \
-t [Type e.g index] \
-d [  Analysis date e.g 01/01/2022] \
-an [analysis full name] -GSF GRCh38.92 \
-GSB HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7 \
-GSV HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer \
-u [user_s3] \
-ip /data/snakemake/spim-dev/boto/endpoint.json \
-bn validation -n A00666_0012_WGS_MR_FS00505001_index_21042022_final.tar.gz \
-bam /scratch3/spim-preprod/pipeline_trio_wgs/data \
-prefix A00666_0012_WGS_MR_FS00505001_21042022 \
-suffix FS00505001_S6 -pvcfhg002 /data/annotations/Human/hg19/references/NA24385_HG002/NIST_SV_v0.6 \
-nvcfhg002 HG002_SVs_Tier1_v0.6 \
-nbedhg002 HG002_SVs_Tier1_v0.6 \
-pbedhg002 /data/annotations/Human/hg19/references/NA24385_HG002/NIST_SV_v0.6 \
-query_sv_path [path to vcf query for witty] \
-query_sv_name [query vcf name for witty] \
-Enviro [Calculation environment] \
-tool [tool to run: Hap.py, ClinSV or Witty]
```
# II. Exécution du pipeline(go_docker)

# II.1. Mount volumes :
-scratch2

-scratch3

-irods

-home

-snakemake

# II.2. Images:
sequoia-docker-tools/snakemake:3.9.0-4
CPU: 4
RAM: 5

# II.3. Commande:
Copier la commande ci-dessous dans go-docker en sécifiant les paramètres entre crochés 
```
#!/bin/bash

set -o pipefail;
/data/snakemake/miniconda3/envs/snakemake/bin/snakemake \
-s [Path to snakefile] \
-k --rerun-incomplete  \
--configfile [Path to pipeline_config file] \
--cluster-config [path to cluster config file] \
--cluster 'godjob.py create -n {cluster.name}_[sample_id] -t {cluster.tags} --external_image -v {cluster.volume_snakemake} -v {cluster.volume_home} -v {cluster.volume_scratch2} -v {cluster.volume_irods}  -v {cluster.volume_annotations} -c {cluster.cpu} -r {cluster.mem} -i {cluster.image} -s' \
-j 40 -w 60 2>&1 | tee [path of log file]/pipeline_validation_wgs.log
```
# II.4. AWS_S3

 Le pipeline permet la compression et le stockage des résultats sur aws_S3,après chaque analyse. Pour cela la [configuration](https://docs.aws.amazon.com/fr_fr/cli/latest/userguide/cli-configure-files.html) de S3 doit être spécifiée sous :
```
/home/.aws/credentials
```


 