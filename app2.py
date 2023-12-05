import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
    
st.set_page_config(page_title="경험 기반 음식점 추천 서비스", page_icon="🍔", layout="wide")

# 세션 상태 초기화
if "page_number" not in st.session_state:
    st.session_state.page_number = 1
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

user_favorite = []
user_ID = 0

if st.session_state.page_number == 1:
    user_favorite = []

    welcome = st.empty()
    welcome.title("안녕하세요!")
    user_name_input = st.empty()
    #button = st.button("회원 가입", key="button")
    user_name = user_name_input.text_input("회원이시면, ID를 입력해 주세요", key="user_name")
    main_text_container = st.empty()
    main_text_container.caption("Visit [GitHub](https://github.com/The-Martin-Kim/2023-Machine-Learning-Term-Project)")

    if user_name != "":
        st.session_state.page_number += 1
        user_ID = user_name

        user_name_input.empty()
        welcome.empty()
        main_text_container.empty()


if st.session_state.page_number == 2:
    Hello_name = st.empty()
    Hello_name.title(f"반가워요, {user_ID} 님!")
    Hello_choice = st.empty()
    Hello_choice.subheader(f"{user_ID} 님께서 가장 최근에 다녀오신 곳이에요")

    select_restaurants = ['Spice Elephant', 'Flavours - Octave Hotel & Spa', 'Paprica', "Palki'S", 'The Onyx - The Hhi Select Bengaluru', 'Nouvelle Garden']

    container1= st.empty()
    with container1.expander(f"Went", expanded=True):
        st.write(f"{select_restaurants[0]}")
        
        next_button_3 = st.button("다음", key="next_button_3")
        if next_button_3:
            st.session_state.page_number += 1

if st.session_state.page_number == 3:
    container1.expander(f"Choice")

    st.write("---")
    Answer_name = st.empty()
    Answer_name.subheader(f"이번엔 여기 어떠세요?")
    selected_restaurant = pd.read_csv('0_dataframe.csv',
                     engine='python', on_bad_lines='skip', encoding='utf-8')

    if selected_restaurant is not None:  # Check if recommended_df is not None
            container2 = st.empty()
            with container2.expander(f"Recommend", expanded=True):
                for i in range(5):
                    col1, col2 = st.columns(2, gap="small")
                    with col1:
                        st.subheader(f"{recommended_df['name'].values[i]}")
                        st.write(f"주소: {recommended_df['address'].values[i]}")
                        st.write(f"cuisines: {recommended_df['cuisines'].values[i]}")
                        review_text = recommended_df['reviews_list'].values[i]
                        st.write(f"리뷰: {review_text[:500]}")
                    with col2:
                        geolocator = Nominatim(user_agent="my_geocoder")
                        location = geolocator.geocode(recommended_df['address'].values[i])
    
                        if location:
                            latitude, longitude = location.latitude, location.longitude
                            recommended_df.loc[i, 'Latitude'] = latitude
                            recommended_df.loc[i, 'Longitude'] = longitude
    
                            m = folium.Map(location=[latitude, longitude], zoom_start=15)
                            folium.Marker([latitude, longitude], popup=f"{recommended_df['address'].iloc[i]}").add_to(m)
                            folium_static(m, width=430, height=400)
                        else:
                            st.warning(f"Location not found for {recommended_df['name'].values[i]}. Skipping map creation.")
    else:
        st.warning("User not found. Please provide a valid user ID.")
