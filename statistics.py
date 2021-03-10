import pandas as pd
import numpy as np
import os

if __name__ == '__main__':

    directory = r'./results'

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            df = pd.read_csv(f'./results/{filename}', usecols=['used', 'total', 'time', 'success'], low_memory=True)
            used = np.array(df['used'])
            total = np.array(df['total'])
            time = np.array(df['time'])
            success = np.array(df['success'])
            print(np.average(used[success]))
            print(np.mean(used[success]))
            print(np.average(time[success]))
            print(np.mean(time[success]))
            print(np.sum(success), "out of", len(success))
        else:
            continue
