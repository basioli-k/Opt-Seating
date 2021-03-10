from optimal_seating import optimal_seating
import os
import pandas as pd

if __name__ == '__main__':

    directory = r'./test_examples'
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            path = f"{directory}/{filename}"
            df = pd.read_csv(path)
            try:
                for i in range(10):
                    optimal_seating(df)
            except AssertionError:
                print("Greške se događaju, u redu je :)")
        else:
            continue