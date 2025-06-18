import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("ai_job_dataset.csv")


### Data Cleaning
print(df.info())
#print(df.isnull())
print(df[df.isnull().any(axis=1)])

plt.figure()
sns.boxplot(data=df, y='salary_usd')
plt.title('Boxplot')
# plt.show()
plt.close()

# Define bounds
Q1 = df['salary_usd'].quantile(0.25)
Q3 = df['salary_usd'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['salary_usd'] < lower_bound) | (df['salary_usd'] > upper_bound)]

print('upper_bound =' , upper_bound)
print(outliers.sort_values(by = 'salary_usd'))
    # "We cannot remove because this is a specific value"

df = df.drop_duplicates()
print(df)


### Graph

label_experience = {
    'EN': 'Entry',
    'MI': 'Mid',
    'SE': 'Senior',
    'EX': 'Executive'
}

mean_salary_by_experience = df.groupby('experience_level')['salary_usd'].mean().sort_values().reset_index()
print(mean_salary_by_experience.sort_values(by = 'salary_usd'))

mean_salary_by_experience['experience_label'] = mean_salary_by_experience['experience_level'].map(label_experience)


# Bar plot
plt.figure()
sns.barplot(data=mean_salary_by_experience, x='experience_label', y='salary_usd')
plt.title('Mean Salary vs Experience Level')
plt.xlabel('Experience Level')
plt.ylabel('Mean Salary')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

