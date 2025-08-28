import streamlit as st
import requests
import os
import json

# 네이버 클라우드 플랫폼에서 발급받은 Client ID와 Client Secret을 설정합니다.
# 보안을 위해 secrets.toml 파일을 사용하는 것을 권장합니다.
try:
    NAVER_CLIENT_ID = st.secrets["NAVER_CLIENT_ID"]
    NAVER_CLIENT_SECRET = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("네이버 API 키를 찾을 수 없습니다. secrets.toml 파일에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 추가하거나, 코드에 직접 키를 입력하세요.")
    st.stop()

st.set_page_config(
    page_title="네이버 지도 경로 찾기",
    page_icon="🗺️"
)

def geocode(address):
    """주소를 위도, 경도 좌표로 변환"""
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY-SECRET": NAVER_CLIENT_SECRET,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['addresses']:
            return (data['addresses'][0]['x'], data['addresses'][0]['y'])
    return None

def get_route(start_coord, end_coord, mode):
    """출발지-도착지 좌표로 최적 경로를 검색"""
    if mode == '자동차':
        url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    elif mode == '대중교통':
        st.warning("네이버 대중교통 경로는 현재 웹 API에서 공식적으로 지원하지 않습니다. 자동차 경로를 대신 검색합니다.")
        url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    else:
        st.warning("도보 및 자전거 경로는 현재 웹 API에서 공식적으로 지원하지 않습니다. 자동차 경로를 대신 검색합니다.")
        url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"

    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY-SECRET": NAVER_CLIENT_SECRET,
    }
    params = {
        'start': f"{start_coord[0]},{start_coord[1]}",
        'goal': f"{end_coord[0]},{end_coord[1]}",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

st.title('🗺️ 네이버 지도 최적 경로 찾기')
st.markdown("---")

# 사용자 입력
start_location = st.text_input("출발지를 입력하세요 (예: 서울역)", "서울역")
end_location = st.text_input("도착지를 입력하세요 (예: 강남역)", "강남역")

transport_mode = st.selectbox(
    "이동 수단을 선택하세요:",
    ('자동차', '대중교통', '도보', '자전거')
)

if st.button("경로 찾기"):
    if not start_location or not end_location:
        st.warning("출발지 또는 도착지를 입력해주세요.")
        st.stop()

    start_coord = geocode(start_location)
    end_coord = geocode(end_location)
    
    if not start_coord:
        st.error(f"'{start_location}'의 좌표를 찾을 수 없습니다. 정확한 주소를 입력해주세요.")
    elif not end_coord:
        st.error(f"'{end_location}'의 좌표를 찾을 수 없습니다. 정확한 주소를 입력해주세요.")
    else:
        st.success("✅ 좌표 변환 성공! 경로를 검색합니다...")
        route_data = get_route(start_coord, end_coord, transport_mode)
        
        if route_data and 'route' in route_data and 'trafast' in route_data['route']:
            st.subheader("✅ 최적 경로 정보")
            
            # API 응답에서 필요한 정보 추출
            if route_data['route']['trafast']:
                path_info = route_data['route']['trafast'][0]
                distance = path_info['summary']['distance'] / 1000  # 미터를 킬로미터로 변환
                duration_sec = path_info['summary']['duration'] / 1000  # 밀리초를 초로 변환
                
                duration_min = int(duration_sec / 60)
                duration_hour = int(duration_min / 60)
                duration_min %= 60
                
                st.write(f"**총 거리:** {distance:.2f} km")
                st.write(f"**예상 시간:** {duration_hour}시간 {duration_min}분")
                
                # 경로를 네이버 지도로 보여주기
                # Geocoding된 좌표를 이용해 URL 생성
                naver_map_url = f"https://map.naver.com/p/search/{start_location}?c=15.00,0,0,0,dh"
                st.write(f"**👉 네이버 지도로 경로 보기:** [바로가기]({naver_map_url})")
                
                # HTML과 JavaScript를 사용하여 지도 표시 (API 키 노출 문제로 이미지로 대체)
                # 실제 앱에서는 네이버 지도의 웹 컴포넌트나 JS API를 사용해야 합니다.
                st.image("https://naver.github.io/maps.js.v3/img/sample/simple-map.png", caption="여기에 네이버 지도가 표시될 영역입니다.")
                st.info("⚠️ 현재 Streamlit에서 네이버 지도를 직접 연동하는 공식적인 컴포넌트가 없어, API 호출 결과만 표시합니다. 실제 지도는 링크를 통해 확인하세요.")

        else:
            st.error("경로를 찾는 데 실패했습니다. 다시 확인해주세요.")
            st.json(route_data) # 디버깅용으로 API 응답 출력
