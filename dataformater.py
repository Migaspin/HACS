import pandas as pd
import os

cwd = os.getcwd()

cwd = cwd + "\\data\\2022\\circulos.csv"

df = pd.read_csv(cwd)
df.to_csv(cwd)