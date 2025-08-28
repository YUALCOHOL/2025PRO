import streamlit as st
import random

st.set_page_config(
    page_title="스트림릿 야바위 게임 (클라우드 버전)",
    page_icon="🔮"
)

# 세션 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = "start"  # 'start', 'shuffling', 'guessing', 'end'
    st.session_state.ball_position = None
    st.session_state.result_message = ""
    st.session_state.shuffle_count = 0
    st.session_state.cup_positions = [0, 1, 2] # 컵의 초기 위치

def start_game():
    """게임을 시작하고 컵을 섞을 준비를 하는 함수"""
    st.session_state.game_state = "shuffling"
    st.session_state.ball_position = random.randint(0, 2)
    st.session_state.result_message = ""
    st.session_state.shuffle_count = 0
    st.session_state.cup_positions = [0, 1, 2]

def shuffle_cups():
    """컵을 한 번 섞는 함수"""
    positions = st.session_state.cup_positions
    
    # 컵의 위치를 무작위로 섞습니다.
    indices = [0, 1, 2]
    random.shuffle(indices)
    
    new_positions = [positions[indices[0]], positions[indices[1]], positions[indices[2]]]
    st.session_state.cup_positions = new_positions

    # 공의 위치도 컵이 섞인 순서에 따라 변경합니다.
    st.session_state.ball_position = indices[st.session_state.ball_position]
    
    st.session_state.shuffle_count += 1
    
    if st.session_state.shuffle_count >= 5: # 5번 섞으면 멈춥니다.
        st.session_state.game_state = "guessing"
    
    st.experimental_rerun()

def check_guess(guess):
    """사용자의 선택과 공의 위치를 비교하는 함수"""
    st.session_state.game_state = "end"
    
    # 실제 공 위치와 사용자의 선택을 비교
    # 컵의 섞인 최종 위치를 기준으로 판단합니다.
    actual_position = st.session_state.cup_positions.index(st.session_state.ball_position)

    if guess == actual_position:
        st.session_state.result_message = "🎉 **성공!** 당신이 공의 위치를 정확히 맞혔습니다."
        st.balloons()
    else:
        st.session_state.result_message = "😭 **실패!** 공은 다른 곳에 있었습니다."
        st.error(f"당신은 {guess + 1}번째 컵을 선택했습니다.")

    st.experimental_rerun()

def main():
    st.title('🎩 스트림릿 야바위 게임')
    st.markdown("---")
    st.write("세 개의 컵 중 공이 들어있는 컵을 맞춰보세요!")
    st.info("이 버전은 Streamlit Cloud에서도 안정적으로 동작하도록 `time.sleep()`을 제거한 버전입니다.")

    if st.session_state.game_state == "start":
        if st.button("게임 시작"):
            start_game()
            st.experimental_rerun()
    
    elif st.session_state.game_state == "shuffling":
        st.subheader("컵을 섞고 있습니다...")
        st.write(f"섞은 횟수: {st.session_state.shuffle_count} / 5")
        
        if st.button("다음 섞기 단계"):
            shuffle_cups()
        
        # 현재 컵 상태를 텍스트로 보여주기
        cups_display = "`[   ]`   `[   ]`   `[   ]`"
        st.markdown(cups_display)
    
    elif st.session_state.game_state == "guessing":
        st.subheader("어떤 컵에 공이 있을까요?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("첫 번째 컵", key="cup_1"):
                check_guess(0)
        with col2:
            if st.button("두 번째 컵", key="cup_2"):
                check_guess(1)
        with col3:
            if st.button("세 번째 컵", key="cup_3"):
                check_guess(2)

    elif st.session_state.game_state == "end":
        st.subheader("결과 확인!")
        
        cups = ["`[   ]`", "`[   ]`", "`[   ]`"]
        
        # 공의 최종 위치를 찾아 공 표시
        final_ball_position = st.session_state.cup_positions.index(st.session_state.ball_position)
        cups[final_ball_position] = "`[ 🔮 ]`"
        
        st.markdown(f"**공의 위치:** `{cups[0]}`   `{cups[1]}`   `{cups[2]}`")
        st.markdown(st.session_state.result_message)
        
        if st.button("다시 하기"):
            start_game()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
