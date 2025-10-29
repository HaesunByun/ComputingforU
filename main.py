import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import urllib.parse
import os
import matplotlib.font_manager as fm

def project_list():

    st.title("📚 프로젝트 목록")

    # 엑셀 파일 불러오기
    excel_file = "projects_with_top_keywords.xlsx"

    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        st.error(f"❌ 엑셀 파일 불러오기 실패: {e}")
        st.stop()

    # 필수 컬럼 체크
    if '학기' not in df.columns or '주제' not in df.columns or '키워드' not in df.columns:
        st.error("❗ '학기', '주제', '키워드' 컬럼이 모두 필요합니다.")
        st.stop()

    df['키워드목록'] = df['키워드'].fillna("").apply(lambda x: [k.strip() for k in x.split(',') if k.strip()])

    semesters = sorted(df['학기'].dropna().unique())
    semester_options = ["전체"] + semesters
    selected_semester = st.selectbox("📅 학기 선택", semester_options)

    from collections import Counter
    all_keywords = [k for kws in df['키워드목록'] for k in kws]
    keyword_counts = Counter(all_keywords)
    keyword_options = ["전체"] + [f"{k} ({keyword_counts[k]})" for k in sorted(keyword_counts.keys())]

    def extract_keyword(selected):
        if selected == "전체":
            return "전체"
        return selected.split(" (")[0]

    selected_keyword_with_count = st.selectbox("🔑 키워드 선택", keyword_options)
    selected_keyword = extract_keyword(selected_keyword_with_count)

    filtered_df = df.copy()
    if selected_semester != "전체":
        filtered_df = filtered_df[filtered_df['학기'] == selected_semester]
    if selected_keyword != "전체":
        filtered_df = filtered_df[filtered_df['키워드목록'].apply(lambda kws: selected_keyword in kws)]

    exclude_columns = ['키워드', '순번']
    display_df = filtered_df.drop(columns=exclude_columns, errors='ignore')    

    st.subheader(f"📋 조회 결과 ({len(display_df)}건)")
    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)

    project_options = display_df['주제'].dropna().unique().tolist()
    selected_project = st.selectbox("🎯 프로젝트를 선택하세요", project_options)

    if selected_project:
        st.markdown("### 🔖 선택한 주제")
        st.code(selected_project, language='')
        st.success("📋 위 텍스트를 복사(Ctrl+C) 후 구글폼에 붙여넣으세요.")

        entry_id = "entry.1166974659"
        form_url = (
            "https://docs.google.com/forms/d/e/1FAIpQLSdU0UZ79ABI4ZpjGRBYsI0wE2BCIXxRVZTM2g2JdNnyHUsUQA/viewform"
            f"?usp=pp_url&{entry_id}={urllib.parse.quote(selected_project)}"
        )
        st.markdown(f"[📩 Google Form으로 이동]({form_url})", unsafe_allow_html=True)

# def add_numbers_to_names(input_file, output_file, sheets):
#     """
#     엑셀 파일의 각 시트에 있는 학생 이름 앞에 번호를 붙여 새 파일로 저장하는 함수.
    
#     Parameters:
#     - input_file : str : 원본 엑셀 파일 경로
#     - output_file : str : 번호가 붙은 새 엑셀 파일 경로
#     - sheets : list : 처리할 시트 이름 리스트
#     """
#     with pd.ExcelWriter(output_file) as writer:
#         for sheet in sheets:
#             # 시트 불러오기
#             df = pd.read_excel(input_file, sheet_name=sheet)
            
#             # '성명' 컬럼에 번호 붙이기
#             df['성명'] = [f"{i+1}. {name}" for i, name in enumerate(df['성명'].dropna())]
            
#             # 기존 NaN은 그대로 두고 시트 저장
#             df.to_excel(writer, sheet_name=sheet, index=False)
    


# def show_seating(class_number):
#     """
#     반 번호를 받아 좌석표를 표시하는 함수
#     class_number : 1, 2, 3
#     """
#     file_path = "class_students_numbered.xls"
#     sheet_name = f"{class_number}반"

#     # ✅ 반이 바뀌면 전체 상태 초기화
#     if "current_class" not in st.session_state or st.session_state.current_class != class_number:
#         st.session_state.clear()
#         st.session_state.current_class = class_number

#     # --- 엑셀 파일 불러오기 ---
#     try:
#         df_students = pd.read_excel(file_path, sheet_name=sheet_name)
#     except Exception as e:
#         st.error(f"학생 명단 불러오기 실패: {e}")
#         return

#     # ✅ 이름 앞에 번호 붙이기
#     students = df_students['성명'].dropna().tolist()

#     rows, cols = 10, 9

#     # --- 좌석표 생성 (처음이거나 비어있을 때만) ---
#     if "seat_table" not in st.session_state or len(st.session_state.seat_table) == 0:
#         seat_table = []
#         seat_index = 0
#         for r in range(rows):
#             row = []
#             for c in range(cols):
#                 if c == 4:
#                     row.append(" ")  # 통로
#                 else:
#                     if seat_index < len(students):
#                         row.append(students[seat_index])
#                         seat_index += 1
#                     else:
#                         row.append("")  # 빈 자리
#             seat_table.append(row)
#         st.session_state.seat_table = seat_table

#     # --- 선택 상태 저장 ---
#     if "selected_student" not in st.session_state:
#         st.session_state.selected_student = None
#         st.session_state.selected_pos = None

