# ListPred

### Introduction

ListPred is a ML based prediction pipeline that uses whole genome sequencing data to predict virulence potential and disinfectant tolerance of *Listeria monocytoges* isolates. In its current implementation, ListPred predicts the tolerance of *L. monocytogenes* isolates to benzalkonium chloride, a compound that is frequently used in food industry disinfectants. The implementation of tolerance prediction models for other disinfectants is currently under development. 

### Input

ListPred can analyze raw or assembled short- and long-read sequencing data. To ensure compatibility with the pipeline the user is required to follow some naming conventions. 

-	Raw reads should generally end with *“.fastq.gz”* or *“.fq.gz”*
	In addition, paired-end sequencing files should include either *“_R1”* and *“_R2”* or *“_1”* and *“_2”* in their names.
-	Single end read files, for both short- and long-read files, should be marked with a *“_SE”* specifier. 
-	Assemblies should end with either *“.fa”*, *“.fasta”*, or *“.fna”*



### Output
ListPred classifies isolates into low, medium, or high virulence risk categories and into sensitive or tolerant groups for benzalkonium chloride tolerance. The output from the web application will be a zip compressed folder containing two csv files, i.e., ‘combined_predictions_out_categorical.csv’ and ‘combined_predictions_out_numerical.csv’ which describe the predictions as category labels and numerical values respectively. Additionally, the folder contains files from the pre-processing steps. 

```
ListPred_results
├── isolate01_tblastxout.txt					# Output from the screening against the reference databases (blast/kma)
├── combined_predictions_out_categorical.csv 	# Combined prediction output using class labels
├── combined_predictions_out_numerical.csv 		# Combined prediction output using numerical values
├── disinf_align_identities_out.csv 			# disinfectant tolerance reference genes %-idenity tables (ML prediction input)
├── disinftolerance_prediction_out.csv 			# ML prediction output for disinfectant tolerance
├── vir_align_identities_out.csv 				# virulence potential reference genes %-idenity tables (ML prediction input)
└── virulence_prediction_out.csv 				# ML prediction output for virulence potential
```

### Usage

Once you cloned the repository from GitHub, move into the ListPred folder and execute the snakemake pipeline as seen in the examples below. 

To run the ListPred pipeline locally, snakemake (version >= 7.32.4) is required. 

```
--cores 			# number of cores you want to use
--use-conda			# required so snakemake is building the correct environments for the ML prediction models
--config			# used to pass information through snakemake to the underlying ML models
	ind=			# use to analyse multiple samples (i.e., path to input directory with multiple input files)
	inp=			# use to analyse individual samples (assemblies and long-read raw reads as input)
	ipe=			# use to analyse individual samples (paired-end short-read raw reads as input)
	out=			# path to output directory 
```

Examples:
```
directory as input ('ind')
snakemake --cores 4 --use-conda --config ind="path/to/input_directory" outd="path/to/output_directory"

assembly as input ('inp')
snakemake --cores 4 --use-conda --config inp="path/to/assembly_01.fa" outd="path/to/output_directory"

long-read raw reads ('inp')
snakemake --cores 4 --use-conda --config inp="path/to/longreads_SE.fastq.gz" outd="path/to/output_directory"

short-read raw reads ('ipe')
snakemake --cores 4 --use-conda --config ipe="path/to/shortreads_R1.fastq.gz path/to/shortreads_R2.fastq.gz" outd="path/to/output_directory" 
```

### Further information

For more information regarding ListPred and the underlying ML models, please refer to the respective publications:
-	“Predicting Listeria monocytogenes virulence potential using whole genome sequencing and machine learning”, https://doi.org/10.1016/j.ijfoodmicro.2023.110491
-	“Quantitative prediction of disinfectant tolerance in Listeria monocytogenes using whole genome sequencing and machine learning”, https://doi.org/10.1101/2023.11.05.565740
-	“ListPred: A predictive ML tool for virulence potential and disinfectant tolerance in Listeria monocytogenes” https://doi.org/10.1101/2024.01.29.577690
