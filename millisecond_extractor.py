# ------------------------------------------
# Endurance Test Data Analysis
# Author: Gideon Karasek
# Created: Thursday, ‎September ‎5, ‎2024, ‏‎4:30:21 PM
# Description: Imports data file produced by specific test, extracts milliseconds from time column
# To Do: Add method to verify/force selected files to be csv
# ------------------------------------------

import pandas as pd
from tkinter import filedialog
import os


# causes filedialog to open in currently open folder
default_dir = os.getcwd()
file_selection = filedialog.askopenfilename(initialdir=default_dir) # only allows for one file to be selected

df = pd.read_csv(file_selection)

# ensure time column is datetime datatype, specify format and create new column assigned to value of milliseconds
df['Milliseconds'] = pd.to_datetime(df['time'].astype('datetime64[ns]'), format='%H:%M:%S.%f').dt.strftime("%f")

df['Milliseconds'] = df['Milliseconds'].astype(int)

# filter out values not needed, save to csv with file name based on original file
df_final = df.loc[(df['Milliseconds'] % 10000 == 0)]
df_final.to_csv(path_or_buf=f'{file_selection[:-4]}_final.csv', mode='w') # drops .csv from file name, adds _final.csv to save

# print confirmation of script finishing in terminal
print('Milliseconds extracted, file saved as:\n' + f'{file_selection[:-4]}_final.csv')

