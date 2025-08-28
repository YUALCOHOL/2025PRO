import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# 이미지 리소스 경로 (이 경로에 투명 배경의 이미지들을 넣어주세요)
IMAGE_RESOURCES_PATH = "images"
HAT_PATH = os.path.join(IMAGE_RESOURCES_PATH, "mario_hat.png")
MUSTACHE_PATH = os.path.join(IMAGE_RESOURCES_PATH, "mario_mustache.png")
EARS_PATH = os.path.join(IMAGE_RESOURCES_PATH, "cat_ears.png")
TAIL_PATH = os.path.join(IMAGE_RESOURCES_PATH, "cat_tail.png")

st.set_page_config(
    page_title="고양이 마리오 생성기",
    page_icon="🐱"
)

def overlay_image(background_img, overlay_img, position, size=None):
    """
    배경 이미지 위에 다른 이미지를 오버레이합니다.
    background_img: PIL Image 객체
    overlay_img: PIL Image 객체 (투명 배경)
    position: (x, y) 튜플 (오버레이 이미지의 좌상단 좌표)
    size: (width, height) 튜플 (오버레이 이미지의 크기를 조절)
    """
    if size:
        overlay_img = overlay_img.resize(size)

    # 오버레이 이미지가 알파 채널을 가지고 있는지 확인
    if overlay_img.mode != 'RGBA':
        overlay_img = overlay_img.convert('RGBA')

    # 배경 이미지의 특정 영역에 오버레이 이미지를 붙여넣기
    # 이 부분은 단순 오버레이이며, 얼굴 인식 등 복잡한 위치 조정은 포함하지 않습니다.
    x, y = position
    background_img.paste(overlay_img, (x, y), overlay_img)
    return background_img

def main():
    st.title('🐱 고양이 마리오 생성기')
    st.markdown("---")
    st.write("당신의 사진에 마리오의 모자, 콧수염과 고양이 귀, 꼬리를 추가하여 고양이 마리오를 만들어보세요!")
    st.info("이 앱은 예시이며, 실제 얼굴 인식 및 정확한 이미지 합성은 추가적인 복잡한 로직이 필요합니다.")

    # 이미지 리소스 존재 여부 확인
    resources_exist = True
    if not os.path.exists(IMAGE_RESOURCES_PATH):
        st.warning(f"'{IMAGE_RESOURCES_PATH}' 폴더가 없습니다. 이미지 리소스를 넣어주세요.")
        resources_exist = False
    else:
        for path in [HAT_PATH, MUSTACHE_PATH, EARS_PATH, TAIL_PATH]:
            if not os.path.exists(path):
                st.warning(f"필요한 이미지 파일 '{os.path.basename(path)}'이(가) '{IMAGE_RESOURCES_PATH}' 폴더에 없습니다. 파일을 넣어주세요.")
                resources_exist = False

    if not resources_exist:
        st.stop() # 리소스 없으면 앱 중단

    uploaded_file = st.file_uploader("사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        try:
            original_image = Image.open(uploaded_file).convert("RGBA")
            st.subheader("원본 이미지")
            st.image(original_image, use_column_width=True)

            st.markdown("---")
            st.subheader("고양이 마리오 이미지")

            # 리소스 이미지 로드 (투명 배경 이미지)
            mario_hat = Image.open(HAT_PATH).convert("RGBA")
            mario_mustache = Image.open(MUSTACHE_PATH).convert("RGBA")
            cat_ears = Image.open(EARS_PATH).convert("RGBA")
            cat_tail = Image.open(TAIL_PATH).convert("RGBA")

            processed_image = original_image.copy()

            # --- 이미지 오버레이 (예시 위치, 실제 구현 시 얼굴 인식 등으로 위치 조정 필요) ---
            img_width, img_height = original_image.size

            # 모자 (이미지 상단 중앙)
            hat_size = (int(img_width * 0.4), int(img_width * 0.4 / mario_hat.width * mario_hat.height))
            processed_image = overlay_image(processed_image, mario_hat, (int(img_width * 0.3), int(img_height * 0.05)), size=hat_size)

            # 고양이 귀 (모자 옆 또는 모자 위쪽)
            ears_size = (int(img_width * 0.2), int(img_width * 0.2 / cat_ears.width * cat_ears.height))
            processed_image = overlay_image(processed_image, cat_ears, (int(img_width * 0.1), int(img_height * 0.02)), size=ears_size)
            processed_image = overlay_image(processed_image, cat_ears.transpose(Image.FLIP_LEFT_RIGHT), (int(img_width * 0.7), int(img_height * 0.02)), size=ears_size)


            # 콧수염 (이미지 중앙 하단)
            mustache_size = (int(img_width * 0.25), int(img_width * 0.25 / mario_mustache.width * mario_mustache.height))
            processed_image = overlay_image(processed_image, mario_mustache, (int(img_width * 0.4), int(img_height * 0.5)), size=mustache_size)

            # 꼬리 (이미지 하단, 실제 인물에 붙이려면 더 복잡한 처리 필요)
            tail_size = (int(img_width * 0.3), int(img_width * 0.3 / cat_tail.width * cat_tail.height))
            processed_image = overlay_image(processed_image, cat_tail, (int(img_width * 0.7), int(img_height * 0.8)), size=tail_size)


            st.image(processed_image, use_column_width=True, caption="짠! 고양이 마리오!")

            # 결과 이미지 다운로드 버튼
            st.markdown("---")
            st.download_button(
                label="결과 이미지 다운로드",
                data=image_to_byte_array(processed_image),
                file_name="cat_mario.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"이미지 처리 중 오류가 발생했습니다: {e}")
            st.exception(e)

def image_to_byte_array(image: Image) -> bytes:
    """PIL Image를 바이트 배열로 변환"""
    import io
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

if __name__ == '__main__':
    main()
