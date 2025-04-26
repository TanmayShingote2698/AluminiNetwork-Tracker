import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, send_file
import folium
from folium.plugins import MarkerCluster
from io import BytesIO
import os

# Initialize Flask app
app = Flask(__name__)

# Load alumni data from CSV file
df = pd.read_csv('alumni_data.csv')

# Generate gender distribution plot
def generate_gender_distribution():
    gender_counts = df['gender'].value_counts()
    fig = px.pie(names=gender_counts.index, values=gender_counts.values, title="Gender Distribution")
    gender_file_path = 'static/gender_distribution.png'
    fig.write_image(gender_file_path)
    return gender_file_path

# Generate graduation year distribution plot
def generate_graduation_year_distribution():
    year_counts = df['graduation_year'].value_counts().sort_index()
    fig = px.bar(year_counts, x=year_counts.index, y=year_counts.values, title="Graduation Year Distribution", labels={'x': 'Year', 'y': 'Count'})
    graduation_year_file_path = 'static/graduation_year_distribution.html'
    fig.write_html(graduation_year_file_path)
    return graduation_year_file_path

# Generate career path distribution plot
def generate_career_path_distribution():
    career_counts = df['career_path'].value_counts()
    fig = px.bar(career_counts, x=career_counts.index, y=career_counts.values, title="Career Path Distribution", labels={'x': 'Career Path', 'y': 'Count'})
    career_path_file_path = 'static/career_path_distribution.html'
    fig.write_html(career_path_file_path)
    return career_path_file_path

# Generate top employers plot
def generate_top_employers_distribution():
    employer_counts = df['top_employer'].value_counts().head(10)
    fig = px.bar(employer_counts, x=employer_counts.index, y=employer_counts.values, title="Top Employers", labels={'x': 'Employer', 'y': 'Count'})
    top_employers_file_path = 'static/top_employers_distribution.html'
    fig.write_html(top_employers_file_path)
    return top_employers_file_path

# Generate geographical distribution map
def generate_geographical_distribution():
    # Filter out rows where latitude or longitude is NaN
    df_cleaned = df.dropna(subset=['latitude', 'longitude'])

    geo_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Center the map at India
    marker_cluster = MarkerCluster().add_to(geo_map)
    
    for _, row in df_cleaned.iterrows():  # Iterate through the cleaned data
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(marker_cluster)
    
    geo_map_file_path = 'static/geographical_distribution_map.html'
    geo_map.save(geo_map_file_path)  # Save the map as HTML file
    return geo_map_file_path

# Route to the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to the analytics page
@app.route('/analytics')
def analytics():
    gender_distribution_path = generate_gender_distribution()
    graduation_year_path = generate_graduation_year_distribution()
    career_path_path = generate_career_path_distribution()
    top_employers_path = generate_top_employers_distribution()
    geographical_path = generate_geographical_distribution()
    
    return render_template('analytics.html', 
                           gender_distribution_path=gender_distribution_path,
                           graduation_year_path=graduation_year_path,
                           career_path_path=career_path_path,
                           top_employers_path=top_employers_path,
                           geographical_path=geographical_path)

# Route to export the data as a CSV
@app.route('/export')
def export():
    # Convert DataFrame to CSV and send it as a file
    csv = df.to_csv(index=False)
    return send_file(BytesIO(csv.encode()), as_attachment=True, download_name='alumni_data.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
