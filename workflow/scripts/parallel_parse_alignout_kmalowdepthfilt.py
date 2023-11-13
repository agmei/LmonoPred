"""
Author: ALGM

Date: 29.04.2021

Parses multiple output files  (blast or kma).
If there is no result for some of the genes from the Database there will be a "NaN" in the final output.
The output is a summary file in csv format (',' delimited).

The script uses 3 inputs. The path to the output directory of the blast search (absolute or relative), 
the full path to the database that you are using, and the desired output name (or path+outfile name to where
you want the outfile to be).
The script uses the %-identity from the hit on top of the list for each gene from the blast output. 
It is set to work with the output format 6 for blast so if you plan to change some output parameters,
make sure that it still uses the right columns (gene name and identity).  
The output file will be stored in the same directory as the input files if no path is given.

"""

import sys
import glob, os
import pandas as pd
from pathlib import Path
from joblib import Parallel, delayed 
from Bio import SeqIO


def get_gene_names_seqio(db_ref_file):
    
    gene_n=list()
    
    with open(db_ref_file) as fh:
        for virg in SeqIO.parse(fh, "fasta"):
            # be careful, somwtimes id is not whole name
            # I think when there are spaces in the name
            #gene_n.append(virg.id)
            gene_n.append(virg.description)
            
    return gene_n


def set_default_NaN(data_, diff_):
    for d in diff_:
        #data.setdefault(d,[]).append("NaN")
        data_.setdefault(d.strip(),"NaN")

    data_sorted_=dict(sorted(data_.items()))    

    return data_sorted_
    

def parse_blast_out(virgenesall,currfile):
    data_={}
    virgenesl=[]
    
    # strip path and extention
    # adjusted so it recognizes tblastx and tblastn output
    sample=os.path.basename(currfile).split("_tblast")[0] 
	
    # add filename to dictionary to create panadas df
    data_['Genome']=sample
   
    # open infile for parsing
    fi=open(currfile, 'r')
    for line in fi:
        # get virgene name and identity-values
        cols=line.split("\t")
        virgene=cols[0]
        #print(virgene,identity) 
        # if the virgene is already in the list
        # skip (so the rest of the blast results for the same gene)
        if virgene not in virgenesl:
            identity=cols[2]
            # to create a dictionary with the gene name as key
            # and a list of identities coresponding to the order of the
            # samplenames list
            #data.setdefault(virgene,[]).append(identity)
            data_.setdefault(virgene, float(identity)) 
            virgenesl.append(virgene)
        else:
            continue
            
    #close
    fi.close()

    # get gene names for which there is no result
    diff=set(virgenesall).difference(set(virgenesl))
        
    data_sorted_=set_default_NaN(data_, diff)
    
    return data_sorted_



def parse_kma_out(virgenesall,col,currfile):
    data_={}
    virgenesl=[]
    sample=os.path.basename(currfile).split("_kmaout")[0]
    
    # add filename to dictionary to create panadas df
    data_['Genome']=sample


    # open infile for parsing
    fi=open(currfile, 'r')
    for line in fi:
        if line.startswith('#') == True:
            outcol_names=line.split("\t")
        else:
            # get virgene name and identity-values
            cols=line.split("\t")
            virgene=cols[0].strip()
            # get identity
            identity=cols[outcol_names.index(col)]
            # to create a dictionary with the gene name as key
            # and a list of identities coresponding to the order of the
            # samplenames list
            # Also filter for hits with depth lower than 5
            depth=float(cols[outcol_names.index("Depth")])
            if depth >= 5.0:
                data_.setdefault(virgene, float(identity))
                virgenesl.append(virgene)

    fi.close()

    # get gene names for which there is no result
    diff=set(virgenesall).difference(set(virgenesl))
    
    data_sorted_=set_default_NaN(data_, diff)

    return data_sorted_


if __name__ == '__main__':
    
    if len(sys.argv) < 5:
        print('''\nArguments are missing...
    Usage: parse_blastout_firsthit.py [path/to/infiles] [path/to/db] [outfile name] [number of processes]\n''')
        sys.exit(1)
    
    blast_out_f=[]
    kma_out_f=[]
    

    #get list of virulence gene names
    invirf = os.path.abspath(sys.argv[2])
    virgenesall = get_gene_names_seqio(invirf)


    # get input filepath from argument and make absolute path
    filepath = os.path.abspath(sys.argv[1])

    # check if outfile name is a path or just a filename
    # also if the outfile is a path then check if it exists
    # if not make the path 
    if os.path.dirname(sys.argv[3]) == '':
        outf = os.path.join(filepath,sys.argv[3])
    else:
        if os.path.isdir(os.path.dirname(sys.argv[3])) == False:
             os.mkdir(os.path.dirname(sys.argv[3]))
        outf = os.path.abspath(sys.argv[3])

    os.chdir(filepath)
    
    # get all the blast out files in the input directory
    for f in glob.glob(os.path.join(filepath,"*.txt")):
    	blast_out_f.append(f)
    
    blast_out_f=sorted(blast_out_f)
    
    # get all the kma out files in the input directory
    for f in glob.glob(os.path.join(filepath,"*.res")):
    	kma_out_f.append(f)
    
    kma_out_f=sorted(kma_out_f)
    
    
    # defining the number of cores
    # this is specifying how many jobs should be used
    n_cores=int(sys.argv[4])
    
    #get results from blast
    blast_res = Parallel(n_jobs=n_cores)(delayed(parse_blast_out)(virgenesall, x) for x in blast_out_f)
    
    #get results form kma
    kma_res = Parallel(n_jobs=n_cores)(delayed(parse_kma_out)(virgenesall,"Template_Identity", x) for x in kma_out_f)
    
    all_res=blast_res
    all_res.extend(kma_res)

    
    # create pandas dataframe and save it in .csv format
    df= pd.DataFrame(all_res).set_index('Genome')
    df.to_csv(outf, sep=";") 
