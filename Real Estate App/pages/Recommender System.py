
import streamlit as st
import pickle
import pandas as pd
import numpy as np



location_df = pickle.load(open('../models/location_distance1.pkl','rb'))

cosine_sim1 = pickle.load(open('../models/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('../models/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('../models/cosine_sim3.pkl','rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


# Test the recommender function using a property name
recommend_properties_with_scores('DLF The Camellias')

st.title('🏡 Property Recommender System')

st.markdown("""
This tool helps you **discover properties based on location and similarity**.

### 🔍 What you can do:

#### 📍 Location Search
- Find properties within a selected **radius (in km)**
- Useful for exploring nearby options

#### 🤝 Similar Property Recommendations
- Select a property and get **similar listings**
- Based on features like location, amenities, and property characteristics
- Uses **similarity algorithms (cosine similarity)**

👉 Use the tools below to explore and compare properties.
""")


st.title('Select Location and Radius')

st.markdown("""
Find properties within a specific **distance from your selected location**.
\n👉 Helps in shortlisting nearby options.
""")

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in Kms')

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    for key, value in result_ser.items():
        st.text(str(key) + "  "+"-->"+"  " + str(round(value/1000)) + ' kms')

st.title('Similar Apartments')
st.markdown("""
Get recommendations for properties that are **similar to your selected apartment**.
\n👉 Useful for comparing alternatives before making a decision.
""")

selected_appartment = st.selectbox('Select an appartment',sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    st.dataframe(recommendation_df)
