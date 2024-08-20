import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

path = 'Test_2.csv'
df = pd.read_csv(path)

voltage = df['0A_Voltage']
current = df['0A_Current']

voltage = np.array(voltage)
current = np.array(current)
power = voltage*current

def fit_func(x, a, b):
    return a - b * np.exp(38.68 * x)

def plot(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, -y, '.')
    ax.plot(x, -y * x, '.')
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (A)')
    # ax.set_xlim(0, 0.7)
    # ax.set_ylim(-0.1, 0.2)
    ax.set_title('IV Curve')
    ax.hlines(0, 0, 0.7, colors='black')
    ax.grid()

if __name__ == '__main__':
    #fit the IV curve in the interval [0, 0.7]
    popt, pcov = curve_fit(fit_func, voltage, current, bounds=([0, 0], [1, 1]))
    print("a = ", popt[0], "b = ", popt[1])

    #plot IV and PV curves on the same graph
    plot(voltage, current)
    plot(voltage, fit_func(voltage, *popt))
    plt.show()