#     st.write(f"🪑 **{class_number}반 좌석표 (이름 클릭 → 빈칸 클릭으로 이동)**")

#     # --- 좌석 테이블 표시 ---
#     for r in range(rows):
#         cols_in_row = st.columns(cols)
#         for c in range(cols):
#             name = st.session_state.seat_table[r][c]


#             if name == " ":
#                 cols_in_row[c].markdown(" ")
#                 continue

#             label = name if name else "⬜️"

#             clicked = cols_in_row[c].button(label, key=f"seat_{r}_{c}_{class_number}")

#             if clicked:
#                 # 이름 클릭 시 → 선택
#                 if name and name.strip() != "":
#                     st.session_state.selected_student = name
#                     st.session_state.selected_pos = (r, c)
#                     st.experimental_rerun()

#                 # 빈칸 클릭 시 → 이동
#                 elif (not name or name.strip() == "") and st.session_state.selected_student:
#                     src_r, src_c = st.session_state.selected_pos
#                     if st.session_state.seat_table[src_r][src_c] and st.session_state.seat_table[r][c] != " ":
#                         st.session_state.seat_table[r][c] = st.session_state.selected_student
#                         st.session_state.seat_table[src_r][src_c] = ""
#                         st.session_state.selected_student = None
#                         st.session_state.selected_pos = None
#                         st.experimental_rerun()

#     # --- 선택 상태 표시 ---
#     if st.session_state.selected_student:
#         st.info(f"선택된 학생: **{st.session_state.selected_student}** — 이동할 빈칸을 클릭하세요.")

def show_seating(class_number):
    """
    반 번호를 받아 좌석표를 표시하는 함수
    class_number : 1, 2, 3
    """
    import pandas as pd
    import streamlit as st

    file_path = "class_students_numbered.xls"
    sheet_name = f"{class_number}반"
    
    # --- 반 바뀌면 전체 상태 초기화 ---
    if "current_class" not in st.session_state or st.session_state.current_class != class_number:
        st.session_state.clear()
        st.session_state.current_class = class_number

    # --- 엑셀 파일 불러오기 ---
    try:
        df_students = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        st.error(f"학생 명단 불러오기 실패: {e}")
        return

    students = df_students['성명'].dropna().tolist()  # 이미 번호가 붙어 있음

    rows, cols = 10, 9  # 4열-5열 통로 포함

    # --- 좌석표 생성 ---
    if "seat_table" not in st.session_state or st.session_state.current_class != class_number:
        seat_table = []
        seat_index = 0
        for r in range(rows):
            row = []
            for c in range(cols):
                if c == 4:
                    row.append(" ")  # 통로
                else:
                    if seat_index < len(students):
                        row.append(students[seat_index])
                        seat_index += 1
                    else:
                        row.append("")  # 빈 자리
            seat_table.append(row)
        st.session_state.seat_table = seat_table

    # --- 선택 상태 초기화 ---
    if "selected_student" not in st.session_state:
        st.session_state.selected_student = None
        st.session_state.selected_pos = None

    st.write(f"🪑 **{class_number}반 좌석표 (이름 클릭 → 빈칸 클릭으로 이동)**")

    # --- 좌석 테이블 표시 ---
    for r in range(rows):
        cols_in_row = st.columns(cols)
        for c in range(cols):
            name = st.session_state.seat_table[r][c]

            if name == " ":
                cols_in_row[c].markdown(" ")  # 통로
                continue

            label = name if name else "⬜️"

            # 버튼 key에 이름 포함 → 레이블 변경시 새로 렌더링
            clicked = cols_in_row[c].button(label, key=f"seat_{r}_{c}_{class_number}_{name}")

            if clicked:
                # 이름 클릭 시 → 선택
                if name and name.strip() != "":
                    st.session_state.selected_student = name
                    st.session_state.selected_pos = (r, c)
                    st.experimental_rerun()

                # 빈자리 클릭 시 → 이동
                elif (not name or name.strip() == "") and st.session_state.selected_student:
                    src_r, src_c = st.session_state.selected_pos
                    if st.session_state.seat_table[src_r][src_c] and st.session_state.seat_table[r][c] != " ":
                        st.session_state.seat_table[r][c] = st.session_state.selected_student
                        st.session_state.seat_table[src_r][src_c] = ""
                        st.session_state.selected_student = None
                        st.session_state.selected_pos = None
                        st.experimental_rerun()

    # --- 선택 상태 안내 ---
    if st.session_state.selected_student:
        st.info(f"선택된 학생: **{st.session_state.selected_student}** — 이동할 빈칸을 클릭하세요.")


def main():
    st.set_page_config(page_title="컴퓨팅", layout="wide")

    # --- 사이드바 메뉴 ---
    menu = st.sidebar.radio(
        "메뉴 선택",
        ["중간고사 좌석배치도", "기말 프로젝트 목록"]
    )

    # --- 오른쪽 화면 내용 ---
    if menu == "중간고사 좌석배치도":
        # 반 선택
        # --- 사용 예시 ---
        # input_file = "class_students.xls"
        # output_file = "class_students_numbered.xls"
        # sheets = ["1반", "2반", "3반"]

        #add_numbers_to_names(input_file, output_file, sheets)        
        selected_class = st.sidebar.radio("반 선택:", ("1반", "2반", "3반"))
        class_number = int(selected_class[0])
        show_seating(class_number)


    elif menu == "기말 프로젝트 목록":
        project_list()

if __name__ == "__main__":
    main()
