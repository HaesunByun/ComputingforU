import streamlit as st
import pandas as pd

def project_list():

    st.title("📚 프로젝트 목록")

    # 엑셀 파일 불러오기
    excel_file = "./projects_with_top_keywords.xlsx"

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



def show_seating(class_number):
    """
    반 번호를 받아 좌석표를 표시하는 함수
    class_number : 1, 2, 3
    """
    # --- 엑셀 파일 불러오기 ---
    # 파일 이름: 'class_students.xlsx', 시트 이름: '1반', '2반', '3반'
    file_path = "class_students.xlsx"
    sheet_name = f"{class_number}반"
    try:
        df_students = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        st.error(f"학생 명단 불러오기 실패: {e}")
        return
    
    # 학생 이름 리스트
    students = df_students['이름'].tolist()
    
    # --- 좌석표 생성 ---
    rows, cols = 10, 8
    seat_index = 0
    seat_table = []

    for r in range(rows):
        row = []
        for c in range(cols):
            # 4열과 5열 사이는 통로
            if c == 4:
                row.append(" ")  # 통로 표시
            else:
                if seat_index < len(students):
                    row.append(students[seat_index])
                    seat_index += 1
                else:
                    row.append("")  # 빈 자리
        seat_table.append(row)
    
    # 데이터프레임으로 변환해서 테이블로 표시
    df_seating = pd.DataFrame(seat_table)
    st.table(df_seating)

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
        selected_class = st.sidebar.radio("반 선택:", ("1반", "2반", "3반"))
        class_number = int(selected_class[0])
        show_seating(class_number)


    elif menu == "기말 프로젝트 목록":
        project_list()

if __name__ == "__main__":
    main()
