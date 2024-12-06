import pandas as pd
og = pd.read_csv('original.csv')
sp = pd.read_csv('supplementary.csv')
com = set(og.columns) & set(sp.columns)
og_data = og[list(com)]
sp_data = sp[list(com)]
sampled = sp_data.sample(n=5000)
combined = pd.concat([og_data, sampled], axis=0, ignore_index=True)
combined.to_csv('base.csv', index=False)
print("Saved")