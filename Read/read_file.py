import streamlit as st
import pandas as pd
import re

# 认证逻辑封装
def check_password():
    correct_pass = st.secrets.get("PASSWORD", "")
    
    # 初始化认证状态和错误次数
    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.attempts = 0  # 错误次数

    # 如果用户尚未认证且未超过最大错误次数
    if not st.session_state.auth:
        if st.session_state.attempts >= 3:
            st.error("三次密码错误，禁止访问")
            st.stop()  # 停止继续执行

        password = st.text_input("请输入访问密码：", type="password")

        if password == correct_pass:
            st.session_state.auth = True  # 认证成功
            st.success("密码正确，访问成功！")
        elif password != "":
            st.session_state.attempts += 1  # 增加错误次数
            st.error(f"密码错误，剩余尝试次数: {3 - st.session_state.attempts}")

# 调用密码验证
check_password()

# 加载数据函数
def load_data():
    try:
        file_id = "165Nlke-27hsRVmoLj_mm3eye1oAsT4xm"
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip()  # 去除列名中的空格
        return df
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")
        return pd.DataFrame()

# 提取题干部分的函数
def extract_question_content(input_text):
    # 使用正则表达式来提取题干（假设题干是冒号前的部分）
    # 例如： "下列选项中那个是A（）:" -> "下列选项中那个是A"
    question_list = []
    
    # 分割输入文本，按每个问题来处理
    problems = input_text.split("\n\n")  # 每两个空行分割问题

    for problem in problems:
        # 去除问题的选项部分（假设每个问题的选项是以 'AA.' 等标记）
        # 使用正则去掉每个选项的部分，提取题干
        match = re.match(r"([^\n]+?)(?=\s*[A-Z]+\.)", problem)  # 匹配题干部分
        if match:
            question_list.append(match.group(1).strip())

    return question_list

# 页面布局
st.title("Excel 数据查询系统 🔍")

# 只有认证成功后才能加载数据
if st.session_state.auth:
    # 加载数据（只在没有加载过的情况下）
    if 'df' not in st.session_state:
        st.session_state.df = load_data()

    df = st.session_state.df

    if not df.empty:
        with st.expander("查看完整数据"):
            st.dataframe(df)

        st.subheader("数据查询")
        input_text = st.text_area("请输入多个题干内容（每个题干之间请用换行符分隔）：")

        if input_text:
            # 提取题干内容
            extracted_questions = extract_question_content(input_text)

            # 查找包含在题干中的每个提取的题干
            if '题干' in df.columns and '答案(多选用英文逗号分隔)' in df.columns:
                matching_rows = []

                # 对每个提取的题干进行匹配查询
                for question in extracted_questions:
                    # 对每个题干内容进行模糊查询
                    result = df[df['题干'].astype(str).str.contains(question, case=False, na=False)]

                    # 收集匹配的行
                    matching_rows.append(result)

                # 合并所有匹配结果
                if matching_rows:
                    final_result = pd.concat(matching_rows).drop_duplicates()

                    if not final_result.empty:
                        st.success(f"查询成功！找到以下匹配结果：")
                        for _, row in final_result.iterrows():
                            st.markdown(f"""
                            **题干**: {row['题干']}  
                            **答案**: {row['答案(多选用英文逗号分隔)']}  
                            """)
                    else:
                        st.warning("未找到匹配结果，请尝试其他题干内容")
                else:
                    st.warning("未找到匹配结果，请尝试其他题干内容")
            else:
                st.error("数据中缺少 '题干' 或 '答案(多选用英文逗号分隔)' 列，无法执行查询。请检查数据文件。")
    else:
        st.error("数据加载失败，请检查文件链接或格式。")

else:
    st.warning("请输入密码才能访问数据。")

# 侧边栏说明
st.sidebar.markdown("""
### 使用说明
1. 确保您的 Excel 文件包含 '题干' 和 '答案(多选用英文逗号分隔)' 两列。
2. 将文件上传到 Google Drive 并设置共享。
3. 替换代码中的文件 ID。
4. 输入题干内容，支持多个题干查询，每个题干内容之间请使用换行符分隔。
""")
