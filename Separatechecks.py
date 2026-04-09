import streamlit as st
import random


# --- 1. 기능 함수 정의 ---
@st.dialog("알림")
def show_alert(message):
    st.write(message)
    _, btn_col = st.columns([0.8, 0.2])
    with btn_col:
        if st.button("확인"):
            st.rerun()


def increase_tip():
    st.session_state.tip_slider = min(20, st.session_state.tip_slider + 10)


def decrease_tip():
    st.session_state.tip_slider = max(0, st.session_state.tip_slider - 10)


def reset_all():
    st.session_state.total_amount = ""
    st.session_state.num_people = ""
    st.session_state.tip_slider = 0
    st.session_state.calculated = False
    # 정산 단계 기억 초기화
    st.session_state.rounding_choice = None
    st.session_state.draw_choice = None
    st.session_state.start_drawing = False


# --- 2. 메인 프로그램 시작 ---
def main():
    if "total_amount" not in st.session_state:
        st.session_state.total_amount = ""
    if "num_people" not in st.session_state:
        st.session_state.num_people = ""
    if "tip_slider" not in st.session_state:
        st.session_state.tip_slider = 0
    if "calculated" not in st.session_state:
        st.session_state.calculated = False

    # 정산 단계 상태 관리
    if "rounding_choice" not in st.session_state:
        st.session_state.rounding_choice = None  # 'yes', 'no'
    if "draw_choice" not in st.session_state:
        st.session_state.draw_choice = None  # 'yes', 'no'
    if "start_drawing" not in st.session_state:
        st.session_state.start_drawing = False  # 추첨 시작 버튼 클릭 여부

    # [디자인 설정]
    st.markdown("""
       <style>
        .main-title { text-align: center; }

        /* 1. 일반 버튼들 (하얀색 유지) */
        button[kind="secondary"], 
        button[data-testid*="secondary"] {
            background-color: white !important; 
            color: black !important;
            border: 1px solid #cccccc !important;
        }

        /* 2. 제출/추첨 버튼 (초록색 강제) */
        button[kind="primary"], 
        button[data-testid*="primary"] {
            background-color: #28a745 !important;
            color: white !important;
            border: 1px solid #28a745 !important;
        }

        /* 3. 초기화 버튼 (회색) */
        div[data-testid*="stHorizontalBlock"]:last-of-type div[data-testid*="column"]:first-child button {
            background-color: #e0e0e0 !important;
            color: black !important;
        }

        /* 4. 스테퍼 버튼들 중앙 정렬 */
        div[data-testid*="stHorizontalBlock"] button {
            display: block;
            margin: 0 auto;
        }

        /* 📱 5. [모바일 완벽 최적화] 핸드폰에서 탑처럼 쌓이는 현상 원천 차단! */
        @media screen and (max-width: 768px) {
            /* (1) 내부 박스들은 무조건 한 줄(row)로 붙여놓기! 줄바꿈 금지! */
            div[data-testid="column"] div[data-testid="stHorizontalBlock"] {
                flex-wrap: nowrap !important;
                flex-direction: row !important;
                align-items: center !important; /* 위아래 수직 중앙 정렬까지! */
            }
            
            /* (2) [가장 중요] 모바일에서 강제로 100% 넓이가 되는 Streamlit 고집 꺾기! */
            div[data-testid="column"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                min-width: 0 !important;  /* 이 한 줄이 3층 탑을 1층으로 만들어줍니다! */
                width: auto !important;
                flex: 1 1 0% !important;
            }

            /* (3) 좁은 핸드폰 화면에서 화살표나 글씨가 잘리지 않게 버튼 양옆 여백 줄이기 */
            div[data-testid="column"] div[data-testid="stHorizontalBlock"] button {
                padding-left: 5px !important;
                padding-right: 5px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>모임 회비 관리 계산기</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>총 금액, 인원 수, 팁 비율을 입력하여 1인당 부담할 금액을 계산합니다.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("입력")
            st.session_state.total_amount = st.text_input("총 금액(원)", value=st.session_state.total_amount)
            st.session_state.num_people = st.text_input("인원 수(명)", value=st.session_state.num_people)
            st.write("---")
            label_col, stepper_col = st.columns([0.5, 0.5])
            with label_col:
                st.markdown("<div style='margin-top: 5px;'><b>팁/서비스 비율(%)</b></div>", unsafe_allow_html=True)
            with stepper_col:
                btn_down, text_val, btn_up = st.columns([1, 1, 1])
                btn_down.button("▼", on_click=decrease_tip, key="down_btn")
                text_val.markdown(
                    f"<div style='text-align: center; margin-top: 5px; background-color: white; border: 1px solid #cccccc; border-radius: 4px; padding: 2px;'><b>{st.session_state.tip_slider}</b></div>",
                    unsafe_allow_html=True)
                btn_up.button("▲", on_click=increase_tip, key="up_btn")

            st.slider("팁", min_value=0, max_value=20, key="tip_slider", label_visibility="collapsed")
            st.write("")

            btn_col_left, btn_col_right = st.columns(2)
            with btn_col_left:
                st.button("초기화", on_click=reset_all, use_container_width=True)
            with btn_col_right:
                if st.button("제출", use_container_width=True, type="primary"):
                    if not st.session_state.total_amount or not st.session_state.num_people:
                        show_alert("총 금액과 인원수를 모두 입력해주세요!")
                    else:
                        try:
                            total = int(st.session_state.total_amount)
                            people = int(st.session_state.num_people)
                            if people <= 0:
                                show_alert("인원수는 1명 이상이어야 합니다!")
                            else:
                                tip_amount = total * (st.session_state.tip_slider / 100)
                                st.session_state.final_total = total + tip_amount
                                st.session_state.calculated = True
                                # 상태 리셋
                                st.session_state.rounding_choice = None
                                st.session_state.draw_choice = None
                                st.session_state.start_drawing = False
                        except ValueError:
                            show_alert("숫자만 입력이 가능합니다.")

    with col2:
        with st.container(border=True):
            st.subheader("계산 결과")
            if st.session_state.calculated:
                total = int(st.session_state.final_total)
                people = int(st.session_state.num_people)
                st.markdown(f"#### 팁 포함 총 금액: {total:,}원")

                exact_per_person = total / people

                if int(exact_per_person) % 100 != 0:
                    if st.session_state.rounding_choice is None:
                        st.markdown(f"#### 1인당 금액: :green[{int(exact_per_person):,}원]")
                        st.info("💡 인원수대로 정확히 나누기에는 잔돈이 조금 남네요. 송금이 편하도록 100원 단위로 깔끔하게 맞춰드릴까요?")
                        b_yes1, b_no1 = st.columns(2)
                        if b_yes1.button("좋아요! 깔끔하게 맞춰주세요", key="b_yes1", type="primary"):
                            st.session_state.rounding_choice = 'yes';
                            st.rerun()
                        if b_no1.button("괜찮아요, 그냥 진행할게요", key="b_no1"):
                            st.session_state.rounding_choice = 'no';
                            st.rerun()

                    elif st.session_state.rounding_choice == 'no':
                        st.markdown(f"#### 1인당 금액: :green[{int(exact_per_person):,}원]")

                    elif st.session_state.rounding_choice == 'yes':
                        base_rounded = (total // people) // 100 * 100
                        remainder = total - (base_rounded * people)

                        if st.session_state.draw_choice is None:
                            st.info(
                                f"정리해볼까요?\n\n**1명은 {base_rounded + remainder:,}원**, **나머지 {people - 1}명은 {base_rounded:,}원**을 내면 됩니다.")
                            st.write("누가 더 낼지 번호를 뽑아볼까요?")
                            b_yes2, b_no2 = st.columns(2)
                            if b_yes2.button("네, 뽑아주세요", key="b_yes2", type="primary"):
                                st.session_state.draw_choice = 'yes';
                                st.rerun()
                            if b_no2.button("괜찮아요, 우리가 정할게요", key="b_no2"):
                                st.session_state.draw_choice = 'no';
                                st.rerun()

                        elif st.session_state.draw_choice == 'yes':
                            if not st.session_state.start_drawing:
                                st.warning(f"**잠깐!** 참여자 1번부터 {people}번까지 각자 누구일지 잠시 생각해주세요. 정하셨다면 아래 버튼을 눌러주세요!")
                                if st.button("🎲 추첨 시작!", type="primary", use_container_width=True):
                                    st.session_state.random_payer = random.randint(1, people)
                                    st.session_state.start_drawing = True
                                    st.rerun()
                            else:
                                st.success(f"🎉 당첨 결과! 참여자 {st.session_state.random_payer}번 당첨!")
                                for i in range(1, people + 1):
                                    if i == st.session_state.random_payer:
                                        st.write(f"- 🎯 **참여자 {i} (당첨!):** :red[{base_rounded + remainder:,}원]")
                                    else:
                                        st.write(f"- 👤 **참여자 {i}:** {base_rounded:,}원")

                        elif st.session_state.draw_choice == 'no':
                            st.success("🎉 자투리 금액을 낼 한 분을 정해주세요!")
                            st.write(f"- 🙋 **더 내는 1명:** :red[{base_rounded + remainder:,}원]")
                            st.write(f"- 👤 **나머지 {people - 1}명:** 각 {base_rounded:,}원")
                else:
                    st.markdown(f"#### 1인당 금액: :green[{int(exact_per_person):,}원]")
            else:
                st.info("왼쪽 박스에 값을 입력하고 제출을 눌러주세요.")


if __name__ == "__main__":
    main()
