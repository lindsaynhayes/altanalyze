#!/usr/bin/env python

import numpy as np
import sys,string
import os
import os.path
from numpy import corrcoef, sum, log, arange
from scipy.stats.stats import pearsonr
import traceback
tandem = dict()
dem=dict()
new=dict()
samplelis=[]
key_length=[]
list_g=[]
lis1=[]
correc=dict()
lis2=[]

def create_corr_matrix(lines,tfs, gene_labels):
 print len(lines),len(tfs)
 for l in range(len(lines)):
    t=string.split(lines[l],'\t')
    t1=t[0]
    
    
    if t1 in tfs:
        t=t[1:]
        
        for k in range(len(lines)):
            if k ==0:
                continue
            
            list1=[]
            list2=[]
            ind=[]
            p=string.split(lines[k],'\t')
            
            p=p[1:]
            for i in range(len(t)-1):
                if(t[i]!='' and p[i]!=''):
                    ind.append(i)
                else:
                    continue
            for i in range(len(ind)-1):
                list1.append(float(t[ind[i]]))
                list2.append(float(p[ind[i]]))
            if len(list1)==0 or len(list2)==0:
                print l;sys.exit()
                correc[t1,gene_labels[k-1]]=0
                continue
            else:
                coefr=pearsonr(list1,list2)
                coef=coefr[0]
		correc[t1,gene_labels[k-1]]=coef
              
 return correc

def strip_first_col(fname, delimiter=None):
    with open(fname, 'r') as fin:
        for line in fin:
            
            try:
               yield line.split(delimiter, 1)[1]
            except IndexError:
               continue

def genelist(fname):
    head=0
    lis=[]
    for line in open(fname,'rU').xreadlines():
        
        line = line.rstrip(os.linesep)
        t=string.split(line,'\t')
	val=t[0]
        if t[0]=='UID':
            continue
        else:
           lis.append(val)
    #print lis
 
    return lis

def sample(fname):
    head=0
    for line in open(fname,'rU').xreadlines():
        line = line.rstrip(os.linesep)
	if head ==0:
	    t=string.split(line,'\t')
	    #print t
	    for p in range(9,len(t)):
		samplelis.append(t[p])
	    head=1
        else:
	    break;
    return samplelis

def create_corr_files(correc,filename, tfs, gene_labels):
    export_corrmat=open(filename[:-4]+'-corr.txt','w')
    #export_corrmat=open('correlation_matrix_up.txt','w')
    for li in range(len(gene_labels)):
        export_corrmat.write('\t'+gene_labels[li])
    export_corrmat.write('\n')
    for i in range(len(tfs)):
        export_corrmat.write(tfs[i]+'\t')
        
	for li in range(len(gene_labels)):
            try:
	        export_corrmat.write(str(correc[tfs[i],gene_labels[li]])+'\t')
	    except Exception:
               print traceback.format_exc()
               export_corrmat.write('NA')
	  #else:
	   # export_corrmat.write(str(0)+'\t')
	export_corrmat.write('\n')
	    #export_corrmat.write('\n')
    export_corrmat.close()
   
def strip_first_col(fname, delimiter=None):
    with open(fname, 'r') as fin:
        for line in fin:
            try:
               yield line.split(delimiter, 1)[1]
            except IndexError:
               continue

def runTFCorrelationAnalysis(query_exp_file,query_tf_file):
    query_data = open(query_exp_file,'rU')
    lines = query_data.readlines()
    print "Number or rows in file:",len(lines)
    query_data.close()

    tfs=genelist(query_tf_file)
    gene_labels=genelist(query_exp_file)
    
    correc=create_corr_matrix(lines,tfs,gene_labels)
    create_corr_files(correc,query_exp_file,tfs,gene_labels)

if __name__ == '__main__':
    import getopt
    filter_rows=False
    filter_file=None
    if len(sys.argv[1:])<=1:  ### Indicates that there are insufficient number of command-line arguments
      print "Insufficient arguments";sys.exit()
    else:
        options, remainder = getopt.getopt(sys.argv[1:],'', ['i=','t='])
        #print sys.argv[1:]
        for opt, arg in options:
            if opt == '--i': query_exp_file=arg
            elif opt == '--t': query_tf_file=arg
            
    runTFCorrelationAnalysis(query_exp_file,query_tf_file)



