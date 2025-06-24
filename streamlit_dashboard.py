# ai_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import io

st.set_page_config(page_title="AI Job Dashboard", layout="wide")

# Load data
df = pd.read_csv("ai_job_dataset.csv")
df = df.drop_duplicates()

label_experience = {'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Executive'}
experience_order = ['EN', 'MI', 'SE', 'EX']
df['experience_level'] = pd.Categorical(df['experience_level'], categories=experience_order, ordered=True)

st.title("📊 AI Job Market Dashboard")

# --- Section: Word Clouds ---
st.header(" Word Cloud: Job Titles")
job_text = ' '.join(df['job_title'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(job_text)
fig10, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig10)

# --- Section 1: Mean Salary vs Experience Level ---
st.header("1. Mean Salary by Experience Level")
mean_salary = (
    df.groupby('experience_level')['salary_usd']
    .mean().sort_values()
    .reindex(experience_order)  # ✅ ensures correct order
    .reset_index()
)

mean_salary['experience_label'] = mean_salary['experience_level'].map(label_experience)

fig1 = px.bar(mean_salary, x='experience_label', y='salary_usd',
              title='Mean Salary by Experience Level', color='salary_usd',
              color_continuous_scale='Blues')
st.plotly_chart(fig1, use_container_width=True)

# --- Section 2: Mean Years of Experience by Experience Level ---
st.header("2. Mean Years of Experience by Experience Level")
mean_exp = df.groupby('experience_level')['years_experience'].mean().reset_index()
mean_exp['experience_label'] = mean_exp['experience_level'].map(label_experience)
fig2 = px.bar(mean_exp, x='experience_label', y='years_experience',
              title='Mean Years of Experience vs Experience Level', color='years_experience',
              color_continuous_scale='Blues')
st.plotly_chart(fig2, use_container_width=True)

# --- Section 3: Mean Salary vs Job Title (Filtered) ---
st.header("3. Mean Salary vs Job Title ($100k–$120k)")
job_salary = df.groupby('job_title')['salary_usd'].mean().sort_values().reset_index()
filtered_job_salary = job_salary[(job_salary['salary_usd'] >= 100000) & (job_salary['salary_usd'] <= 120000)]
fig3 = px.bar(filtered_job_salary.sort_values(by='salary_usd', ascending=False),
              x='salary_usd', y='job_title', orientation='h',
              title='Mean Salary vs Job Title ($100k–$120k)', color='salary_usd',
              color_continuous_scale='Spectral')

# Set x-axis range
fig3.update_xaxes(range=[100000, 120000])
st.plotly_chart(fig3, use_container_width=True)

# --- Section 4: Mean Salary vs Industry ---
st.header("4. Mean Salary vs Industry ($100k–$120k)")
industry_salary = df.groupby('industry')['salary_usd'].mean().sort_values().reset_index()
filtered_industry = industry_salary[(industry_salary['salary_usd'] >= 100000) & (industry_salary['salary_usd'] <= 120000)]
fig4 = px.bar(filtered_industry.sort_values(by='salary_usd', ascending=False),
              x='salary_usd', y='industry', orientation='h',
              title='Mean Salary vs Industry ($100k–$120k)', color='salary_usd',
              color_continuous_scale='Blues')

# Set x-axis range
fig4.update_xaxes(range=[100000, 120000])

st.plotly_chart(fig4, use_container_width=True)

# --- Section 5: Avg. Years of Experience per Industry ---
st.header("5. Avg. Years of Experience per Industry")
exp_by_industry = df.groupby('industry')['years_experience'].mean().sort_values().reset_index()
fig5 = px.bar(exp_by_industry.sort_values(by='years_experience', ascending=False),
              x='years_experience', y='industry', orientation='h',
              title='Avg. Years of Experience per Industry', color='years_experience',
              color_continuous_scale='Blues')
st.plotly_chart(fig5, use_container_width=True)

# --- Section 6: Scatter Plot of Years Experience vs Salary ---
st.header("6. Years of Experience vs Salary")
experience_order = ['EN', 'MI', 'SE', 'EX']
df['experience_level'] = pd.Categorical(df['experience_level'], categories=experience_order, ordered=True)
fig6 = px.scatter(df, x='years_experience', y='salary_usd', color='experience_level',
                  title='Years of Experience vs Salary')
st.plotly_chart(fig6, use_container_width=True)

# --- Section 7: Heatmap of Mean Salary by Company Size & Experience Level ---
st.header("7. Salary Heatmap: Company Size vs Experience Level")
pivot_table = df.pivot_table(index='company_size', columns='experience_level',
                             values='salary_usd', aggfunc='mean').rename(columns=label_experience)
fig7, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='YlGnBu', ax=ax)
st.pyplot(fig7)

# --- Section 8: Top Skills Pie Chart ---
st.header("8. Top 10 Required Skills")
all_skills = ','.join(df['required_skills']).split(',')
skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(10))
fig8, ax = plt.subplots(figsize=(8, 8))
ax.pie(top_skills.values(), labels=top_skills.keys(), autopct='%1.1f%%', startangle=140)
ax.set_title('Top 10 Required Skills')
st.pyplot(fig8)

# --- Section 9: Global Job Distribution (Choropleth) ---
st.header("9. Global Distribution of AI Jobs")
country_counts = df['company_location'].value_counts().reset_index()
country_counts.columns = ['country', 'job_count']
fig9 = px.choropleth(country_counts, locations='country', locationmode='country names',
                     color='job_count', color_continuous_scale='Reds',
                     title='AI Jobs by Country', labels={'job_count': 'Jobs'})
fig9.update_geos(showcoastlines=True, showland=True, landcolor='white',
                 showcountries=True, countrycolor='lightgray')

fig9.update_layout(
    height=700,
    width=1000,
    margin={"r":0,"t":50,"l":0,"b":0},
    coloraxis_colorbar=dict(title='Jobs'))

st.plotly_chart(fig9, use_container_width=True)



st.header("Word Cloud: Company Names")
company_text = ' '.join(df['company_name'])
wordcloud2 = WordCloud(width=800, height=400, background_color='white').generate(company_text)
fig11, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud2, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig11)
