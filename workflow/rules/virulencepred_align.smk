# tblastx for files that end with '.fa'
rule align_assemblies_fa:
    input:
        sample=ind+"/{sample}.fa"
    output:
        outd+"/vir_align_out/{sample}_tblastxout.txt"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        db="data/databases/vir_pan_genome_reference_finalmodel_featurefilt.fa"
    shell:
        'tblastx -query {params.db} -subject {input.sample} -outfmt 6 -out {output} -evalue 0.001 -max_hsps 1'


# tblastx for files that end with '.fna'
use rule align_assemblies_fa as align_assemblies_fna with:
    input:
        sample=ind+"/{sample}.fna"


# tblastx for files that end with '.fasta'
use rule align_assemblies_fa as align_assemblies_fasta with:
    input:
        sample=ind+"/{sample}.fasta"


rule align_rawreads:
    input: 
        sample1=ind+"/{sample}_R1.fastq.gz",
        sample2=ind+"/{sample}_R2.fastq.gz"
    output:
        outd+"/vir_align_out/{sample}_kmaout.res"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        db="data/databases/kma_pangenome_vir/kma_pangenome_nucleotide_finalmodel_featurefilt",
        outn=outd+"/vir_align_out/{sample}_kmaout"
    shell:
        "kma -ipe {input.sample1} {input.sample2} -o {params.outn} -t_db {params.db} -1t1"

# kma for files that end with '.fq.gz'
use rule align_rawreads as align_assemblies_fq with:
    input: 
        sample1=ind+"/{sample}_R1.fq.gz",
        sample2=ind+"/{sample}_R2.fq.gz"


# snakemake complains about ambuiguity (two rules able to produce same output) when using '.res' file ending
# that is why I use .fsa (another file produced by kma)
# that solves the ambuiguity issue for snakemake
rule align_rawreads_longreads:
    input:
        sample=ind+"/{longsample}_SE.fastq.gz"
    output:
        outd+"/vir_align_out/{longsample}_kmaout.fsa"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        db="data/databases/kma_pangenome_vir/kma_pangenome_nucleotide_finalmodel_featurefilt",
        outn=outd+"/vir_align_out/{longsample}_kmaout"
    shell:
        "kma -i {input.sample} -o {params.outn} -t_db {params.db} -mem_mode -mp 20 -mrs 0.0 -bcNano -bc 0.7"


# parse alignment output
rule parse_alignments:
    input:
        expand("{outd}/vir_align_out/{sample}_tblastxout.txt", outd=outd, sample=assbly_ids),
        expand("{outd}/vir_align_out/{sample}_kmaout.res", outd=outd, sample=raw_pairs_ids),
        expand("{outd}/vir_align_out/{sample}_kmaout.fsa", outd=outd, sample=raw_singles_ids)
    output:
        outd+"/vir_align_out/vir_align_identities_out.csv"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        indir=outd+"/vir_align_out/",
        db="data/databases/vir_pan_genome_reference_finalmodel_featurefilt.fa",
        outn="vir_align_identities_out.csv"
    threads: cores
    shell:
        "python3 workflow/scripts/parallel_parse_alignout.py {params.indir} {params.db} {params.outn} {threads}"

