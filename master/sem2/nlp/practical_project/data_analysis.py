import pandas as pd

df = pd.read_csv('./data/PMC-Patients.csv')
print(f"Found {len(df)} entries")

print(df.columns)

print(df[:10]["similar_patients"])
