# tblastx for files that end with '.fa'
rule disinf_align_assemblies_fa:
    input:
        sample=ind+"/{sample}.fa"
    output:
        outd+"/disinf_align_out/{sample}_tblastxout.txt"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        db="data/databases/disinf_pan_genome_reference.fa"
    shell:
        'tblastx -query {params.db} -subject {input.sample} -outfmt 6 -out {output} -evalue 0.001 -max_hsps 1'


# tblastx for files that end with '.fna'
use rule disinf_align_assemblies_fa as disinf_align_assemblies_fna with:
    input:
        sample=ind+"/{sample}.fna"


# tblastx for files that end with '.fasta'
use rule disinf_align_assemblies_fa as disinf_align_assemblies_fasta with:
    input:
        sample=ind+"/{sample}.fasta"


rule disinf_align_rawreads:
    input: 
        ind+"/{sample}_R1.fastq.gz", ind+"/{sample}_R2.fastq.gz"
    output:
        outd+"/disinf_align_out/{sample}_kmaout.res"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        db="data/databases/kma_pangenome_disinf/disinf_pan_genome_reference",
        outn=outd+"/disinf_align_out/{sample}_kmaout"
    shell:
        "kma -ipe {input[0]} {input[1]} -o {params.outn} -t_db {params.db} -1t1"


# parse alignment output
rule disinf_parse_alignments:
    input:
        expand("{outd}/disinf_align_out/{sample}_tblastxout.txt", outd=outd, sample=assbly_ids),
        expand("{outd}/disinf_align_out/{sample}_kmaout.res", outd=outd, sample=raw_ids)
    output:
        outd+"/disinf_align_out/disinf_align_identities_out.csv"
    conda:
        "../envs/LmonoPred_config.yml"
    params:
        indir=outd+"/disinf_align_out/",
        db="data/databases/disinf_pan_genome_reference.fa",
        outn="disinf_align_identities_out.csv"
    threads: cores
    shell:
        "python3 workflow/scripts/parallel_parse_alignout.py {params.indir} {params.db} {params.outn} {threads}"

