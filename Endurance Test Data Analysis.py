# ------------------------------------------
# Endurance Test Data Analysis
# Author: Gideon Karasek
# Description: Imports data file produced by specific test, prints summary statistics and creates
#   matplotlib visualization; can be adjusted for specific column, default is forward RF power
# To Do: Add method to verify/force selected files to be csv
# ------------------------------------------

import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog
import os
import matplotlib.dates as mdates
import datetime


# causes filedialog to open in currently open folder
default_dir = os.getcwd()
file_selection = filedialog.askopenfilenames(initialdir=default_dir)

# Specify column names, create dataframe
column_names = ['date', 'frequency', 'fwd_power', 'ref_power', 'return_loss', 'phase']
df = pd.DataFrame(columns=column_names)

# iterate through selected files, set index to be date column, concatenate into main dataframe
for item in file_selection:
    df1 = pd.read_csv(item)
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'index': 'date'})
    df = pd.concat([df, df1], ignore_index=True)

# ensure date column keeps datetime datatype
df.date = pd.to_datetime(df.date)

# pick column to generate descriptive stats, set outlier limit; user input can be added here
use_col = 'column'
outlier_limit = 12500

# remove outliers based on specific column
df = df.loc[df['column'] < outlier_limit]

# print descriptive statistics, rounded to 2 decimal places
print(df['column'].describe().apply("{0:.2f}".format))

# create plot of data, format x-axis labels for cleaner appearance; y limits can be adjusted based on data being plotted
plt.figure(1, figsize=(30, 12))
ax = sns.lineplot(data=df, x='date', y='column')
ax.set(xlabel='Time', ylabel='column')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M:%S'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
ax.set_ylim([10500, 12500])
plt.xticks(rotation=90)
plt.tick_params(labelsize=14)

font = {'weight': 'bold',
        'size': 20}

plt.xlabel('Time', fontdict=font)
plt.ylabel('Forward Power', fontdict=font)

plt.grid()
plt.show()
