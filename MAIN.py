import streamlit as st
import random
import time

st.set_page_config(
    page_title="스트림릿 야바위 게임",
    page_icon="🔮"
)

# 세션 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.ball_position = None
    st.session_state.game_over = False
    st.session_state.result_message = ""
    st.session_state.shuffling_finished = False

def start_game():
    """게임을 시작하고 컵을 섞는 함수"""
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.result_message = ""
    st.session_state.shuffling_finished = False

    # 공의 위치를 무작위로 정합니다 (0, 1, 2 중 하나)
    st.session_state.ball_position = random.randint(0, 2)

    st.write("---")
    st.subheader("🔮 야바위 게임 시작!")
    st.info("컵을 섞고 있습니다...")

    # 컵 섞는 애니메이션 효과 (텍스트로 표현)
    shuffling_placeholder = st.empty()
    shuffling_placeholder.markdown("`[   ]   [   ]   [ 🔮 ]`")
    time.sleep(0.5)

    with st.spinner('컵을 섞는 중...'):
        shuffle_steps = 10
        for i in range(shuffle_steps):
            cups = ["`[   ]`", "`[   ]`", "`[   ]`"]
            # 컵 섞는 순서를 무작위로 결정
            positions = [0, 1, 2]
            random.shuffle(positions)
            
            # 실제 공 위치도 섞는 순서에 따라 이동
            new_position = positions.index(st.session_state.ball_position)
            st.session_state.ball_position = new_position
            
            # 화면에 컵의 위치 변화를 보여줍니다.
            shuffling_placeholder.markdown(f"`{cups[positions[0]]}`   `{cups[positions[1]]}`   `{cups[positions[2]]}`")
            time.sleep(0.3)
    
    shuffling_placeholder.empty()
    st.success("컵 섞기가 끝났습니다. 공은 어디에 있을까요?")
    st.session_state.shuffling_finished = True
    st.experimental_rerun()

def check_guess(guess):
    """사용자의 선택과 공의 위치를 비교하는 함수"""
    st.session_state.game_over = True
    
    cups = ["`[   ]`", "`[   ]`", "`[   ]`"]
    cups
