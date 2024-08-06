from PIL import Image
from PIL.ExifTags import TAGS
from geopy.geocoders import Nominatim

import datetime
from glob import glob
import os

image = Image.open(r'./사진/KakaoTalk_20240806_151540574.jpg')
info = image._getexif() #이미지 메타정보


# GPSInfo 정보 추출(위도, 경도)
from PIL.ExifTags import TAGS
for tag,value in info.items():
    decoded = TAGS.get(tag,tag) #태그숫자를 디코딩

    if decoded == 'GPSInfo':
        gps_lat =  value.get(2) #위도
        gps_lon =  value.get(4) #경도
        lat = (((gps_lat[2] / 60.0 ) +  gps_lat[1]) / 60.0) + gps_lat[0]
        lon = (((gps_lon[2] / 60.0 ) +  gps_lon[1]) / 60.0) + gps_lon[0]
        lat_lng_str = f'{lat},{lon}' #위도 경도 문자열
        loc = geolocator.reverse(lat_lng_str)
        loc.address

