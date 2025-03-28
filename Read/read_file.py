import streamlit as st
import pandas as pd
import re


def check_password():
    correct_pass = st.secrets.get("PASSWORD", "")

    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.attempts = 0

    if not st.session_state.auth:
        if st.session_state.attempts >= 3:
            st.error("三次密码错误，禁止访问")
            st.stop()

        password = st.text_input("请输入访问密码：", type="password")

        if password == correct_pass:
            st.session_state.auth = True
            st.success("密码正确，访问成功！")
        elif password != "":
            st.session_state.attempts += 1
            st.error(f"密码错误，剩余尝试次数: {3 - st.session_state.attempts}")


def load_data():
    try:
        file_id = "165Nlke-27hsRVmoLj_mm3eye1oAsT4xm"
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")
        return pd.DataFrame()


def extract_questions(text):
    # 提取题目的函数，通过正则表达式捕获题干内容
    pattern = r'(\d+)\.\s*(.*?)\s*(?:学生答案：|$)'
    questions = re.findall(pattern, text)
    return questions


st.title("Excel 数据查询系统 🔍")

if st.session_state.auth:
    if 'df' not in st.session_state:
        st.session_state.df = load_data()
    df = st.session_state.df

    if not df.empty:
        with st.expander("查看完整数据"):
            st.dataframe(df)

        st.subheader("输入待查询的题目内容")

        user_input = st.text_area("请在此处粘贴题目内容（支持多题批量查询）", height=200)

        if st.button("开始查询"):
            if user_input:
                # 提取题干信息
                questions = extract_questions(user_input)

                if questions:
                    st.success(f"共找到 {len(questions)} 道题目，开始查询...")

                    # 循环查询每一道题
                    for q_id, q_text in questions:
                        clean_q = ' '.join(q_text.strip().split())
                        result = df[df['题干'].str.contains(clean_q, case=False, na=False)]

                        if not result.empty:
                            answer = result.iloc[0]['答案(多选用英文逗号分隔)']
                            st.markdown(f"""
                            **题目**: {clean_q}  
                            **答案**: {answer}  
                            ---
                            """)
                        else:
                            st.warning(f"未找到匹配题目: {clean_q}")
                else:
                    st.error("未检测到有效题目格式，请确保题目以 '数字. 内容' 格式输入")
            else:
                st.warning("请输入内容后再点击查询")
    else:
        st.error("数据加载失败")
else:
    st.warning("请输入密码访问")

st.sidebar.markdown("""
### 使用说明
1. 确保您的 Excel 文件包含 '题干' 和 '答案(多选用英文逗号分隔)' 两列。
2. 将文件上传到 Google Drive 并设置共享。
3. 替换代码中的文件 ID。
4. 输入要查询的题干内容即可获取对应的答案。
""")
