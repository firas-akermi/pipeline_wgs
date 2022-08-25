# Pipeline de validation de détection des variants

L’évaluation qualitative d’un pipeline d’appel de variants consiste, pour SeqOIA-IT, à évaluer si un pipeline est suffisamment sensible et précis.
Ce pipeline de validation de détection de variants permet de mesurer la sensibilité et la précision d’une version de pipeline données (MR).

Les mesures de sensibilité et de précision sont possibles grâce à une comparaison de deux listes de variants.
Les variants provenant d’une expérience SeqOIA (QUERY) sont comparés à une liste de variants de référence (TRUTH). Cette comparaison permet de distribuer les variants de l’expérience essentiellement en trois catégories :

- **VP** : Vrais Positifs (variants détectés dans l’expérience et également présents dans le VCF de référence) ,

- **FN** : Faux Négatifs (variants NON détectés dans l’expérience alors qu’ils sont présents dans le VCF de référence) ,

- **FP** : Faux Positifs (variants détectés dans l’expérience alors qu’ils sont absents dans le VCF de référence).

Trois méthodes sont intégrées au pipeline de validation :

- L’utilitaire [Hap.py](https://github.com/Illumina/hap.py), Illumina qui est dédié aux calculs de sensibilité et de précision des SNPs et les DELINS (<50bp)

- L’utilitaire [Witty.er](https://github.com/Illumina/witty.er), Illumina qui est dédié aux calculs de sensibilité et de précision des Svs

- L’utilitaire [ClinSV](https://github.com/KCCG/ClinSV).


Le pipeline de validation de détection de variants est accessible depuis scratch3, sous /scratch3/spim-preprod/pipeline_validation_wgs/

L’exécution pipeline de validation  se découpe en 2 étapes :
1. Création du fichier config
2. Evaluation qualitative du pipeline d’appel de variants à partir du fichier config
# Installation et nom d’utilisateur

Le pipeline de validation de détection de variants est installé sous scratch3, et accessible sous  /scratch3/spim-preprod/pipeline_validation_wgs

Le nom d’utilisateur qui exécute le pipeline est spim-preprod

Pour cloner le pipeline de validation (sous  scratch3), faire :
```
git clone https://github.com/firas-akermi/pipeline_wgs.git
```

# Les préalables (à l’exécution du pipeline)
### Connexion à  GO-DOCKER DEV

- Ouvrir l’interface web [GO-DOCKER DEV](bio4g-god-dev.bbs.aphp.fr).
- Se connecter avec le nom d’utilisateur spim-dev.
- Mot de passe : contacter l’administrateur-système de SeqOIA-IT.

### Ouverture d’un Terminal sous scratch3
Sous un Terminal,  et en tant qu’utilisateur spim-preprod, naviguer jusqu’au répertoire du pipeline

# Création du fichier config via GO-DOCKER
L’exécution du script argconfig_json.py permet de créer le fichier .json de configuration de pipeline.
Le fichier de configuration permet de décrire, notamment,  la méthode de comparaison de variants (Hap.py, Witty.er, ou ClinSV), qui sera à utiliser, dans un second temps, par le pipeline de validation.


La ligne de commande du script argconfig_json.py prends en compte un ensemble de paramètres :

- une liste d’arguments obligatoires pour tous les outils complétée par une liste spécifique de la méthode de comparaison de variants choisie (Hap.py, Witty.er, ou ClinSV).
### Arguments obligatoires pour tous les outils

|Arguments obligatoires|  Description|                  Exemple|
|:----:|:----:|:----:|
|-i|input path|/scratch3/spim-preprod/pipeline_validation_wgs|
|-o|output path|/scratch3/spim-preprod/pipeline_validation_wgs/data|
|-s|Rules path|/scratch3/spim-preprod/pipeline_validation_wgs/Rules|
|-Enviro|Execution environment|scratch3|
|-tool|tool to launch|Hap.py or Witty or ClinSV|
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
|-bn|S3 Bucket name|validation|

### Arguments spécifiques à Hap.py

|Arguments|   Description|    Exemple|
|:----:|:----:|:----:|
|-r|gold standard vcf path|/data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2|
|-b|gold standard bed path|/data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2|
|-e|vcf sample path|/scratch2/tmp/fakermi|
|-f|fasta path|/data/annotations/Human/GRCh38/index/sorted_primary_assemblies|
|-GSF|fasta file name|GRCh38.92|
|-GSB|standard bed file name|HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7|
|-GSV|standard vcf file name|HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer|

### Arguments spécifiques à Witty.er
Arguments|   Description|     Exemple|
|:----:|:----:|:----:|
|-pvcfhg002|Standard vcf hg002|/data/annotations/Human/hg38/references/NA24385_HG002/NISTv4.2.1|
|-nvcfhg002|standard hg002 VCf file name|HG002_GRCh38_1_22_v4.2.1_benchmark|
|-nbedhg002|standard hg002 bed file name|HG002_GRCh38_1_22_v4.2.1_benchmark_noinconsistent|
|-pbedhg002|standard hg002 bed file path|/data/annotations/Human/hg38/references/NA24385_HG002/NISTv4.2.1|
|-query_sv_path|path to  vcf query for witty|/scratch2/tmp/vsaillour/tmp/20220704_wittyer_test/A00666_0012_WGS_MR_FS00505001_index_21042022|
|-query_sv_name|query vcf name for witty|A00666_0012_WGS_MR_FS00505001_index_21042022_SV-CNV|
|-em|evaluation mode|SimpleCounting|

### Arguments spécifiques à ClinSV
Arguments|    Description|      Exemple|
|:----:|:----:|:----:|
|-bam|bam files base directory|/scratch3/spim-preprod/pipeline_trio_wgs/data|
|-prefix|bam files subdirectory|A00666_0012_WGS_MR_FS00505001_21042022|
|-suffix|bam files directory|FS00505001_S6|



### Remarques:

1. A propos des valeurs spécifiques des noms de fichiers : les extensions des fichiers ne doivent pas être précisées (e.g : .vcf.gz, .bam, .fa, .bed, ...). Par exemple, pour mentionner le fichier name.vcf.gz dans le fichier de configuration, la valeur name est utilisée (l’extension .vcf.gz est volontairement omise).
2. A propos des valeurs spécifiques des chemins de dossiers : le dernier dossier du chemin ne doit pas être suivi du « / ».
Par exemple, pour mentionner le chemin « /path/to/folder/ » la valeur du paramètre est à décrire selon  « /path/to/folder »


# Exemples de ligne de commande

### 1. Exemple de ligne de commande (de création du fichier config) en vue d’une méthode de comparaison de variants via Hap.py
```
#!/bin/bash

python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules \
-Enviro scratch3 \
-tool Hap.py \
-ref NA12878 \
-V 3.3.1 \
-R A00666 \
-A 0012 \
-T WGS \
-D MR \
-S FS00505001 \
-t index \
-d 22/08/2022 \
-an A00666_0012_WGS_MR_FS00505001_index_21042022_final \
-u spim-preprod \
-bn validation  \
-r /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-b /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-e /scratch2/tmp/shared_files_tmp/spim \
-f /data/annotations/Human/GRCh38/index/sorted_primary_assemblies \
-GSF GRCh38.92 \
-GSB HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7 \
```
### 2. Exemple de ligne de commande (de création du fichier config) en vue d’une méthode de comparaison de variants via Witty.er

```
#!/bin/bash

python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules \
-Enviro scratch3 \
-tool Witty \
-ref NA12878 \
-V 3.3.1 \
-R A00666 \
-A 0012 \
-T WGS \
-D MR \
-S FS00505001 \
-t index \
-d 22/08/2022 \
-an A00666_0012_WGS_MR_FS00505001_index_21042022_final \
-u spim-preprod \
-bn validation  \
-pvcfhg002 /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-nvcfhg002 HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer \
-nbedhg002 HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7 \
-pbedhg002 /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-query_sv_path [path to vcf query for witty] \
-query_sv_name [query vcf name for witty] \
-em SimpleCounting

```
###  3. Exemple de ligne de commande (de création du fichier config) en vue d’une méthode de comparaison de variants via ClinSV

```
#!/bin/bash
python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules \
-Enviro scratch3 \
-tool ClinSV \
-ref NA12878 \
-V 3.3.1 \
-R A00666 \
-A 0012 \
-T WGS \
-D MR \
-S FS00505001 \
-t index \
-d 22/08/2022 \
-an A00666_0012_WGS_MR_FS00505001_index_21042022_final \
-u spim-preprod \
-bn validation  \
-bam /scratch3/spim-preprod/pipeline_trio_wgs/data \
-prefix A00666_0012_WGS_MR_FS00505001_21042022 \
-suffix FS00505001_S6 \
```
## Procédure:
1. Ouvrir l’interface web GO-DOCKER DEV (usager : spim-preprod) – voir paragrahe Connexion à  GO-DOCKER DEV
2. Créer un nouvelle tâche (cliquer sur « Create job »)
3. Remplir :
    - **Name** : argconfig_json (nom laissé libre selon la préférence de l’utilisateur)
    - **Container image** : sequoia-docker-tools/snakemake:3.9.0-4
    - **Command** : écrire la ligne de commande en s’aidant du tableau de description des arguments obligatoires  et de celui spécifique de la méthode de comparaison de variants (Hap.py, Witty.er, ou ClinSV) ; les exemples proposés sont également de bons supports.
    - **CPU requirements** : 1
    - **RAM requirements** (Gb) : 1
    - **Mount volumes** : snakemake, scratch2, scratch3, home
4. Finalement, cliquer sur le bouton "Submit".


## Modèle de ligne de commande
# Evaluation Qualitative d’un pipeline d’appel de variants via GO-DOCKER
Cette étape permet d’initialiser la méthode de comparaison de variants via les utilitaires Hap.py, Witty.er, ou ClinSV , et en prenant en compte les arguments déclarés dans le fichier de configuration (voir étape précédente).


```
#!/bin/bash
set -o pipefail;
/data/snakemake/miniconda3/envs/snakemake/bin/snakemake \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Snakefile_validation.smk \
-k --rerun-incomplete \
--configfile /scratch3/spim-preprod/pipeline_validation_wgs/pipeline_config/config.json \
--cluster-config /scratch3/spim-preprod/pipeline_validation_wgs/cluster_config/cluster_config.json \
--cluster 'godjob.py create -n {cluster.name}_[Sample id] -t {cluster.tags} --external_image -v {cluster.volume_snakemake} -v {cluster.volume_home} -v {cluster.volume_scratch2} -v {cluster.volume_irods} -v {cluster.volume_scratch3} -v {cluster.volume_annotations} -c {cluster.cpu} -r {cluster.mem} -i {cluster.image} -s' \
-j 40 -w 60 2>&1 | tee /scratch3/spim-preprod/pipeline_validation_wgs/log/[Full analysis name].log
```

# Exemple de ligne de commande 
En considérant :
- [Sample id] = FS00505001
- [Full analysis name] = A00666_0012_WGS_MR_FS00505001_index_21042022_final
```
#!/bin/bash
set -o pipefail;
/data/snakemake/miniconda3/envs/snakemake/bin/snakemake \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Snakefile_validation.smk \
-k --rerun-incomplete \
--configfile /scratch3/spim-preprod/pipeline_validation_wgs/pipeline_config/config.json \
--cluster-config /scratch3/spim-preprod/pipeline_validation_wgs/cluster_config/cluster_config.json \
--cluster 'godjob.py create -n {cluster.name}_FS00505001 -t {cluster.tags} --external_image -v {cluster.volume_snakemake} -v {cluster.volume_home} -v {cluster.volume_scratch2} -v {cluster.volume_irods} -v {cluster.volume_scratch3} -v {cluster.volume_annotations} -c {cluster.cpu} -r {cluster.mem} -i {cluster.image} -s' \
-j 40 -w 60 2>&1 | tee /scratch3/spim-preprod/pipeline_validation_wgs/log/A00666_0012_WGS_MR_FS00505001_index_21042022_final.log
```
**Conseil :** il est cohérent d’utiliser les valeurs des 2 paramètres [Sample id] et [Full analysis name] comme celles décrites dans le fichier de configuration.
**Remarque :** La commande d'exécution du pipeline est générée automatiquement après la création de fichier de configuration. Il suffit de copier le contenu de fichier commande_*.txt sous le répertoire pipeline_config et le coller dans la plateforme GO-Docker

## Résultats :
La tâche de création du fichier config.json est terminée avec succès lorsque la section « over jobs » de GO-DOCKER laisse apparaître un statut « over » surlignée en vert ; (la tâche est en échec si la couleur de surbrillance est de couleur noire ; dans ce cas, il y a une erreur dans la ligne de commande).

Afin de s'assurer de la complétude du pipeline vérifier la présence des fichiers *_done.txt et *_csv_done.txt. Ce sont des fichiers vides indiquant le succés de l'analyse et de l'archivage des résultats sur S3.  

Aprés chaque analyse les résultats sont ajoutés dans un fichier out.csv et envoyé au S3 sous le nom data.csv.
# AWS_S3

 Le pipeline permet la compression et le stockage des résultats sur aws_S3,après chaque analyse. Pour cela la [configuration](https://docs.aws.amazon.com/fr_fr/cli/latest/userguide/cli-configure-files.html) de S3 doit être spécifiée sous :
```
/home/.aws/credentials
```
# Interface
Les résultats peuvent être visualisés via un [tableau de bord interactif](https://github.com/firas-akermi/dashboard_pipeline_validation_wgs.git).

# Références/Publications
[Hap.py](https://github.com/Illumina/hap.py)

[Witty.er](https://github.com/Illumina/witty.er) 

[ClinSV](https://github.com/KCCG/ClinSV)

Minoche AE, Lundie B, Peters GB, Ohnesorg T, Pinese M, Thomas DM, et al. ClinSV: clinical grade structural and copy number variant detection from whole genome sequencing data. Genome Medicine. 2021;13:32.

# Auteur

[**Firas AKERMI**](www.linkedin.com/in/firas-akermi)
2021-2023 Ingénieur en biologie et etudiant en Master 1 en Bioinformatique à Université Paris-Saclay

Stage M1, SeqOIA-IT, [avril 2022 - Août 2022]
encadré par Adrien Legendre, Intégrateur SeqOIA-IT

Titre du stage : Développement d'un pipeline automatisé pour la validation de détection des variants
