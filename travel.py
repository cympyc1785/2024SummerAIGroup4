from PIL import Image
from PIL.ExifTags import TAGS

image = Image.open(r'./사진/KakaoTalk_2022-06-04 14-06-00.jpg')
info = image._getexif() #이미지 메타정보
info


from PIL.ExifTags import TAGS
for tag,value in info.items():
    # print(value)
    decoded = TAGS.get(tag,tag) #태그숫자를 디코딩
    print(tag,decoded,value)


    