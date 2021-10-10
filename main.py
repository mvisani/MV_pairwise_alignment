from Bio import Align, SeqIO
from Bio.Align import substitution_matrices
from Bio.Emboss.Applications import NeedleCommandline
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd 
import numpy as np 
import openpyxl
import re
import csv
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
#filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

### First we need to load all files before running the program ####

#Choose the proteome of the organism of your MS file
Tk().withdraw()
Proteome1_path = askopenfilename(title = 'Choose proteome of the organism of your MS file')
Proteome1_id = []
Proteome1_seq = []
for p in SeqIO.parse(Proteome1_path, 'fasta'):
    Proteome1_id.append(p.id)
    Proteome1_seq.append(p.seq)

#Choose the proteome you want to compare it with 
Proteome2_path = askopenfilename(title = 'Choose the proteome you want to compare it with')
Proteome2_id = []
Proteome2_seq = []
for n in SeqIO.parse(Proteome2_path, 'fasta'):
    Proteome2_id.append(n.id)
    Proteome2_seq.append(n.seq)

#Choose BLAST file 
BlastCSV_path = askopenfilename(title = "Choose BLAST file" )
BlastCSV = pd.read_csv(BlastCSV_path, header=None)

#Finally choose the MS file to be analyzed
MSFile_path = askopenfilename(title = "Choose the MS file to be analyzed")
MSFile = pd.read_excel(MSFile_path, engine='openpyxl', header=0)
Protein1_name_list = []
Protein2_name_list = []
Position_of_AA_1 = []
Position_of_AA_2 = []
AA_1 = []
AA_2 = []

for my_prot_name in range(len(MSFile['Entry'])) :
    try :
        Protein1_line = BlastCSV[BlastCSV[0].str.contains(MSFile['Entry'][my_prot_name])]
        index_prot = Protein1_line.index[0]
        Protein1_name = BlastCSV.loc[index_prot,0]
        Protein2_name = BlastCSV.loc[index_prot,1]

        Protein1_name_list.append(Protein1_name)
        Protein2_name_list.append(Protein2_name)
        
        Position_in_fasta_Prot1 = [z for z, s in enumerate(Proteome1_id) if Protein1_name in s]
        Position_in_fasta_Prot2 = [x for x, s in enumerate(Proteome2_id) if Protein2_name in s]

        ##Get sequences of both proteins
        Seq1 = Proteome1_seq[Position_in_fasta_Prot1[0]]
        Seq2 = Proteome2_seq[Position_in_fasta_Prot2[0]]

        #Start pairwise alignment
        aligner = Align.PairwiseAligner()
        aligner.open_gap_score = -10
        aligner.extend_gap_score = -0.5
        aligner.mode = 'local'
        aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
        try :
            alignments = aligner.align(Seq1, Seq2)
        except ValueError:
            pass
        alignment = alignments[0]
        nested = alignment.aligned

        for my_position in range(len(nested[0])):
            if nested[0][my_position][0] <= MSFile['Position'][my_prot_name] - 1 < nested[0][my_position][1]:
                PythonAAreal1 = int(MSFile['Position'][my_prot_name] - 1)
                y = nested[0][my_position][1] - MSFile['Position'][my_prot_name] + 1
                AAreal2 = int(nested[1][my_position][1] - y + 1)
                #if it finds an alignemnt, it will save that position and break the loop, otherwise it will continue
                break
            else :
                #if at the end of the loop it didn't find anything, the amino acid of the corresponding protein is "-"
                AAreal2 = '-'
                continue
        Position_of_AA_1.append(int(MSFile['Position'][my_prot_name]))
        Position_of_AA_2.append(AAreal2)
        if isinstance(AAreal2, (int, np.integer)) == True :
            PythonAAreal2 = int(AAreal2 - 1)
            AA_2.append(str(Seq2[PythonAAreal2]))
            AA_1.append(str(Seq1[PythonAAreal1]))
        else:
            AA_2.append('-')
            PythonAAreal1 = int(MSFile['Position'][my_prot_name] - 1)
            AA_1.append(str(Seq1[PythonAAreal1]))
    except IndexError:
        pass

my_columns = zip(Protein1_name_list, Position_of_AA_1, AA_1, Protein2_name_list, Position_of_AA_2, AA_2)
with open('output.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerow(['Protein of MS file', 'Position', 'Amino Acid', 'Target protein', 'Corresponding position', 'Amino acid'])
    for row in my_columns:
        writer.writerow(row)
