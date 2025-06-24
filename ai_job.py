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

# 1. Bar plot_A : mean_salary vs experience_level
label_experience = {
    'EN': 'Entry',
    'MI': 'Mid',
    'SE': 'Senior',
    'EX': 'Executive'
}

mean_salary_by_experience = df.groupby('experience_level')['salary_usd'].mean().sort_values().reset_index()
mean_salary_by_experience['experience_label'] = mean_salary_by_experience['experience_level'].map(label_experience)
print(mean_salary_by_experience.sort_values(by = 'salary_usd'))

plt.figure()
sns.barplot(data=mean_salary_by_experience, x='experience_label', y='salary_usd', palette='Blues_d')
plt.title('Mean Salary vs Experience Level')
plt.xlabel('Experience Level')
plt.ylabel('Mean Salary')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()





# # 3. Bar plot_C : mean_salary vs educattion_required
# mean_salary_by_education = df.groupby('education_required')['salary_usd'].mean().sort_values().reset_index()
# print(mean_salary_by_education.sort_values(by = 'salary_usd'))

# plt.figure()
# sns.barplot(data=mean_salary_by_education, x='education_required', y='salary_usd', palette='Set2')
# plt.title('Mean Salary vs Education')
# plt.xlabel('Education')
# plt.ylabel('Mean Salary')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# 2. Bar plot_D : mean_year exp vs expereice level
mean_yearexp_by_explevel = df.groupby('experience_level')['years_experience'].mean().sort_values().reset_index()
mean_yearexp_by_explevel['experience_label'] = mean_yearexp_by_explevel['experience_level'].map(label_experience)
print(mean_yearexp_by_explevel.sort_values(by = 'years_experience'))

plt.figure()
sns.barplot(data=mean_yearexp_by_explevel, x='experience_label', y='years_experience', palette='Set2')
plt.title('Mean Year Experience vs Experience Level')
plt.xlabel('Experience Level')
plt.ylabel('Mean Year Experience')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Bar plot_B : mean_salary vs job_title
# Calculate mean salary by job title
mean_salary_by_jobtitle = (
    df.groupby('job_title')['salary_usd']
    .mean()
    .reset_index()
    .sort_values(by='salary_usd', ascending=False)
)

# Plot the bar chart with full data
plt.figure(figsize=(12, 8))
sns.barplot(data=mean_salary_by_jobtitle, x='salary_usd', y='job_title', palette='Spectral')

# Set x-axis limits from 100,000 to 120,000
plt.xlim(100000, 120000)

plt.title('Mean Salary vs Job Title (Zoomed to $100k–$120k)')
plt.xlabel('Mean Salary (USD)')
plt.ylabel('Job Title')
plt.tight_layout()
plt.show()


# 4. Bar plot : industry vs mean_salary // experience level
# Calculate mean salary by industry
mean_salary_by_industry = (
    df.groupby('industry')['salary_usd']
    .mean()
    .reset_index()
    .sort_values(by='salary_usd', ascending=False)
)

# Plot the bar chart
plt.figure(figsize=(14, 8))
sns.barplot(data=mean_salary_by_industry, x='salary_usd', y='industry', palette='coolwarm')

# Set x-axis limits from 100,000 to 120,000
plt.xlim(100000, 120000)

plt.title('Mean Salary vs Industry (Zoomed to $100k–$120k)')
plt.xlabel('Mean Salary (USD)')
plt.ylabel('Industry')
plt.tight_layout()
plt.show()

# 5. Bar plot : industry vs experience level

# Count of experience levels per industry
mean_yearexp_by_industry = (df.groupby('industry')['years_experience']
    .mean()
    .reset_index()
    .sort_values(by='years_experience', ascending=False)
)
print(mean_yearexp_by_industry.sort_values(by = 'years_experience'))

# Plot a grouped bar chart
plt.figure(figsize=(16, 8))
sns.barplot(data=mean_yearexp_by_industry, x='years_experience', y='industry', palette='Set3')


plt.title('Experience Level Distribution Across Industries')
plt.xlabel('Years Experience')
plt.ylabel('Industry')
# plt.xticks(rotation=45, ha='right')
plt.legend(title='Experience Level')
plt.tight_layout()
plt.show()

