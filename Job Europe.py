import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("emed_careers_eu.csv")
# print(df.info())
print(df["category"].value_counts())
df2 = df[["category", "location"]]
print(df2[df2["category"]=="Switzerland"])
print(df2[(df2["category"] == "Switzerland") & (df2["location"] == "switzerland")])
