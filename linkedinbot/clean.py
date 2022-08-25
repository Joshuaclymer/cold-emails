import time
import pandas as pd
import numpy as np
from pandas.core.algorithms import isin

df = pd.read_csv('linkedin_cleaned.csv')
students = df.to_dict('records')
out = pd.DataFrame()
emailsAdded = []
emails = [s["Email"] for s in students]
for e in emails:
    if (emails.count(e) > 1):
        print("DUPLICATE:")
        print(e)
        break
for i in range(len(students)):
    student = students[i]
    email = student["Email"]
    if (email not in emailsAdded):
        dups = [s for s in students if s["Email"] == email]
        nonNullCount = [len([field for field in d.values() if not pd.isnull(field)]) for d in dups]
        bestOne = dups[nonNullCount.index(max(nonNullCount))]
        if (len(dups) > 1):
            print(nonNullCount)
            print(bestOne)
            break
        out.append(bestOne, ignore_index = True)
        emailsAdded.append(email)
# for i in range(len(students)):
#     student = students[i]
#     if (student["Year"] != np.nan and (student["Year"] < 1 or student["Year"] > 4)):
#         df.at[i, "Major"] = np.nan
#         df.at[i, "Year"] = np.nan
#         df.at[i, "GPA"] = np.nan
#     if (student["GPA"] != np.nan and not isinstance(student["GPA"], float)):
#         df.at[i, "GPA"] = np.nan
#     if (student["Major"] != np.nan and not isinstance(student["Major"], str)):
#         df.at[i, "Major"] = np.nan
#     if (student["Year"] != np.nan and not isinstance(student["Year"], float)):
#         df.at[i, "Year"] = np.nan
#     if (student["Address"] != np.nan and student["Address"] == '\xa0'):
#         df.at[i, "Address"] = np.nan

# df.to_csv(r"./linkedin_cleaned.csv", encoding='utf-8', index=False)