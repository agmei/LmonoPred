# tblastx for files that end with '.fa'
rule align_assemblies_fa:
    input:
        sample=ind+"/{sample}.fa"
    output:
        outd+"/vir_align_out/{sample}_tblastxout.txt"
    params:
        db="data/databases/pan_genome_reference_finalmodel_featurefilt.fa"
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
        ind+"/{sample}_R1.fastq.gz", ind+"/{sample}_R2.fastq.gz"
    output:
        outd+"/vir_align_out/{sample}_kmaout.res"
    params:
        db="data/databases/kma_pangenome_virulence/kma_pangenome_nucleotide_finalmodel_featurefilt",
        outn=outd+"/vir_align_out/{sample}_kmaout"
    shell:
        "kma -ipe {input[0]} {input[1]} -o {params.outn} -t_db {params.db} -1t1"


# parse alignment output
rule parse_alignments:
    input:
        expand("{outd}/vir_align_out/{sample}_tblastxout.txt", outd=outd, sample=assbly_ids),
        expand("{outd}/vir_align_out/{sample}_kmaout.res", outd=outd, sample=raw_ids)
    output:
        outd+"/vir_align_out/vir_align_identities_out.csv"
    params:
        indir=outd+"/vir_align_out/",
        db="data/databases/virulence_genes_nuc_database.fa",
        outn="vir_align_identities_out.csv"
    threads: cores
    shell:
        "python3 workflow/scripts/parallel_parse_alignout.py {params.indir} {params.db} {params.outn} {threads}"

