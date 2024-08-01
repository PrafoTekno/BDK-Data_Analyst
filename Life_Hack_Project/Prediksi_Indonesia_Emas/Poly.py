
import logging as log
import numpy as np
import matplotlib.pyplot as plt
import math as mt

log.basicConfig (level=log.ERROR)
log.error ('Matrix is singular')

def Tukar (matrix, a, b):
    matrix[[a, b]] = matrix[[b, a]]

def GaussPivot (a, b, tol=1.0e-12):

    n = len(b)
  # Set up scale factors
    s = np.zeros(n)

    for i in range(n):
        s[i] = max(np.abs(a[i,:]))

    for k in range(0,n-1):

      # Row interchange, if needed
        p = np.argmax(np.abs(a[k:n,k])/s[k:n]) + k

        if abs(a[p,k]) < tol: 
            log.error('Matrix is singular')
        if p != k:
            Tukar(b,k,p)
            Tukar(s,k,p)
            Tukar(a,k,p)

      # Elimination
        for i in range(k+1,n):
            if a[i,k] != 0.0:
                lam = a[i,k]/a[k,k]
                a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
                b[i] = b[i] - lam*b[k]

    if abs(a[n-1,n-1]) < tol: 
        log.error('Matrix is singular')
                                        
  # Back substitution
    b[n-1] = b[n-1]/a[n-1,n-1]

    for k in range(n-2,-1,-1):
        b[k] = (b[k] - np.dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    return b

def polyFit(xData, yData, m):
    
    a = np.zeros((m+1,m+1))
    b = np.zeros(m+1)
    s = np.zeros(2*m+1)

    for i in range(len(xData)):
        temp = yData[i]
        for j in range(m+1):
            b[j] = b[j] + temp
            temp = temp*xData[i]
        temp = 1.0

        for j in range(2*m+1):
            s[j] = s[j] + temp
            temp = temp*xData[i]

    for i in range(m+1):
        
        for j in range(m+1):
            a[i,j] = s[i+j]
        
    return GaussPivot (a, b)

def stdDev(c,xData,yData):

    def evalPoly(c,x):

        m = len(c) - 1
        p = c[m]
        for j in range(m):
            p = p*x + c[m-j-1]
        return p
    
    n = len(xData) - 1
    m = len(c) - 1
    sigma = 0.0
    
    for i in range(n+1):
        p = evalPoly(c,xData[i])
        sigma = sigma + (yData[i] - p)**2
        
    sigma = mt.sqrt(sigma/(n - m))

    return sigma

def plotPoly (xData,yData,coeff,xlab,ylab):
             
    m = len(coeff)
    x1 = min(xData)
    x2 = max(xData)
    dx = (x2 - x1)/20.0
    x = np.arange(x1,x2 + dx/10.0,dx)
    y = np.zeros((len(x)))*1.0

    for i in range(m):
        y = y + coeff[i]*x**i
        
    plt.scatter (xData, yData, color="red", label="data")
    plt.plot (x, y, color="green", label="fitting")

    plt.xlabel (xlab)
    plt.ylabel (ylab)
    plt.grid (True)

    plt.legend (loc="best")
    plt.show()