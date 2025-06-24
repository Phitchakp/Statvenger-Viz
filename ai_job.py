import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud


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

# WordCloud for Job Title
text_a = ' '.join(df['job_title'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_a)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud: Job Titles')
plt.tight_layout()
plt.show()


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

# 6. Scatter plot : year exp vs salary

# Set experience_level as an ordered categorical type
experience_order = ['EN', 'MI', 'SE', 'EX']
df['experience_level'] = pd.Categorical(df['experience_level'], categories=experience_order, ordered=True)

plt.figure()
sns.scatterplot(data=df, x='years_experience', y='salary_usd', hue='experience_level')
plt.title('Years of Experience vs Salary')
plt.xlabel('Years of Experience')
plt.ylabel('Salary (USD)')
plt.tight_layout()
plt.show()

# 7. Pivot Table     : mean_salary vs experience level vs company size
pivot_table = df.pivot_table(index='company_size', columns='experience_level', values='salary_usd', aggfunc='mean')
pivot_table = pivot_table.rename(columns=label_experience)

plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='YlGnBu')
plt.title('Mean Salary by Experience Level and Company Size')
plt.xlabel('Experience Level')
plt.ylabel('Company Size')
plt.tight_layout()
plt.show()

# 8. Pie chart : required_skill {vs experience level}
skills_experience = df.groupby('experience_level')['required_skills'].apply(lambda x: ','.join(x)).reset_index()
skills_experience['experience_label'] = skills_experience['experience_level'].map(label_experience)

# # Show pie for one experience level (e.g., Mid)
# from collections import Counter

# skills = ','.join(df[df['experience_level'] == 'MI']['required_skills']).split(',')
# skill_counts = Counter(skills)
# top_skills = dict(skill_counts.most_common(10))

# plt.figure()
# plt.pie(top_skills.values(), labels=top_skills.keys(), autopct='%1.1f%%')
# plt.title('Top Skills for Mid-Level Experience')
# plt.tight_layout()
# plt.show()

from collections import Counter
import matplotlib.pyplot as plt


# Combine all required skills into one list
all_skills = ','.join(df['required_skills']).split(',')

# Count the top 10 most common skills
skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(10))

# Plot a pie chart
plt.figure(figsize=(8, 8))
plt.pie(top_skills.values(), labels=top_skills.keys(), autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Required Skills Across All Experience Levels')
plt.tight_layout()
plt.show()

# 9. Bubble chart_A : company_location, + New Variable = Continent for each country (Color = Continent)
# from collections import Counter
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Step 1: Define a simplified mapping from country code to continent
# continent_map = {
#     'US': 'North America', 'GB': 'Europe', 'CA': 'North America', 'IN': 'Asia',
#     'DE': 'Europe', 'FR': 'Europe', 'AU': 'Oceania', 'CN': 'Asia',
#     'BR': 'South America', 'JP': 'Asia', 'KE': 'Africa', 'NG': 'Africa',
#     'ZA': 'Africa', 'SG': 'Asia', 'NL': 'Europe'
# }

# # Step 2: Add a new column "continent" based on company_location
# df['continent'] = df['company_location'].map(continent_map).fillna('Other')

# # Step 3: Count job postings per location and continent
# loc_counts = df.groupby(['company_location', 'continent']).size().reset_index(name='count')

# # Step 4: Create bubble chart
# plt.figure(figsize=(12, 6))
# sns.scatterplot(
#     data=loc_counts,
#     x='company_location',
#     y='count',
#     size='count',
#     hue='continent',
#     sizes=(100, 1000),
#     alpha=0.7
# )
# plt.title('Job Postings by Company Location and Continent')
# plt.xlabel('Company Location')
# plt.ylabel('Number of Jobs')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

import plotly.express as px

# # Count jobs per country
# job_counts_by_country = df['company_location'].value_counts().reset_index()
# job_counts_by_country.columns = ['country_code', 'job_count']

# # Choropleth map
# fig = px.choropleth(
#     job_counts_by_country,
#     locations='country_code',
#     color='job_count',
#     color_continuous_scale='Viridis',
#     title='Global Distribution of AI Jobs',
#     labels={'job_count': 'Number of Jobs'},
#     locationmode='ISO-3'  # ISO 2-letter or 3-letter codes — confirm your dataset format
# )

# fig.update_geos(showcoastlines=True, showland=True, showocean=True)
# fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
# fig.show()

import plotly.express as px

# Count jobs per country
job_counts_by_country = df['company_location'].value_counts().reset_index()
job_counts_by_country.columns = ['country', 'job_count']

# Plotly choropleth using country names
fig = px.choropleth(
    job_counts_by_country,
    locations='country',
    locationmode='country names',
    color='job_count',
    color_continuous_scale='Reds',
    title='Global Distribution of AI Jobs by Country',
    labels={'job_count': 'Number of Jobs'}
)

fig.update_geos(
    showcoastlines=True, 
    showland=True, 
    showocean=True,
    landcolor='white',
    showcountries=True,
    countrycolor='lightgray'    
    )
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0},
                  coloraxis_colorbar=dict(title='Jobs')
                  )
fig.show()


# 10. Bubble chart_B : industry vs company_location
# industry_loc_counts = df.groupby(['industry', 'company_location']).size().reset_index(name='count')

# plt.figure(figsize=(14, 6))
# sns.scatterplot(
#     data=industry_loc_counts,
#     x='industry',
#     y='company_location',
#     size='count',
#     sizes=(20, 800),
#     alpha=0.6
# )
# plt.title('Job Count by Industry and Company Location')
# plt.xlabel('Industry')
# plt.ylabel('Company Location')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()

# 11. ??? : experience level vs employment_type
# plt.figure(figsize=(8, 5))
# sns.countplot(data=df, x='experience_level', hue='employment_type')
# plt.title('Experience Level vs Employment Type')
# plt.xlabel('Experience Level')
# plt.ylabel('Count')
# plt.legend(title='Employment Type')
# plt.tight_layout()
# plt.show()

# 12. Word cloud : job_title, company_name
# from wordcloud import WordCloud

# text = ' '.join(df['job_title']) + ' ' + ' '.join(df['company_name'])

# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud: Job Titles and Company Names')
# plt.tight_layout()
# plt.show()



text_b = ' '.join(df['company_name'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_b)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud: Company Name')
plt.tight_layout()
plt.show()

