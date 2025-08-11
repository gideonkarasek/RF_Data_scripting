# ------------------------------------------
# Endurance Test Data Analysis
# Author: Gideon Karasek
# Created: Friday, ‎November ‎1, ‎2024, ‏‎3:23:11 PM
# Description: Imports csv file, selects desired column, resamples values to create a new dataframe
#   with min/max values from each minute of data; can be adjusted to change resample period/calculation,
#   or to focus on a different column of data
# To Do: Add method to verify/force selected files to be csv
# ------------------------------------------

import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog
import os
import matplotlib.dates as mdates
from datetime import date
import math
import datetime


# tells pandas to display floats rounded to 2 decimal places
pd.set_option('display.float_format', lambda x: '%.2f' % x)
# hides 'Setting with a copy' warning from pandas in terminal output
pd.options.mode.chained_assignment = None

# causes filedialog to open in currently open folder
default_dir = os.getcwd()
file_selection = filedialog.askopenfilenames(initialdir=default_dir)

# set column names, initailize dataframe
column_names = ['date', 'frequency', 'fwd_power', 'ref_power', 'return_loss', 'phase', 'time']
df = pd.DataFrame(columns=column_names)

# iterate through list of selected files, concatenate into main dataframe
for item in file_selection:
    df1 = pd.read_csv(item)
    # extract date column from index
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'index': 'date'})
    df = pd.concat([df, df1], ignore_index=True)

# after populating entire dataframe, ensure date column is datetime datatype
df.date = pd.to_datetime(df.date)

# remove outliers, can be changed based on column of interest/parameters
df = df.loc[df['fwd_power'] < 12500]

to_group = df[['fwd_power', 'date']]

to_group = to_group.set_index('date')

# resamples values, selecting calculated value from specified resample period
grouped_df_min = to_group.resample('1min').min() # creates new df, observations are minimum recorded value in each minute
grouped_df_min = grouped_df_min.rename(columns={'fwd_power': 'min_fwd_power'})
grouped_df_max = to_group.resample('1min').max() # creates new df, observations are maximum recorded value in each minute
grouped_df_max = grouped_df_max.rename(columns={'fwd_power': 'max_fwd_power'})

grouped_df = pd.concat([grouped_df_min, grouped_df_max], axis=1) # concatenate resampled dataframes along the columns, gives new df with 2 columns + index

# save final dataframe to csv, user input to name file
filepath_header = 'C:/Users/gkarasek/Desktop/PTL Testing/EandS Testing/temp'
print('Enter file name: ')
file_to_save = input()
grouped_df.to_csv(path_or_buf=f'{filepath_header}/{file_to_save}.csv', mode='a')

