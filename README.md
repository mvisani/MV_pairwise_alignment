## pairwise_alignment

# Abstract
This code was created during an internship that I made at the University of Fribourg. I had never learned Python and decided to attend a basic Python course in order to understand the fundamentals of programming. Has I got more and more interested in coding, I wanted to try to create my own program that had a real life purpose. I decided to ask one of the PhDs there to see if I could code something that would make their life easier. He was interested in looking if some specific phosphosites were conserved through different organismes of interest.

I decided then decided to try build a program that would align a protein of an organism with the homologous protein of the organism of interest and tell if a specific site of interest is conserved or not. 

# What you'll need
This code needs 4 files as input. 
* 2 files are the proteomes of the 2 diffrent organisms that we are interested in, as a ".fasta" format (downloadable on https://www.uniprot.org). 
* The third file is a ".csv" file containing the name of the protein of one organism paired with the homologous protein of the other organism. This file was created using a downloaded version of Blast+ by NCBI (https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/).
* An output mass spectrometry analysis made by MaxQuant from Max-Planck-Institute for Biochemistry (this file was an Excel file for us). 

In addition to that, one must have all the packages written at the top of the code installed and ready to run.

# Files preparation
Before starting the alignment, we decided to BLAST the entire proteome of our organism against the proteome of the organisme of interest. Usually pBLAST ouputs multiple proteins from one query (in our case : an entire protein instead of a sequence of amino acid). Since we were only interested in the most closely "related" protein, we decided to ouput only one protein per query. Please note that the documentation recommends to set a minimum of 5 sequences as "-max_target_seqs". But for the purpose of this program, only the best target was kept and aligned with our protein of interest.

For more detailed information about the BLAST+ suite and how to perform such queries, please check their detailed documentation (https://www.ncbi.nlm.nih.gov/books/NBK279690/). We decided to set the e-value for the BLAST analysis at 0.00001, the maximum target sequences at 1 (explained above) and the output format as ".csv". 

# Starting the program and explanation
Once we lauch the program, the latter will ask us to select the files we prepared. The first file is the proteome of the organsim you analyzed with mass spectrometry. The program will then parse file and save into a list all ID of all proteins and their corresponding sequence. The program will then do the same for the second file which is the proteom of the organism we are interested in. The program will then open the third file (BLAST file) and create a pandas data-frame containing its data. Finally the fourth file must be the mass spectrometry file itself and will be opened as a pandas data frame as well.

The program will then loop over every protein of the MS file. For each protein, it will ask if the unique entry identifier of the protein is present in the BLAST file. If not it will just pass that protein and go to the next one. If yes, it will look for this protein and its homolog in the BLAST file and save their name for the final ouput file. Since we have the proteins IDs, the program will look for the proteins in the fasta files and save the corresponding sequence.  

Once the program has both sequenes, it will start the pairwise alignment. We decided to keep the default parameters of the local pairwise alignment Water (EMBOSS), from EMBL-EBI (https://www.ebi.ac.uk/Tools/psa/). Feel free to change the parameters as you like and to check BioPython documentation for a more detailed explanation of how the alignment in Python works (https://biopython.org/wiki/Documentation). 

Python output a nested tuple with the range of the position of the amino acids of the first protein with the range of amino acids of the other protein (see BioPython documentation for examples of how "alignment.aligned" ouputs). 

The program will search the position of amino acid you of your MS file and look if it is aligned to anything. If yes, it will save the position of the corresponding amino acid. If not, it will save a "-" meaning that it is not aligned with anything. If it found an alignment, the program will also save the amino acid one letter code that is at that position, otherwise it will also save a "-". 

Finally, the program will save into a CSV format, the name of the protein of the MS file, the posistion of the amino acid, the letter of the amino acid, the name of the protein of the organism that we are interested in, the posisiton of the aligned amino acid and the letter of the amino acid of that protein. 

# Comments and critiques 
This program was made as a self learning project and its initial goal was for me to learn Python. However this program resulted in being useful for some people in the University and allowed them gain a lot of time. Indeed, some people used to check by hand if some sites of a protein were conserved or not. This program allows them to quickly check the latter and to have all proteins of their MS file aligned in one single file. 

It is obvious that this program isn't perfect and each couple of protein should be aligned with their own specific parameters. In the same time this program gives good results for closesly related proteins and outputs the same alignment of the EMBOSS Water pairwise alignment (since it uses the same parameters). Moreover, this program allowed me to learn about the basics of Python and the use of informatics in Biology. 

# Note from the author
Please fell free to give me some tips on how to improve this code, or the entire program. I am really interested into learining and improving in Python and I think having an actual project is the best way to learn. 

I would like to thank all the PhDs, Professors and friends that supported me and gave me some advice. I would like to especially thant Axel Giottonini for all the times that I was stuck or didnt understand something. Feel free to check his LinkedIn page (https://www.linkedin.com/in/axel-giottonini/). 

Feel free to check my LinkedIn page too :D :

https://www.linkedin.com/in/marco-visani-594790186/
