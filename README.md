# Simple-Scripts-for-data-analysis
This is just a repository for storing simple Python3 scripts which I have written to simplify my data analysis.

Currently, there are scripts for:
1. Tm analysis (to determine Tm values from RNA/DNA melting experiments)

    Basics operation:
    1. The script accepts an input file of .txt or .csv file format with two columns (1st column being "Temperature", 2nd column being "Absorption").
    2. The script then finds the temperature for which the changes in absorption are at their maximum.
    3. Uses data that is +(-) 20 C from the said data point and attempts to fit a sigmoidal curve against the 41 data points
    4. Tm is determined by solving the second derivative function of the sigmoidal curve function
    5. The largest tangent angle (TA) is determined by inputting the Tm value to the first derivative function of the sigmoidal curve function
       (larger TA indicates higher cooperativity)
    6. Script output the figure of the data points near Tm, the fitted sigmoidal curve, and the curve of the first derivative function of sigmoidal curve. The exact values of Tm and TA are outputted in csv.
    7. Check the output figure to see if the curve was fitted properly before using the data. The output figure should look like something below.

    ![NL-396-R004 txt_Sigmoid_fit](https://github.com/BenNiLu/Simple-Scripts-for-data-analysis/assets/137369525/34390c42-afc0-463f-883c-a3d51d17f648)
