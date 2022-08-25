import pandas as pd
import numpy as np
df = pd.read_csv('linkedin_info_3.csv')
deps = []
for i in range(df.shape[0]):
    dep = df.loc[i, "Major"]
    if (dep != np.nan):
        deps += [dep]
counts = {"test": 0}
for dep in deps:
    counts[dep] = deps.count(dep)
countsOrdered = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])[::-1]}
print(countsOrdered)
print("sum:")
total = sum(list(countsOrdered.values())[1:])
print(total)
print({k: v/total for k, v in sorted(counts.items(), key=lambda item: item[1])[::-1]})