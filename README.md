# Simple-Scripts-for-data-analysis
This is just a repository for storing simple Python3 scripts which I have written to simplify my data analysis.
Make sure to have the necessary packages installed before usage.

Currently, there are scripts for:
1. Tm analysis (to determine Tm values from RNA/DNA melting experiments) (Updated 2023/09/22)

    Basics operation: (python3 Tm_multiple_curvefit.py --f *Insert file name here* [Optional arguments: --sn --rfl --rfh --l --h])
   
    1. The script accepts an input file of .txt or .csv file format with two columns of float values (1st column being "Temperature", 2nd column being "Absorption").
    2. The script then finds the temperature for which the changes in absorption are at their maximum.
    3. Uses data that surrounds the said data point and attempts to fit a sigmoidal curve (upper/lower range specified via --rfl --rfh argument, default is: *--rfl 15 --rfh 15*)
    4. Tm is determined by solving the second derivative function of the sigmoidal curve function
    5. The largest tangent angle (TA) is determined by inputting the Tm value to the first derivative function of the sigmoidal curve function
       (larger TA indicates higher cooperativity)
    6. Script output the figure of the data points near Tm, the fitted sigmoidal curve, and the curve of the first derivative function of sigmoidal curve. The exact values of Tm and TA are outputted in csv.
    7. Check the output figure to see if the curve was fitted properly before using the data. The output figure should look like something below.
       (First figure is for single phase transition, second is for bi-phasic transition)

    Additonal Change Log:
    1. Added --help page within the script. The definition of Optional arguments are specified there.
    2. Can now specify the temperature window in which the script will attempt to find the sigmoidal curve. Specified with --l and --h
       (default is: *--l 30 --h 90*)
    4. Can now analyze multiphasic transition with --sn argument (default is: *--sn 1*)

    ![NL-396-R004 txt_Sigmoid_fit](https://github.com/BenNiLu/Simple-Scripts-for-data-analysis/assets/137369525/34390c42-afc0-463f-883c-a3d51d17f648)
![NL-414-46-2 txt_Sigmoid_fit](https://github.com/BenNiLu/Simple-Scripts-for-data-analysis/assets/137369525/0e089d97-5421-43a7-a602-8ee709da022a)
