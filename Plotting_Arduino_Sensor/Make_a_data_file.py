
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animasi
import time
import numpy as np

def decomp (c,d,e):
    
    n = len(d)
    
    for k in range(1,n):

        lam = c[k-1]/d[k-1]
        d[k] = d[k] - lam*e[k-1]
        c[k-1] = lam

    return c,d,e

def solve (c,d,e,b):

    n = len(d)

    for k in range(1,n):
        b[k] = b[k] - c[k-1]*b[k-1]
    b[n-1] = b[n-1]/d[n-1]

    for k in range(n-2,-1,-1):
        b[k] = (b[k] - e[k]*b[k+1])/d[k]
    return b

def curvatures(xData,yData):
    
    n = len(xData) - 1
    c = np.zeros(n)
    d = np.ones(n+1)
    e = np.zeros(n)
    k = np.zeros(n+1)

    c[0:n-1] = xData[0:n-1] - xData[1:n]
    d[1:n] = 2.0*(xData[0:n-1] - xData[2:n+1])
    e[1:n] = xData[1:n] - xData[2:n+1]
    k[1:n] =6.0*(yData[0:n-1] - yData[1:n]) \
                 /(xData[0:n-1] - xData[1:n]) \
             -6.0*(yData[1:n] - yData[2:n+1])   \
                 /(xData[1:n] - xData[2:n+1])
    
    decomp (c,d,e)
    solve (c,d,e,k)

    return k

def evalSpline (xData, yData,k,x):  
    
    def findSegment(xData,x):
        
        iLeft = 0
        iRight = len(xData)- 1
        
        while 1:
            if (iRight-iLeft) <= 1: 
                return iLeft
            i = int ((iLeft + iRight)/2)
            if np.all(x < xData[i]): 
                iRight = i
            else: 
                iLeft = i

    i = findSegment(xData, x)
    h = xData[i] - xData[i+1]
    
    y = ((x - xData[i+1])**3/h - (x - xData[i+1])*h)*k[i]/6.0 \
      - ((x - xData[i])**3/h - (x - xData[i])*h)*k[i+1]/6.0   \
      + (yData[i]*(x - xData[i+1])                            \
       - yData[i+1]*(x - xData[i]))/h
    
    return y

# Set up serial connection (sesuaikan dengan port serial yang digunakan Arduino)
arduino = serial.Serial("/dev/cu.usbmodem14201", 9600)
time.sleep (2)

fig = plt.figure ()
ax = fig.add_subplot (111)

# Buat ploting secara realtime

def animate (i, dataList, port):
    arduinoData_string = port.readline().decode('ascii')

    try:
        arduinoData_float = float (arduinoData_string)
        dataList.append (arduinoData_float)
    except:
        pass

    dataList = dataList[-50:]

    ax.clear ()
    ax.plot (dataList, 'o', color='red', label="data")

    ax.set_ylim ([0, 1200])
    ax.set_title ('Arduino Data')
    ax.set_ylabel ('Nilai')

dataList = []
anime = animasi.FuncAnimation (fig, animate, frames=100, fargs=(dataList, arduino), interval=100)

plt.show ()
arduino.close ()
