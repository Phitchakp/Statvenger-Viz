import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
from io import BytesIO

# Load dataset
df = pd.read_csv("ai_job_dataset.csv")

# --- Generate Plots ---

# 1. Mean Salary by Experience Level
mean_salary = df.groupby('experience_level')['salary_usd'].mean().reset_index()
fig_exp = px.bar(mean_salary, x='experience_level', y='salary_usd',
                 title='Mean Salary by Experience Level')

# 2. Mean Salary by Job Title (Top 10)
top_jobs = df.groupby('job_title')['salary_usd'].mean().sort_values(ascending=False).head(10).reset_index()
fig_jobs = px.bar(top_jobs, x='job_title', y='salary_usd',
                  title='Top 10 Job Titles by Salary')

# 3. Choropleth Map by Company Location
country_counts = df['company_location'].value_counts().reset_index()
country_counts.columns = ['country', 'job_count']
fig_map = px.choropleth(
    country_counts,
    locations='country',
    locationmode='country names',
    color='job_count',
    color_continuous_scale='Reds',
    title='Job Distribution by Country'
)
fig_map.update_geos(landcolor="white", showcountries=True, countrycolor="lightgray")

# 4. Word Cloud: Job Titles
job_title_text = ' '.join(df['job_title'])
job_wc_img = WordCloud(width=800, height=400, background_color='white').generate(job_title_text)

# 5. Word Cloud: Company Names
company_text = ' '.join(df['company_name'])
company_wc_img = WordCloud(width=800, height=400, background_color='white').generate(company_text)

# Convert WordClouds to image buffers
def fig_to_base64(wordcloud_fig):
    buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_fig, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()

job_wc_base64 = fig_to_base64(job_wc_img)
company_wc_base64 = fig_to_base64(company_wc_img)

# --- Dash App ---
app = dash.Dash(__name__)
app.title = "AI Job Dashboard"

app.layout = html.Div([
    html.H1("AI Job Market Dashboard", style={'textAlign': 'center'}),
    
    html.H2("1. Salary by Experience Level"),
    dcc.Graph(figure=fig_exp),

    html.H2("2. Top 10 Job Titles by Salary"),
    dcc.Graph(figure=fig_jobs),

    html.H2("3. Global Job Distribution"),
    dcc.Graph(figure=fig_map),

    html.H2("4. Word Cloud: Job Titles"),
    html.Img(src='data:image/png;base64,{}'.format(job_wc_base64), style={'width': '100%'}),

    html.H2("5. Word Cloud: Company Names"),
    html.Img(src='data:image/png;base64,{}'.format(company_wc_base64), style={'width': '100%'})
])

if __name__ == '__main__':
    app.run(debug=True)
