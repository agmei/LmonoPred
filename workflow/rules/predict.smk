# predict the results
rule predict_virulence:
    input:
        f"{outd}"+"/align_out/align_identities_out.csv"
    output:
        f"{outd}"+"/virulence_prediction_out.csv"
    params:
        level="virgenes",
        outd=outd
    shell:
        "python3 /home/projects/course_23262/course/week09/scripts/pred_virulence/workflow/scripts/run_prediction.py -inf {input} -outd {params.outd} -l {params.level}"