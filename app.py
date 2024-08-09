from openai import OpenAI
from PIL import Image
from PIL.ExifTags import TAGS
from geopy.geocoders import Nominatim
from prompt import photo_keyword_request as pkr
from dotenv import load_dotenv
from meta_app import get_image_metadata
import streamlit as st
import datetime
import os
import tempfile
import webbrowser
import pandas as pd
def goto_link(site_url):
    webbrowser.open(site_url)
# Load .env
load_dotenv()
# API_KEY = os.environ.get('API_KEY')
API_KEY = st.secrets['API_KEY']
# Initial Setup
geolocator = Nominatim(user_agent='geoapigroup4')
if 'playlist_generated' not in st.session_state:
    st.session_state.playlist_generated = False
if 'music_filled' not in st.session_state:
    st.session_state.music_filled = False
if 'prev_image' not in st.session_state:
    st.session_state.prev_image = None
if 'prev_description' not in st.session_state:
    st.session_state.prev_description = ""
if 'total_playlists' not in st.session_state:
    st.session_state.total_playlists = []
if 'travel_title' not in st.session_state:
    st.session_state.travel_title = ""
st.title('TripTunes')
tab1, tab2 = st.tabs(['사용자 정보 입력', "서비스 소개 및 사용 가이드"])
# Sidebar update function
def update_sidebar():
    with st.sidebar:
        for title in st.session_state.total_playlists:
            st.write(title)
#update_sidebar()  # Initial sidebar update
with tab1:
    st.title('당신은 어떤 사람인가요?')
    gender = st.text_input('당신의 성별을 입력해주세요.')
    age = st.text_input("당신의 나이를 입력해주세요.")
    character = st.text_input("당신의 MBTI를 입력해주세요.")
    genre = st.multiselect(
        '선호하는 장르를 선택해주세요.',
        ['Pop', 'Rock', 'Jazz', 'Classic', 'Hip-hop', 'R&B/Soul', 'Electronic', 'Blues'])
    st.write('You Selected:', ','.join(genre))
    if st.button('플레이리스트 생성'):
        st.session_state.playlist_generated = True
    if st.session_state.playlist_generated:
        st.title('당신의 여행을 표현해주세요')
        st.write("여행 중 찍은 가장 좋아하는 사진을 올려주세요")
        image = st.file_uploader("사진 첨부", type=['png', 'jpeg', 'jpg'])
        description = st.text_input("사진에 대한 설명을 넣어주세요.")
        if image is not None:
            st.image(image)
            if image != st.session_state.prev_image or description != st.session_state.prev_description:
                st.session_state.prev_image = image
                st.session_state.prev_description = description
                # Save Image Temporarily
                temp_dir = tempfile.mkdtemp()
                img_path = os.path.join(temp_dir, image.name)
                with open(img_path, "wb") as f:
                    f.write(image.getvalue())
                caption = pkr.get_image_caption(img_path)
                loc, dtime = get_image_metadata(img_path)
                img_meta_data = (loc, dtime)
                user_data = {'gender': gender, 'age': age, 'character': character, 'genre': genre}
                st.session_state.recommendation = pkr.get_recommendation(caption, description, img_meta_data, user_data)
            col1, col2 = st.columns(2)
            style = """
            <style>
            .title {
                font-size:25px !important;
            }
            .subheader{
                font-size:15px !important;
            }
            </style>
            """
            playlist1_title = """
            <p class="title">Your Playlist</p>
            """
            playlist2_title = """
            <p class="title">Recommendation</p>
            """
            playlist1_subheader = """
            <p class="subheader">이 세상 하나뿐인 플레이리스트와 함께 여행해보세요</p>
            """
            playlist2_subheader = """
            <p class="subheader">당신의 취향에 맞는 노래들로 채워보세요.</p>
            """
            selected_music = []
            with col1:
                st.markdown(playlist2_title, unsafe_allow_html=True)
                st.markdown(playlist2_subheader, unsafe_allow_html=True)
                if "recommendation" in st.session_state:
                    recommend = st.session_state.recommendation
                    df = pd.DataFrame(
                        [
                            {"Select": False,
                             "Title": music[0],
                             "Artist": music[1],
                             "Genre": music[2],
                             "URL": f"https://open.spotify.com/search/{music[0]}"} for music in recommend
                        ]
                    )
                    editable_df = st.data_editor(
                        df,
                        column_config={
                            "URL": st.column_config.LinkColumn("Music URL")
                        },
                        disabled=["Title", "Artist", "Genre", "URL"],
                        hide_index=True
                    )
                    selected_music = editable_df[editable_df["Select"] == True]
            with col2:
                st.markdown(style + playlist1_title, unsafe_allow_html=True)
                st.markdown(style + playlist1_subheader, unsafe_allow_html=True)
                if len(selected_music) > 0:
                    st.dataframe(selected_music.drop(columns=["Select"]),
                                 column_config={
                                     "URL": st.column_config.LinkColumn("Music URL")
                                 }, hide_index=True, width=700)
            # Separated title input and button logic
            st.session_state.travel_title = st.text_input("여행의 제목을 입력해주세요")
            if st.button('음악 채우기') and st.session_state.travel_title:
                st.session_state.total_playlists.append(st.session_state.travel_title)
                update_sidebar()  # Update sidebar after adding new playlist title
                st.success('음악이 당신의 플레이리스트에 채워졌습니다!')
with tab2:
    st.title('TripTunes')
    st.image('https://dynamic.design.com/preview/logodraft/6ee31420-5ed6-412e-87b0-d1e4d35bcce2/image/large.png', width=300)
    st.write('저희의 새로운 서비스 Triptunes는 여러분들의 여행을 더 풍요롭게 만들 음악 플레이리스트를 제공합니다.Triptunes와 함께 여행을 떠나보세요.')
    st.title('서비스 이용 가이드')
    st.write('1. 사용자 정보를 입력해주세요')
    st.write('2. 선호하는 음악 장르를 선택해주세요.')
    st.write('3. 당신의 여행을 표현한 글 혹은 이미지를 자유롭게 선택해주세요.')