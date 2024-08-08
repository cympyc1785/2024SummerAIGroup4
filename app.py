from openai import OpenAI
from PIL import Image
from PIL.ExifTags import TAGS
from geopy.geocoders import Nominatim
from prompt import photo_keyword_request as pkr
from dotenv import load_dotenv
import streamlit as st
import datetime
import os
import tempfile
import webbrowser
import pandas as pd
import streamlit as st

def goto_link(site_url):
    webbrowser.open(site_url)

# load .env
load_dotenv()
API_KEY = os.environ.get('API_KEY')

# 아무거나 초기설정
geolocator = Nominatim(user_agent='geoapigroup4')
def get_image_metadata(image_path):
    try:
        img = Image.open(image_path)
        info = img._getexif()  # 이미지 메타정보
        
        # 메타데이터 존재여부 (휴대폰 설정에 따라 다른듯요)
        if info is None:
            print(f"No EXIF metadata found in {image_path}")
            return None, None, None 
        
        lat = None
        lon = None
        dtime = None
        loc = None

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)  # 태그숫자를 디코딩

            if decoded == 'GPSInfo':
                gps_lat = value.get(2)  # 위도
                gps_lon = value.get(4)  # 경도

                #표준화
                lat = (gps_lat[0] + gps_lat[1] / 60.0 + gps_lat[2] / 3600.0)
                lon = (gps_lon[0] + gps_lon[1] / 60.0 + gps_lon[2] / 3600.0)

                # 동서/ 남북 구분
                if value.get(3) == 'S':
                    lat = -lat
                if value.get(1) == 'W':
                    lon = -lon

                # 역계산
                if lat is not None and lon is not None:
                    location = geolocator.reverse((lat, lon))
                    loc = location.address

            if decoded == 'DateTime':
                dt = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                dtime = dt.strftime("%Y-%m-%d %H-%M-%S")  # 연, 월, 일, 시간, 분, 초 순 자료형태

        return loc, dtime
    
    except FileNotFoundError:
        print(f"Image not found at {image_path}")
        return None, None

if 'playlist_generated' not in st.session_state:
    st.session_state.playlist_generated = False

if 'music_filled' not in st.session_state:
    st.session_state.music_filled = False

if 'prev_image' not in st.session_state:
    st.session_state.prev_image = None

if 'prev_description' not in st.session_state:
    st.session_state.prev_description = ""


st.image('https://bcassetcdn.com/social/vm77minaoy/preview.png', width = 200)

tab1, tab2 = st.tabs(['사용자 정보 입력',"서비스 소개 및 사용 가이드"])

