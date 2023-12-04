
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

plt.style.use ('fivethirtyeight')

x_val = []
y_val = []

index = count ()

def animation (i):
    
    data = pd.read_csv ('data.csv')
    x = data['x']
    y1 = data['y1']
    y2 = data['y2']

    #x_val.append (next(index)) # Count up 1 
    #y_val.append (random.randint (-4, 10))

    plt.cla () #Untuk clear out our axis saat update new line
    plt.plot (x, y1, 'r-', label="data 1")
    plt.plot (x, y2, 'g-', label="data 2")

    plt.legend (loc="best")
    plt.tight_layout ()

anime = FuncAnimation (plt.gcf(), animation, interval=300) #gcf (get current figure)

plt.tight_layout ()
plt.show ()