import streamlit as st
import time

st.set_page_config(
    page_title="고양이 마리오 (텍스트 버전)",
    page_icon="🐱"
)

# 게임 상태를 저장할 변수 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "start"
    st.session_state.game_over = False
    st.session_state.score = 0

def reset_game():
    """게임을 초기화하는 함수"""
    st.session_state.game_state = "start"
    st.session_state.game_over = False
    st.session_state.score = 0

def go_to_level(level_name):
    """다음 레벨로 이동하는 함수"""
    st.session_state.game_state = level_name
    st.session_state.score += 1

def end_game(message):
    """게임 오버를 처리하는 함수"""
    st.session_state.game_over = True
    st.error(f"❌ 게임 오버: {message}")
    st.warning("다시 시작하려면 아래 버튼을 눌러주세요.")
    if st.button("다시 시작하기", on_click=reset_game):
        st.experimental_rerun()

def render_level():
    """현재 게임 상태에 따라 화면을 렌더링하는 함수"""
    if st.session_state.game_state == "start":
        st.title('🐱 고양이 마리오 텍스트 모험')
        st.markdown("---")
        st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?q=80&w=2940&auto=format&fit=crop", caption="마을 입구에 도착한 고양이 마리오...", use_column_width=True)
        st.write("마을 입구에 도착했습니다. 당신의 앞에는 마리오의 상징적인 **물음표 블록**이 두 개 보입니다. 어느 것을 칠까요?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("왼쪽 블록 치기"):
                go_to_level("level_1_left")
        with col2:
            if st.button("오른쪽 블록 치기"):
                go_to_level("level_1_right")

    elif st.session_state.game_state == "level_1_left":
        st.header("레벨 1: 물음표 블록")
        st.write("당신은 왼쪽 블록을 쳤습니다. **앗!** 블록에서 동전 대신 날카로운 가시가 튀어나왔습니다.")
        end_game("가시에 찔렸습니다. 역시나 함정이었군요.")

    elif st.session_state.game_state == "level_1_right":
        st.header("레벨 1: 물음표 블록")
        st.write("당신은 오른쪽 블록을 쳤습니다. **와!** 블록에서 버섯이 나왔습니다. 몸이 조금 더 커진 것 같네요.")
        st.success("버섯 획득! 계속 전진하세요.")
        st.image("https://images.unsplash.com/photo-1549557492-c0e862024de3?q=80&w=2940&auto=format&fit=crop", caption="성장 버섯을 획득했다!", use_column_width=True)
        if st.button("계속하기"):
            go_to_level("level_2")
            st.experimental_rerun()

    elif st.session_state.game_state == "level_2":
        st.header("레벨 2: 절벽과 파이프")
        st.write("버섯을 먹고 힘차게 달리던 중, 앞에 깊은 절벽이 나타났습니다. 절벽 아래로는 초록색 파이프가 보입니다. 점프해서 건너갈까요, 아니면 파이프 안으로 들어갈까요?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("점프해서 건너가기"):
                end_game("절벽을 건너가려다 발을 헛디뎠습니다. 그대로 아래로 추락했습니다.")
        with col2:
            if st.button("파이프 안으로 들어가기"):
                st.write("파이프 안으로 조심스럽게 들어갔습니다. 놀랍게도 파이프 아래는 안전한 통로였습니다!")
                st.success("안전하게 다음 구역으로 이동했습니다.")
                if st.button("다음 레벨로"):
                    go_to_level("level_3")
                    st.experimental_rerun()

    elif st.session_state.game_state == "level_3":
        st.header("레벨 3: 최종 보스")
        st.write("모든 역경을 뚫고 최종 보스 성에 도착했습니다. 성 안에는 거대한 악당이 기다리고 있습니다.")
        st.write("...라고 생각했지만, 갑자기 **'끝'** 이라는 글자가 나타나더니 게임이 종료되었습니다.")
        st.balloons()
        end_game("성공적으로 게임을 클리어했습니다! 하지만 이런 게임이 늘 그렇듯, 허무한 엔딩이 기다리고 있었군요.")

    st.markdown("---")
    st.write(f"현재 점수: {st.session_state.score}")
    
    if st.session_state.game_over:
        st.markdown("<p style='text-align: center;'><strong>게임 오버!</strong></p>", unsafe_allow_html=True)
        if st.button("다시 시작", key="restart_after_game_over"):
            st.experimental_rerun()

# 게임 시작
render_level()
