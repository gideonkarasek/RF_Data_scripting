# ------------------------------------------
# CSV file combiner
# Author: Gideon Karasek
# Created: ‎Thursday, ‎September ‎5, ‎2024, ‏‎3:13:27 PM
# Description: Prompts user to select files, imports/concatenates files into one data frame,
#   saves out to csv file with user specified name
# To Do: Add method to verify/force selected files to be csv
# ------------------------------------------

import pandas as pd
from tkinter import filedialog
import os
import time


default_dir = os.getcwd() # causes filedialog to open in currently open folder
file_selection = filedialog.askopenfilenames(initialdir=default_dir) # gives a list of file names

df = pd.DataFrame()  # columns=column_names can be used if specific columns are desired; must define column_names as a list
x = 0

# iterate through all selected files, concatenate each file onto main dataframe to be saved
for item in file_selection:
    start = time.time()
    x += 1
    df1 = pd.read_csv(item) # temp dataframe, only used to concatenate csv into main dataframe
    df = pd.concat([df, df1])
    print(f'Concatenation #{x} Done in {time.time() - start} seconds')

# Extract time (HH:MM:SS) from date/time column, not always needed
'''
print('Extracting time from date/time column...\n')
df['time'] = pd.to_datetime(df['date'].astype('datetime64[ns]'), format='%m/%d/%Y %I:%M:%S.%f %p').dt.time
'''

# Designate file path, ask for file name and save to given path using append, not write
filepath_header = 'C:/Users/gkarasek/Desktop/PTL Testing/EandS Testing/temp'
print('Enter file name: ')
file_to_save = input()
# Will only create a new file if file path does not exist, otherwise adds to end of old file
df.to_csv(path_or_buf=f'{filepath_header}/{file_to_save}.csv', mode='a')

