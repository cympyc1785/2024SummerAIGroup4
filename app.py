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


st.title('TripTunes')

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
        
        if image is not None :
            st.image(image)

            loc, dtime = get_image_metadata(image) # prompt 연결 필요

            # Save Image Temporarily
            temp_dir = tempfile.mkdtemp()
            img_path = os.path.join(temp_dir, image.name)
            with open(img_path, "wb") as f:
                    f.write(image.getvalue())

            caption = pkr.get_image_caption(img_path)

            print(caption)

            recommendation = pkr.get_recommendation(caption)

            print(recommendation)

            col1, col2 = st.columns([1,1])

            with col1:
                st.title('당신만의 플레이리스트')
                st.subheader('이 세상 하나뿐인 플레이리스트와 함께 여행해보세요 🎶')

            with col2:
                st.title('당신을 위해 추천된 플레이리스트')
                st.subheader('당신의 취향에 맞는 노래들로 채워보세요.')
            
            if st.button('음악 채우기'):
                st.session_state.music_filled = True
            
            if st.session_state.music_filled:
                st.success('음악이 당신의 플레이리스트에 채워졌습니다!')

with tab2:
    st.title('TripTunes')
    st.image('https://dynamic.design.com/preview/logodraft/6ee31420-5ed6-412e-87b0-d1e4d35bcce2/image/large.png', width=300)
    st.write('저희의 새로운 서비스 Triptunes는 여러분들의 여행을 더 풍요롭게 만들 음악 플레이리스트를 제공합니다.Triptunes와 함께 여행을 떠나보세요.')

    st.title('서비스 이용 가이드')
    st.write('1. 사용자 정보를 입력해주세요')
    st.write('2. 선호하는 음악 장르를 선택해주세요.')
    st.write('3. 당신의 여행을 표현한 글 혹은 이미지를 자유롭게 선택해주세요.')
    
    
    