with tab1:
    st.title('당신은 어떤 사람인가요?')
    gender = st.text_input('당신의 성별을 입력해주세요.')
    age = st.text_input("당신의 나이를 입력해주세요.")
    character = st.text_input("당신의 MBTI를 입력해주세요.")
    genre = st.multiselect(
        '선호하는 장르를 선택해주세요.',
        ['Pop','Rock','Jazz','Classic', 'Hip-hop', 'R&B/Soul', 'Electronic','Blues'])
    st.write('You Selected:', ','.join(genre))

    if st.button('플레이리스트 생성'):
        st.session_state.playlist_generated = True

    if st.session_state.playlist_generated:
    
        st.title('당신의 여행을 표현해주세요 ✈️')
    
        st.write("여행 중 찍은 가장 좋아하는 사진을 올려주세요 📷")
        image = st.file_uploader("사진 첨부", type = ['png','jpeg','jpg'])
        description = st.text_input("사진에 대한 설명을 넣어주세요.")
        
        if image is not None and description is not None:
            st.image(image)

            if image != st.session_state.prev_image or description != st.session_state.prev_description:
                st.session_state.prev_image = image

                # Save Image Temporarily
                temp_dir = tempfile.mkdtemp()
                img_path = os.path.join(temp_dir, image.name)
                with open(img_path, "wb") as f:
                        f.write(image.getvalue())

                caption = pkr.get_image_caption(img_path)

                print(caption)
                
                st.session_state.recommendation = pkr.get_recommendation(caption, description)

                print(st.session_state.recommendation)

            recomm = [['"Bubble Pop"', '', 'Hyuna', '', 'K-pop'], ['"Electric Feel"', '', 'MGMT  ', '', 'Psychedelic Rock'], ['"Dog Days Are Over"', '', 'Florence + The Machine', '', 'Indie Rock'], ['"Go!"', '', 'The Chemical Brothers (feat. Q-Tip)', '', 'Electronic Dance Music'], ['"Happy"', '', 'Pharrell Williams', '', 'Pop'], ['"Daft Punk Is Playing At My House"', '', 'LCD Soundsystem', '', 'Dance Punk'], ['"Shake It Off"', '', 'Taylor Swift', '', 'Pop'], ['"Experiment On Me"', '', 'Halsey', '', 'Alternative/Indie'], ['"Blue Monday"', '', 'New Order', '', 'Synthpop'], ['"Viva La Vida"', '', 'Coldplay', '', 'Alternative Rock'], ['"I Got A Boy"', '', "Girls' Generation", '', 'K-pop'], ['"Do It"', '', 'Chloe x Halle', '', 'R&B/Soul']]

            rec_v2 = [['"Dynamite"', 'BTS', 'K-pop'], ['"Blinding Lights"', 'The Weeknd', 'Synthwave/Pop'], ['"Watermelon Sugar"', 'Harry Styles', 'Pop'], ['"Electric Feel"', 'MGMT', 'Indietronica/Psychedelic pop'], ['"Little Dark Age"', 'MGMT', 'Synthpop/Indietronica'], ['"Stay"', 'The Kid LAROI & Justin Bieber', 'Pop'], ['"Slide"', 'Calvin Harris ft. Frank Ocean & Migos', 'Electropop'], ['"On Our Way"', 'The Royal Concept', 'Indie Rock/Indietronica'], ['"You Can Call Me Al"', 'Paul Simon', 'Worldbeat/Pop Rock'], ['"Deja Vu"', 'Olivia Rodrigo', 'Pop/Rock'], ['"A Boy Is a Gun"', 'Tyler, the Creator', 'Alternative Hip-Hop'], ['"Phantom Pt. II"', 'Justice', 'Electro House']]

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
            <p class="subheader">이 세상 하나뿐인 플레이리스트와 함께 여행해보세요 🎶</p>
            """
            playlist2_subheader = """
            <p class="subheader">당신의 취향에 맞는 노래들로 채워보세요.</p>
            """

            #st.markdown(html_code, unsafe_allow_html=True)

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
                st.markdown(style+playlist1_title, unsafe_allow_html=True)
                st.markdown(style+playlist1_subheader, unsafe_allow_html=True)
                if len(selected_music) > 0:
                    st.dataframe(selected_music.drop(columns=["Select"]),
                                 column_config={
                                     "URL": st.column_config.LinkColumn("Music URL")
                                 }, hide_index=True, width=700)
                # Display the selected music
                #st.write("Selected Music:")
                #st.write(selected_music)
                #st.title('당신만의 플레이리스트')
                #st.subheader('이 세상 하나뿐인 플레이리스트와 함께 여행해보세요 🎶')
                

            #if st.button('음악 채우기'):
            #    st.session_state.music_filled = True
            
            if st.session_state.music_filled:
                st.success('음악이 당신의 플레이리스트에 채워졌습니다!')

with tab2:
    st.title('TripTunes')
    
    st.write('저희의 새로운 서비스 Triptunes는 여러분들의 여행을 더 풍요롭게 만들 음악 플레이리스트를 제공합니다.Triptunes와 함께 여행을 떠나보세요.')

    st.title('서비스 이용 가이드')
    st.write('1. 사용자 정보를 입력해주세요')
    st.write('2. 선호하는 음악 장르를 선택해주세요.')
    st.write('3. 당신의 여행을 표현한 글 혹은 이미지를 자유롭게 선택해주세요.')
    
    
    