import pandas as pd
df = pd.read_csv('raw_eco_india.csv')

print("====DATASET SHAPE====")
print(f"Total Rows: {df.shape[0]} | Total Columns: {df.shape[1]}\n")

print("====MISSING VALUES====")
print(df.isnull().sum(), "\n")

print("====DATA INFO====")
df.info()
print("\n")

print("====TOP 5 ROWS====")
print(df.head())

print("====TOP 5 TAIL====")
print(df.tail())
