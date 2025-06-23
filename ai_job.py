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
sns.barplot(data=mean_salary_by_experience, x='experience_label', y='salary_usd')
plt.title('Mean Salary vs Experience Level')
plt.xlabel('Experience Level')
plt.ylabel('Mean Salary')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Bar plot_B : mean_salary vs job_title
mean_salary_by_jobtitle = df.groupby('job_title')['salary_usd'].mean().sort_values().reset_index()
print(mean_salary_by_jobtitle.sort_values(by = 'salary_usd'))

plt.figure()
sns.barplot(data=mean_salary_by_jobtitle, x='job_title', y='salary_usd')
plt.title('Mean Salary vs Job Title')
plt.xlabel('job Title')
plt.ylabel('Mean Salary')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Bar plot_C : mean_salary vs educattion_required
mean_salary_by_education = df.groupby('education_required')['salary_usd'].mean().sort_values().reset_index()
print(mean_salary_by_education.sort_values(by = 'salary_usd'))

plt.figure()
sns.barplot(data=mean_salary_by_education, x='education_required', y='salary_usd')
plt.title('Mean Salary vs Education')
plt.xlabel('Education')
plt.ylabel('Mean Salary')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Bar plot_D : mean_year exp vs expereice level

# 5. Bar plot : industry vs mean_salary // experience level

# 6. Scatter plot : year exp vs salary

# 7. ED Isoserface : mean_salary vs experience level vs company size

# 8. Pie chart : required_skill {vs experience level}

# 9. Bubble chart_A : company_location, + New Variable = Continent for each country (Color = Continent)

# 10. Bubble chart_B : industry vs company_location

# 11. ??? : experience level vs employment_type

# 12. Word cloud : job_title, company_name





