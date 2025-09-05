import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# Embedded CSV data as a string (replace with actual file path if needed)
csv_data_path = r'/Users/pankajti/dev/git/fedreserve_data_research/frdr/analysis/events.csv'
# Load data into a pandas DataFrame
df = pd.read_csv(csv_data_path)

# Convert DATE to datetime and extract year
df['DATE'] = pd.to_datetime(df['DATE'])
df['year'] = df['DATE'].dt.year

# Derive fields
df['rateDifference'] = df['Yield'] - df['FedFundsRate']
df =df.dropna()


# Shorten speaker names for labels
speakers_dict = {
    "Chairman Jerome H. Powell": ("Jerome H. Powell", "Chairman"),
    "Vice Chairman for Supervision Randal K. Quarles": ("Randal K. Quarles", "Vice Chairman for Supervision"),
    "Governor Lael Brainard": ("Lael Brainard", "Governor"),
    "Vice Chairman Richard H. Clarida": ("Richard H. Clarida", "Vice Chairman"),
    "Vice Chairman for Supervision and Chair of the Financial Stability Board Randal K. Quarles": ("Randal K. Quarles", "Vice Chairman for Supervision and Chair of the Financial Stability Board"),
    "Governor Michelle W. Bowman": ("Michelle W. Bowman", "Governor"),
    "Vice Chair Richard H. Clarida": ("Richard H. Clarida", "Vice Chair"),
    "Chair Jerome H. Powell": ("Jerome H. Powell", "Chair"),
    "Vice Chair for Supervision and Chair of the Financial Stability Board Randal K. Quarles": ("Randal K. Quarles", "Vice Chair for Supervision and Chair of the Financial Stability Board"),
    "Vice Chair for Supervision Randal K. Quarles": ("Randal K. Quarles", "Vice Chair for Supervision"),
    "Governor Christopher J. Waller": ("Christopher J. Waller", "Governor"),
    "Governor Randal K. Quarles": ("Randal K. Quarles", "Governor"),
    "Chair Pro Tempore Jerome H. Powell": ("Jerome H. Powell", "Chair Pro Tempore"),
    "Vice Chair Lael Brainard": ("Lael Brainard", "Vice Chair"),
    "Governor Philip N. Jefferson": ("Philip N. Jefferson", "Governor"),
    "Governor Lisa D. Cook": ("Lisa D. Cook", "Governor"),
    "Vice Chair for Supervision Michael S. Barr": ("Michael S. Barr", "Vice Chair for Supervision"),
    "Vice Chair Philip N. Jefferson": ("Philip N. Jefferson", "Vice Chair"),
    "Governor Adriana D. Kugler": ("Adriana D. Kugler", "Governor"),
    "Governor Michael S. Barr": ("Michael S. Barr", "Governor")
}

speaker_map = {
    'Chairman Jerome H. Powell': 'J. Powell',
    'Vice Chairman for Supervision Randal K. Quarles': 'R. Quarles',
    'Governor Lael Brainard': 'L. Brainard',
    'Vice Chair Richard H. Clarida': 'R. Clarida',
    'Governor Michelle W. Bowman': 'M. Bowman',
    'Governor Christopher J. Waller': 'C. Waller',
    'Vice Chair Philip N. Jefferson': 'P. Jefferson',
    'Governor Lisa D. Cook': 'L. Cook',
    'Governor Adriana D. Kugler': 'A. Kugler',
    'Vice Chair for Supervision Michael S. Barr': 'M. Barr'
}
df['shortSpeaker'] = df['speaker'].map(lambda x: speakers_dict.get(x.strip(), x)[0])


# Determine dominant topic
df['dominantTopic'] = df[['inflation', 'employment', 'other']].idxmax(axis=1).str.capitalize()

# Visualization 1: Line Chart - Yield and Fed Funds Rate Over Time
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['DATE'], y=df['Yield'], mode='lines', name='Yield', line=dict(color='#3B82F6', width=2)))
fig1.add_trace(go.Scatter(x=df['DATE'], y=df['FedFundsRate'], mode='lines', name='Fed Funds Rate', line=dict(color='#EF4444', width=2)))
fig1.update_layout(
    title='Yield and Fed Funds Rate Over Time',
    xaxis_title='Date',
    yaxis_title='Rate (%)',
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig1.write_image("yield_fedfunds_rate.png", width=800, height=400, scale=2)

# Visualization 2: Stacked Area Chart - Emphasis Over Time (Yearly Average)
yearly_data = df.groupby('year')[['inflation', 'employment', 'other']].mean().reset_index()
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=yearly_data['year'], y=yearly_data['inflation'], stackgroup='one', name='Inflation', line=dict(color='#FBBF24')))
fig2.add_trace(go.Scatter(x=yearly_data['year'], y=yearly_data['employment'], stackgroup='one', name='Employment', line=dict(color='#34D399')))
fig2.add_trace(go.Scatter(x=yearly_data['year'], y=yearly_data['other'], stackgroup='one', name='Other', line=dict(color='#A1A1AA')))
fig2.update_layout(
    title='Emphasis on Topics Over Time (Yearly Average)',
    xaxis_title='Year',
    yaxis_title='Proportion',
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig2.write_image("emphasis_over_time.png", width=800, height=400, scale=2)

# Visualization 3: Bar Chart - Average Emphasis by Speaker
speaker_data = df.groupby('shortSpeaker')[['inflation', 'employment', 'other']].mean().reset_index()
fig3 = go.Figure(data=[
    go.Bar(name='Inflation', x=speaker_data['shortSpeaker'], y=speaker_data['inflation'], marker_color='#FBBF24'),
    go.Bar(name='Employment', x=speaker_data['shortSpeaker'], y=speaker_data['employment'], marker_color='#34D399'),
    go.Bar(name='Other', x=speaker_data['shortSpeaker'], y=speaker_data['other'], marker_color='#A1A1AA')
])
fig3.update_layout(
    title='Average Emphasis by Speaker',
    xaxis_title='Speaker',
    yaxis_title='Proportion',
    barmode='stack',
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig3.write_image("emphasis_by_speaker.png", width=800, height=400, scale=2)

# Visualization 4: Scatter Plot - Yield vs. Fed Funds Rate by Dominant Topic
fig4 = go.Figure()
for topic in df['dominantTopic'].unique():
    df_topic = df[df['dominantTopic'] == topic]
    fig4.add_trace(go.Scatter(x=df_topic['FedFundsRate'], y=df_topic['Yield'], mode='markers', name=topic,
                              marker=dict(size=10, opacity=0.6, color={'Inflation': '#FBBF24', 'Employment': '#34D399', 'Other': '#A1A1AA'}[topic])))
fig4.update_layout(
    title='Yield vs. Fed Funds Rate by Dominant Topic',
    xaxis_title='Fed Funds Rate (%)',
    yaxis_title='Yield (%)',
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig4.write_image("yield_vs_fedfunds_rate.png", width=800, height=400, scale=2)

print("Graphs have been generated and saved as PNG files: yield_fedfunds_rate.png, emphasis_over_time.png, emphasis_by_speaker.png, yield_vs_fedfunds_rate.png")