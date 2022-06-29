import datetime

import numpy as np
import pandas as pd


def process(df, window_size) -> pd.DataFrame:
    return _calculateAvg(df, window_size)


# For every window of x minutes will create a dataframe of [dates,duration]
# Will filter the selected records for corresponding window [dates,duration]
# calculates the moving average with rolling function [dates, avg]
# return a master dataframe of the output
def _calculateAvg(df, window_size) -> pd.DataFrame:
    df['dates'] = df['timestamp'].astype('datetime64[s]')
    df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d %H:%M:%S.%f')
    df2 = df[['dates', 'duration']]
    start_time = df2['dates'].dt.round('min').min()
    end_time = df2['dates'].dt.round('min').max()
    dummy_df = pd.DataFrame(pd.date_range(start=start_time - datetime.timedelta(minutes=1),
                                          end=end_time + datetime.timedelta(minutes=1), freq='min'),
                            columns=['dates'])
    all_df = pd.concat([df2, dummy_df])
    all_df = all_df.sort_values('dates')
    moving_average_df = all_df.rolling(str(window_size) + 'min', on='dates').mean().resample('1min', on='dates').first()
    return moving_average_df
