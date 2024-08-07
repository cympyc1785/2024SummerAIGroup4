from PIL import Image
from PIL.ExifTags import TAGS
import datetime
from geopy.geocoders import Nominatim

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

# 이미지 넣으면 path 설정 필요!!
image_path = '/content/KakaoTalk_20240806_164948730.jpg'
metadata = get_image_metadata(image_path)
print(metadata) # 자료형 확인해서 프롬프트 엔지니어링 필요

#얘는 그냥 깔끔용.
if metadata:
    location, datetime_str = metadata
    if location:
        print(f"Location: {location}")
    else:
        print("Location information not available")
    
    if datetime_str:
        print(f"DateTime: {datetime_str}")
    else:
        print("DateTime information not available")
else:
    print("Metadata extraction failed")
