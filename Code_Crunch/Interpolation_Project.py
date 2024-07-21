
### Kelompok Huru Hara (2)
'''
    Salfa
    Kentdry
    Timo
    Riv
    Patricia
'''

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
from scipy.interpolate import CubicSpline
#import itertools

## =================== Decomp (materi bab 2) ================ ##

def decomp (c,d,e): #halaman 62
    n = len(d)
    
    for k in range(1,n):
        lam = c[k-1]/d[k-1]
        d[k] = d[k] - lam*e[k-1]
        c[k-1] = lam

    return c,d,e

## =================== solve (materi bab 2) ================ ##

def solve (c,d, e,b): # halaman 62

    n = len(d)

    for k in range(1,n):  # forward subs
        b[k] = b[k] - c[k-1]*b[k-1]
    
    b[n-1] = b[n-1]/d[n-1] # backward subs
    for k in range(n-2,-1,-1): 
        b[k] = (b[k] - e[k]*b[k+1])/d[k]
    
    return b

## =================== Curvatures (cari konstanta k) ================ ##

def curvatures(x_data, y_data):  #halaman 122
    
    n = len (x_data) - 1 # jumlah data
    c = np.zeros(n) # k(i-1) konstanta sebelumnya
    d = np.ones(n+1) # k(i) konstanta sekarang 
    e = np.zeros(n) # k(i+1) konstanta setelahnya
    k = np.zeros(n+1) # sesuatu 

    # Ax = b -> k adalah b | c,d,e adalah matrix A

    c[0:n-1] = x_data[0:n-1] - x_data[1:n]
    d[1:n] = 2.0*(x_data[0:n-1] - x_data[2:n+1])
    e[1:n] = x_data[1:n] - x_data[2:n+1]

    # Persamaan eq 3.11
    k[1:n] = 6.0*(y_data[0:n-1] - y_data[1:n]) \
                 /(x_data[0:n-1] - x_data[1:n]) \
             -6.0*(y_data[1:n] - y_data[2:n+1])   \
                 /(x_data[1:n] - x_data[2:n+1])
    
    decomp (c,d,e)
    solve (c,d,e,k)

    return k

## =================== EvalSpline cari nilai y (persamaan) ================ ##

def evalSpline (x_data, y_data, k, x):  # halaman 121
    
    def findSegment (x_data, x): # untuk mencari segmen dari nilai x yang diketahui,
                                 # yang ada di dalam matrix x_data
        
        iLeft = 0    # batas bawah i
        iRight = len(x_data)- 1 # batas atas i
        
        while 1:       # untuk menggeser range dan menemukan segmen yang diinginkan
            if (iRight-iLeft) <= 1: # jika panjang range i 
                return iLeft # maka nilainya adalah batas bawah
            
            i = int ((iLeft + iRight)/2) # i adalah nilai tengah dari range 
            if np.all(x < x_data[i]): 
                iRight = i # nilai batas atas = i
            else: 
                iLeft = i # nilai batas bawah = i

    i = findSegment (x_data, x)
    h = x_data[i] - x_data[i+1] # jarak antar data adalah sama sepanjang interval h
    
    # Persamaan eq 3.10

    y = ((x - x_data[i+1])**3/h - (x - x_data[i+1])*h)*k[i]/6.0 \
      - ((x - x_data[i])**3/h - (x - x_data[i])*h)*k[i+1]/6.0   \
      + (y_data[i]*(x - x_data[i+1])                            \
       - y_data[i+1]*(x - x_data[i]))/h
    
    return y

## ===================== Sample data random ==================== ##
x_data1 = np.arange (0, 50, 1)   
y_data1 = np.array ([14.3175479, 0.92054765, 23.2925276, -17.4986091,  -16.94932916,
 -11.58207327, -21.34536182,   6.38116242,   4.65650798,  11.21964583,
  12.26596314,  22.03675471,  -7.35525923,  15.14465718, -19.00408436,
  12.168594,    24.88687485,  24.24066932,  -7.55427387,  14.4985789,
  21.62865868,   3.29697108, -15.70601761,  -0.4708342,  -7.42030894,
  14.38162283,   6.63901545,  -5.88536424,  -2.69355842 -20.69116677,
  12.07207299,   1.04675634,   9.99446215,  14.98718849,  -7.33901069,
   6.74517357,   2.30202694, -10.31439548, -13.28513278,  14.23455895,
 -16.07237381,   9.6477658,  -20.65549708, -9.78003468, -15.66211802,
 -23.08019089, -22.1512766,   17.81518843, -10.16475258, -18.98586465, -10.0])
#y_data1 = np.array([random.uniform(-25, 25) for _ in range(len(x_data1))])

print (f"x data = {x_data1} | y data = {y_data1}\n")

# =================== Panggil Fungsi Spline dari Scipy ======================

y_eq_CS = CubicSpline (x_data1, y_data1) 

# =================== Panggil Fungsi Spline dari Kiusalas ===================

k = curvatures (x_data1, y_data1) # nilai k didapat dari fungsi curvatures di atas
x_eq = np.arange (0, 50, 0.1) # beda nya 0.1, biar grafik makin halus

y_eq_K = np.zeros_like (x_eq) # inisial kondisi y_eq = matrix 0 dengan
                              # ukuran seperti matrix x_eq
for i in range(len(x_eq)): # definisikan setiap y_eq index ke i
                           # dengan persamaan evalSpline
    y_eq_K[i] = evalSpline(x_data1, y_data1, k, x_eq[i])

## =================== Atribut untuk Plotting ================ ##

fig, ax = plt.subplots (2, 1, figsize=(9, 7.5))  # Mengubah ukuran agar lebih sesuai dengan layar

plot_data = []
plot_inter = []

for i in range(len(ax)):
    ax[i].set_xlim([min(x_data1) - 2, max(x_data1) + 2])
    ax[i].set_ylim([min(y_data1) - 5, max(y_data1) + 5])

    plot_data.append(ax[i].plot([], [], 'o', color='red', label='data')[0])
    plot_inter.append(ax[i].plot([], [], '-', color='black', label='inter')[0])

ax[1].set_title("Kiusalas", fontsize=25)
ax[0].set_title("Scipy", fontsize=25)

## =================== Function untuk melakukan animasi ================== ##

def animate(frame):

    plot_data[0].set_data(x_data1[:frame], y_data1[:frame])
    plot_inter[0].set_data(x_eq[:frame], y_eq_CS(x_eq[:frame]))

    plot_data[1].set_data(x_data1[:frame], y_data1[:frame])
    plot_inter[1].set_data(x_eq[:frame], y_eq_K[:frame])

    return plot_data + plot_inter

animasi = FuncAnimation(fig=fig, func=animate, interval=25, frames=len(x_eq), 
                        blit=True, repeat=True)

ax[0].legend (loc='best')
ax[1].legend (loc='best')
plt.show ()
