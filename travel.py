from PIL import Image
from PIL.ExifTags import TAGS
import datetime
from glob import glob
import os

def get_image_metadata(image_path):
    image = Image.open(image_path)
    info = image._getexif() #이미지 메타정보
    print(info)
    for tag,value in info.items():
        decoded = TAGS.get(tag,tag) #태그숫자를 디코딩

        if decoded == 'GPSInfo':
            gps_lat =  value.get(2) #위도
            gps_lon =  value.get(4) #경도
            lat = (((gps_lat[2] / 60.0 ) +  gps_lat[1]) / 60.0) + gps_lat[0] #위도 단위 통일
            lon = (((gps_lon[2] / 60.0 ) +  gps_lon[1]) / 60.0) + gps_lon[0] #경도 단위 통일

        if decoded == 'DateTime':
            dt = datetime.datetime.strptime(value,"%Y:%m:%d %H:%M:%S")
            dtime = dt.strftime("%Y-%m-%d %H-%M-%S")
            print(dtime)

    return lat, lon, dtime

image_path = 'KakaoTalk_20240806_151540574.jpg'
metadata = get_image_metadata(image_path)
print(metadata)


        
        



