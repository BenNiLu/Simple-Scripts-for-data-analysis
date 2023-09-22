import numpy as np
import sys
import argparse
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from sympy.abc import x
from sympy import solve

def main (input_DF, file_name):
    xdata = np.array(input_DF['Temp'].values.tolist())
    ydata = np.array(input_DF['ABS'].values.tolist())
    ydata = ydata-ydata.min() #subtract baseline absorption

    def sigmoid(x, L=max(ydata), x0=21, k=0.6, b=5): #define sigmoidal curve function to fit
        y = (L / ((1 + np.exp(-k*(x-x0)))))+b
        return (y)

    p0 = [max(ydata), np.median(xdata), 1, 0] #initial guess condition for sigmoid curve 

    popt, pcov = curve_fit(sigmoid, xdata, ydata, p0, method='dogbox',  maxfev=100000) #fit
    # print(popt)
    L=popt[0]
    x0=popt[1]
    k=popt[2]
    b=popt[3]
    e = np.e

    solved_sigmoid_func = (L/(1+e**(-k*(x-x0))))+b #best fit sigmoid function (for use below)
    print(solved_sigmoid_func)

    Sigmoid_deriv = solved_sigmoid_func.diff(x) #first differentiation (for Tangent angle value)
    Sec_Sig_deriv = solved_sigmoid_func.diff(x, 2) #second differentiation (for Tm value)


    local_max = solve([x >= xdata.min(), x <= xdata.max(),Sec_Sig_deriv],x) #solve the second derivative function -> Tm value
    TM_value = float(str(local_max)[5:19]) #Parse Tm from output
    TA_value=Sigmoid_deriv.subs({x:TM_value}) #input Tm value to solve for the largest Tangent Angle

    Summary = 'Tm = '+str(TM_value)+', TA = '+str(TA_value)
    print(Summary)

    ydd = [] 
    for i in xdata: #out put data for plotting first derivative line
        ydd.append(Sigmoid_deriv.subs({x:i}))

    yd = sigmoid(xdata, *popt)
   
    plt.plot(xdata, ydata, 'o', label='data') #plot the data
    plt.plot(xdata,ydd, '-', label='fit_deriv') #plot the first derivative curve
    plt.plot(xdata,yd, label='fit') #plot the fit line
    plt.legend(loc='best')
    #plt.show()
    plt.savefig(f'{file_name}_Sigmoid_fit.png')
    df2 = pd.DataFrame({'name':str(file_name),'Tm':TM_value,'TA':TA_value}, index=['i',])
    df2.to_csv("TA.csv", mode='a', header=True, index=False)

def find_Tm_range(Input_DF, reference_frame_lower, reference_frame_upper, lower_limit, higher_limit):
    temp_Df=Input_DF.drop(Input_DF[Input_DF.Temp < lower_limit].index)
    temp_Df.drop(temp_Df[temp_Df.Temp > higher_limit].index, inplace=True)
    temp_Df['diff']=temp_Df['ABS'].diff()
    idxmax=temp_Df['diff'].idxmax()
    Temp=temp_Df['Temp']
    Tm=int(Temp[idxmax])
    if Tm-int(reference_frame_lower) < int(Input_DF['Temp'].iat[0]):
        start_temp = Input_DF['Temp'].iat[0]
    else:
        start_temp = Tm-int(reference_frame_lower)
    if Tm+int(reference_frame_upper) > int(Input_DF['Temp'].iat[-1]):
        end_temp = Input_DF['Temp'].iat[-1]
    else:
        end_temp = Tm+int(reference_frame_upper)

    target_range = [start_temp, end_temp] 
    print(target_range)
    return target_range

def Fit_sigmoid(infile=None, no_sig=1, reference_frame_lower=15, reference_frame_upper=15, lower_limit=30, higher_limit=90):
    df=pd.read_csv(infile, names=('Temp', 'ABS')) #Parse data
    for i in range(int(no_sig)):
        Target_Fit_range = find_Tm_range(df, reference_frame_lower,reference_frame_upper, lower_limit, higher_limit)
        df2 = df.drop(df[df.Temp < Target_Fit_range[0]].index)
        df2.drop(df2[df2.Temp > Target_Fit_range[1]].index, inplace=True)
        main(df2, infile)
        if Target_Fit_range[0]-int(df['Temp'].iat[0]) <= int(df['Temp'].iat[-1])-Target_Fit_range[1]:
            df.drop(df[df.Temp < Target_Fit_range[1]].index, inplace=True)
        elif Target_Fit_range[0]-int(df['Temp'].iat[0]) > int(df['Temp'].iat[-1])-Target_Fit_range[1] and Target_Fit_range[0] > lower_limit:
            df.drop(df[df.Temp > Target_Fit_range[0]].index, inplace=True)
        else:
            df.drop(df[df.Temp < Target_Fit_range[1]].index, inplace=True)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Determine Tm and TA of melt curve, adapted for single/multiphasic curves directly from raw txt file")
    parser.add_argument("--f", "--inFile", help="The name of TXT file to be imported. E.g. something.txt")
    parser.add_argument("--sn","--No_Sigmoid", type=int, default=1, help="Number of Sigmoidal curve expected in the data, default is 1")
    parser.add_argument("--rfl","--ref_frame_l", type=int, default=15, help="Lower range distance [data point] from the Tm to be taken account when fitting curve, default is 15")
    parser.add_argument("--rfh","--ref_frame_h", type=int, default=15, help="Higher range distance [data point] from the Tm to be taken account when fitting curve, default is 15")
    parser.add_argument("--l", "--lower_limit", type=int, default=30, help="The minimum temperature below which it will not look for a Tm curve, default is 30")
    parser.add_argument("--h", "--higher_limit", type=int, default=80, help="The maximum temperature above which it will not look for a Tm curve, default is 90")
    args = parser.parse_args()
    inFile = args.f
    no_sig = args.sn
    reference_frame_lower = args.rfl
    reference_frame_upper = args.rfh
    lower_limit = args.l
    higher_limit = args.h
    Fit_sigmoid(inFile, no_sig, reference_frame_lower, reference_frame_upper, lower_limit, higher_limit)
