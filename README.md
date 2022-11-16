# gromacs_on_cluster
A series of scripts on how to run a MD simulation of a protein using gromacs on a cluster.
The main script for a direct call to use is md_run. In the current version this 
would take the pdb INPUT.pdb from the input folder and prepare it for minimization as
well as run minimzation, NVT and NPT equilibration and then createing a tpr
for the productive run. Although this works sometimes I mostly recommend doing those 
step by step, by commenting out all other functions in the bottom of the script 
and only calling it with one function at a time not commented out.
Otherwise if it doesn't work you will see a bunch of errors.

Furthermore, the batch job obviously needs to be adapted to the parameters you
need to run it on your cluster. Stuff like, partition, account, different number
of taks etc need to be considered.

Otherwise the configuration files are largely based on
http://www.mdtutorials.com/gmx/lysozyme/index.html
