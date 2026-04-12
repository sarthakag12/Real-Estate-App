import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns



st.title('Analytics')

st.markdown("""
This dashboard provides insights into real estate data including:
- Price trends across sectors
- Property size vs price relationship
- Popular features and configurations
\n👉 Use this dashboard to explore market patterns and make informed decisions.
""")

new_df = pd.read_csv('../datasets/processed/data_viz1.csv')
print(new_df.info())
feature_text = pickle.load(open('../models/feature_text.pkl', 'rb'))

new_df1 = new_df[['sector','price','price_per_sqft','built_up_area','latitude','longitude']]
group_df = new_df1.groupby(['sector']).mean()[['price','price_per_sqft','built_up_area','latitude','longitude']]

st.header('Sector Price per Sqft Geomap')

st.markdown("""
This map shows the distribution of average **price per square foot across different sectors**.
- Bigger circles indicate larger average built-up area.
- Darker colors represent higher price per sqft.
\n👉 Use this to identify premium and affordable locations.
""")

fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)

st.header('Features Wordcloud')

st.markdown("""
This word cloud highlights the most common features mentioned in property listings.
- Larger words indicate more frequent features.
\n👉 Helps understand what amenities are popular among properties.
""")

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot(fig)

st.header('Area Vs Price')

st.markdown("""
This scatter plot shows the relationship between **property size and price**.
- Each point represents a property.
- Color indicates number of bedrooms.
\n👉 Useful to identify whether larger homes always mean higher prices.
""")

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

st.markdown("""
This chart shows the distribution of properties based on **number of bedrooms (BHK)**.
\n👉 Helps understand which type of properties are most common in a sector.
""")

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

st.markdown("""
This box plot compares price distribution across different BHK categories.
- Shows median, range, and outliers.
\n👉 Helps identify how price increases with number of bedrooms.
""")

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

st.markdown("""
This distribution plot compares price trends between **houses and flats**.
\n👉 Helps understand which property type is generally more expensive and their price spread.
""")

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig3)