# mem-tension

These are the scripts I used to analyse membrane tether force data generated using my optical tweezers in Ulrich Keyser's group at the Cavendish Lab, University of Cambridge. There are two scripts, one for 3T3 fibroblast data, and one for neuron data. All the functions needed to run the scripts are found in this repo. The data files are in .tdms format and so require npTDMS to be opened in python (you can find that here: https://github.com/adamreeve/npTDMS, an extremely useful package maintained by Adam Reeve).

<h1>How to use</h1>

These scripts were written specifically to analyse the datsets used in this study: https://www.biorxiv.org/content/10.1101/2021.11.09.467973v1. To use either main script, simply run it, you should be presented with a file dialog window where you can navigate to the parent directory that contains the sub-directories of data files, and select that parent folder. After this you will be presented with another window where you can choose a save location for the force trace plots that are generated for each file.
