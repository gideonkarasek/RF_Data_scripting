# ------------------------------------------
# Datetime formatter
# Author: Gideon Karasek
# Description: Prompts user to select files, ensures csv files have properly formatted date and time columns
# To Do: Add method to verify/force selected files to be csv
# ------------------------------------------

import pandas as pd
import numpy
from tkinter import filedialog
import os
from datetime import date


default_dir = os.getcwd()
file_selection = filedialog.askopenfilenames(initialdir=default_dir)

# column names, data collection error caused columns to be labeled wrong
column_names = ['date', 'frequency', 'fwd_power', 'ref_power', 'return_loss', 'phase']
df = pd.DataFrame(columns=column_names)

for item in file_selection:
    df1 = pd.read_csv(item, index_col=6)

    # fix misnamed columns, then populate main df with values from selected files
    df1.rename(columns={'date': 'empty', 'frequency': 'date', 'fwd_power': 'frequency', 'ref_power': 'fwd_power',
                        'return_loss': 'ref_power', 'phase': 'return_loss'}, inplace=True)
    
    df = pd.concat([df, df1], ignore_index=True)

# Splits date/time column, keeps datetime data object
df['time'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M:%S').dt.time
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M:%S').dt.strftime('%m/%d/%Y')

# save to new csv file, using current date in file name
df.to_csv(path_or_buf=f'Logs/Endurance Test Log {date.today().strftime("%Y%m%d")} Formatted for PowerBI.csv', mode='a')
