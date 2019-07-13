import pandas as pd
import matplotlib.pyplot as plt

fixed_df = pd.read_csv('C:\Study\sc.csv')
plt.figure()
fixed_df["Год"].plot.hist(color='gray', alpha=0.5, bins=50, title = 'Статей/Год')
fixed_df["Год"].value_counts()
#отделяем авторов каждой статьи
df_a = fixed_df.drop("Авторы", axis=1).join(fixed_df["Авторы"].str.rsplit("., ", expand=True).stack().reset_index(drop=True, level=1).rename('Статей'))
nums = df_a['Статей'].reset_index()
nums = nums.drop("index", axis=1)
s_names = nums["Статей"].value_counts()
#находим топ-10
df_best_10 = s_names.iloc[:10]
#сумму остальных
sum_other = s_names.iloc[10:].sum()
#полное количество
count_all = s_names.iloc[10:].shape[0]
b = pd.Series([sum_other/count_all], index=['other'])
df_articles = df_best_10.add(b, fill_value=0)
plt.pie(df_articles, labels=df_articles.index.values, autopct='%i%%')

fixed_df["Цитирования"].plot.hist(color='gray', alpha=0.5, bins=50, title = 'Цитируемость статей ДВФУ')
sum_quotes = fixed_df["Цитирования"].sum()
count_quotes = fixed_df.shape[0]
imFac_all = sum_quotes/count_quotes
imFac_all
df_after_2018 = fixed_df.loc[fixed_df["Год"] >= 2018]
sum_quotes = df_after_2018["Цитирования"].sum()
count_quotes = df_after_2018.shape[0]
imFac_after_2018 = sum_quotes/count_quotes
imFac_after_2018

df_quoted = fixed_df.loc[fixed_df["Цитирования"] >= imFac_all]
df_quoted = df_quoted.sort_values(by = ['Цитирования'], ascending = [False])

df_best_quoted = df_quoted.iloc[:10][['Цитирования','Авторы']]
sum_quotes = df_quoted.iloc[10:]['Цитирования'].sum()
count_quotes = df_quoted.iloc[10:]['Цитирования'].shape[0]
#добавим значение
df_best_quoted.loc[10] = [sum_quotes/count_quotes, 'other']
df_best_quoted = df_best_quoted.drop("Авторы", axis=1).join(df_best_quoted["Авторы"].str.rsplit("., ", expand=True).stack().reset_index(drop=True, level=1).rename('Авторы'))
df_best_quoted = df_best_quoted.drop_duplicates(["Цитирования"])

a = df_best_quoted['Цитирования'].groupby(df_best_quoted['Авторы']).sum()
a.plot.pie(y='Цитирования', title = 'Цитирования')
