# predict the results
rule predict_virulence:
    input:
        outd+"/vir_align_out/vir_align_identities_out.csv"
    output:
        outd+"/virulence_prediction_out.csv"
    params:
        outd=outd
    shell:
        "python3 workflow/scripts/virulence_prediction.py --vir-align {input} --outd {params.outd}"


rule predict_disinftolerance:
    input:
        outd+"/disinf_align_out/disinf_align_identities_out.csv"
    output:
        outd+"/disinftolerance_prediction_out.csv"
    params:
        outd=outd
    shell:
        "python3 workflow/scripts/disinftolerance_prediction.py --disinf-align {input} --outd {params.outd}"