# GraftJ
A program for grafting antibody donor CDR loops onto acceptor sequences. Designed by Yilan Yu and programmed by Jordan Jantschulev.

Inputs: 
 
•	a .txt file (in FASTA format) of the sequence alignment including the acceptor sequence (in our case Moon nanobody)
•	RANGE: a-b, c-d, e-f (where a,b,c ... correspond to amino acid positions in the aligned sequences) is to be added at the top of the file (please save file afterwards)
•	Insert @ in front of the > of the acceptor sequence.

GraftJ will then splice out the specified ranges of the donor sequences to replace the same specified range within the acceptor sequence. Finally, the program would remove all '_' (placeholders from sequence alignment) as well as the text inputs, leaving a clean FASTA-formatted output that is then exported into an Excel.



