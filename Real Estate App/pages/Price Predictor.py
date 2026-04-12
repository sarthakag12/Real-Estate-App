import streamlit as st
import pickle
import pandas as pd
import numpy as np




with open('../models/df.pkl','rb') as file:
    df = pickle.load(file)


with open('../models/pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)

st.title('🏠 Property Price Predictor')

st.markdown("""
This tool predicts the **estimated price of a property in Gurgaon** based on key inputs.

### 🔍 How it works:
- Uses a trained **machine learning model** on historical real estate data
- Considers factors like location, size, amenities, and property type
- Provides a **price range** instead of a single value for better realism

### 📊 Key Inputs:
- Property type (Flat/House)
- Sector (Location)
- Area (Built-up area)
- Number of rooms & bathrooms
- Property features (furnishing, luxury level, etc.)

👉 Enter the details below to get an estimated price range.
""")

st.header('Enter your inputs')

# property_type
property_type = st.selectbox('Property Type',['flat','house'])

# sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))
store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):

    # form a dataframe
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    #st.dataframe(one_df)

    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    st.success(f"""
💰 Estimated Property Price Range:  
**₹ {round(low,2)} Cr – ₹ {round(high,2)} Cr**

📌 This is an approximate range based on similar properties and market trends.
""")
