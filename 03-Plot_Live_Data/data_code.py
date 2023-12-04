
import csv #buat bikin file csv
import random
import time

x_val = 0
y_tot_1 = 1300
y_tot_2 = 1300

header = ['x', 'y1', 'y2']

with open ('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter (csv_file, fieldnames=header)
    csv_writer.writeheader ()

while True:
    with open ('data.csv', 'a') as csv_file:
        
        csv_writer = csv.DictWriter (csv_file, fieldnames=header) #format nulis dalam dictionary
        dict_info = {
            'x' : x_val,
            'y1' : y_tot_1,
            'y2' : y_tot_2 
        }

        csv_writer.writerow (dict_info) #baris
        print (x_val, y_tot_1, y_tot_2)

        x_val += 1
        y_tot_1 += random.randint (-5, 10)
        y_tot_2 += random.randint (-3, 7)

    time.sleep (1)



