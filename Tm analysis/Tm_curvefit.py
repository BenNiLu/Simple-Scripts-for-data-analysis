import numpy as np
import sys
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from sympy.abc import x
from sympy import solve

def main (file_name):
    df1=pd.read_csv(file_name, names=('Temp', 'ABS')) #Parse data
    Target_Fit_range = find_Tm_range(df1)
    df1.drop(df1[df1.Temp < Target_Fit_range[0]].index, inplace=True)
    df1.drop(df1[df1.Temp > Target_Fit_range[1]].index, inplace=True)
    xdata = np.array(df1['Temp'].values.tolist())
    ydata = np.array(df1['ABS'].values.tolist())
    ydata = ydata-ydata.min() #subtract baseline absorption

    

    def sigmoid(x, L=max(ydata), x0=21, k=0.6, b=5): #define sigmoidal curve function to fit
        y = (L / ((1 + np.exp(-k*(x-x0)))))+b
        return (y)

    p0 = [max(ydata), np.median(xdata), 1, 0] #initial guess condition for sigmoid curve 

    popt, pcov = curve_fit(sigmoid, xdata, ydata, p0, method='dogbox',  maxfev=10000) #fit
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

def find_Tm_range(Input_DF=pd.DataFrame()):
    Input_DF['diff']=Input_DF['ABS'].diff()
    idxmax=Input_DF['diff'].idxmax()
    Temp=Input_DF['Temp']
    Tm=int(Temp[idxmax])
    if Tm-20 < int(Input_DF['Temp'].iat[0]):
        start_temp = Input_DF['Temp'].iat[0]
    else:
        start_temp = Tm-20
    if Tm+20 > int(Input_DF['Temp'].iat[-1]):
        end_temp = Input_DF['Temp'].iat[-1]
    else:
        end_temp = Tm+20

    target_range = [start_temp, end_temp] 
    print(target_range)
    return target_range


if __name__ == '__main__':
    inFile = sys.argv[1]
    main(inFile)