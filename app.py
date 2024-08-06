
from openai import OpenAI
import streamlit as st

st.title('Triptunes')

tab1, tab2, tab3,tab4 = st.tabs(["Introduction", 'How to use (Guide)','User Info','Playlist maker'])

with tab1:
    st.title('TripTunes')
    st.image('https://dynamic.design.com/preview/logodraft/6ee31420-5ed6-412e-87b0-d1e4d35bcce2/image/large.png', width=300)
    st.subheader('저희의 새로운 서비스 Triptunes는 여러분들의 여행을 더 풍요롭게 만들 음악 플레이리스트를 제공합니다.Triptunes와 함께 여행을 떠나보세요.')
with tab2:
    st.title('서비스 이용 가이드')
    st.write('1. 사용자 정보를 입력해주세요')
    st.write('2. 선호하는 음악 장르를 선택해주세요.')
    st.write('3. 당신의 여행을 표현한 글 혹은 이미지를 자유롭게 선택해주세요.')
with tab3:
    st.title('당신은 어떤 사람인가요?')
    gender = st.text_input('당신의 성별읍 입력해주세요.')
    age = st.text_input("당신의 나이를 입력해주세요.")
    character = st.text_input("당신의 MBTI를 입력해주세요.")
    genre = st.multiselect(
        '선호하는 장르를 선택해주세요.',
        ['Pop','Rock','Jazz','Classic', 'Hip-hop', 'R&B/Soul', 'Electronic','Blues'])
    st.write('You Selected:', ','.join(genre))
with tab4:
    st.title('당신의 여행을 표현해주세요 ✈️')

    form = st.radio("제출 양식", ('글','이미지'))
    if form == '글':
        st.text_input("당신의 여행을 글로 자유롭게 표현해주세요!")

    else : 
        st.write("여행 중 찍은 가장 좋아하는 사진을 올려주세요!")
        image = st.file_uploader("Upload your image here", type = ['png','jpeg','jpg'])

        if image is not None :
            st.image(image)

    

    

    
    
    
    