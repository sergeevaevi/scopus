import pandas as pd
import matplotlib.pyplot as plt

fixed_df = pd.read_csv('C:\Study\sc.csv')
plt.figure()
fixed_df["Год"].hist(color='gray', alpha=0.5, bins=50)
fixed_df["Год"].value_counts()

df3 = fixed_df.drop("Авторы", axis=1).join(fixed_df["Авторы"].str.rsplit("., ", expand=True).stack().reset_index(drop=True, level=1).rename('Names'))
nums = df3['Names'].reset_index()
nums = nums.drop("index", axis=1)
s_names_alp = nums.groupby("Names", sort = True).size()

a = s_names_alp.drop_duplicates()
s_names = nums["Names"].value_counts()
s1 = s_names.iloc[:10]
s2 = s_names.iloc[10:].sum()
s3 = s_names.iloc[10:].shape[0]
b = pd.Series([s2/s3], index=['other'])
s1 = s1.add(b, fill_value=0)
plt.pie(s1, labels=s1.index.values, autopct='%i%%')

fixed_df["Цитирования"].hist(color='k', alpha=0.5, bins=50)
df4 = fixed_df.groupby("Цитирования")
qo = fixed_df["Цитирования"].sum()
val = fixed_df.shape[0] 
imFac = qo/val

df5 = fixed_df.loc[fixed_df["Год"] >= 2018]
df6 = df5.groupby("Цитирования")
qo = df5["Цитирования"].sum()
val = df5.shape[0] 
imFac2 = qo/val

t2  = fixed_df.loc[fixed_df["Цитирования"] >= imFac] 
t2 = t2.sort_values(by = ['Цитирования'], ascending = [False])
t2['Цитирования'].hist()
