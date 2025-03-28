import streamlit as st
import pandas as pd
import re

# 假设文件ID字典，文件名映射到 Google Drive 的文件 ID
file_ids = {
    "计算机系统原理": "165Nlke-27hsRVmoLj_mm3eye1oAsT4xm",
    "工作簿1": "1iqOn3l7PhnYTBImFsr-iT56So37r01FN",
    # 添加其他文件名称与ID的映射
}

def load_data(file_name):
    try:
        file_id = file_ids.get(file_name, "")
        if not file_id:
            st.error(f"未找到文件: {file_name}")
            return pd.DataFrame()

        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip()  # 清理列名空格
        return df
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")
        return pd.DataFrame()

def check_password():
    correct_pass = st.secrets.get("PASSWORD", "")

    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "attempts" not in st.session_state:
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

def extract_questions(text):
    # 更新正则表达式以支持多行输入
    pattern = r'(\d+)\.\s*(.*?)(?=（|学生答案：|$)'  # 捕获数字+题目内容，直到遇到 "（" 或 "学生答案："
    questions = re.findall(pattern, text, re.MULTILINE)
    return [q[1].strip() for q in questions]  # 只返回题干内容

st.title("Excel 数据查询系统 🔍")

check_password()  # 先进行密码检查

if st.session_state.auth:
    # 显示文件选择按钮
    st.subheader("请选择要查询的文件")
    
    # 为每个文件创建按钮，点击后加载对应的文件
    selected_file = None
    for file_name in file_ids.keys():
        if st.button(f"选择 {file_name}"):
            selected_file = file_name
            break  # 只允许选一个文件

    if selected_file:
        # 加载选中的文件
        if 'df' not in st.session_state or st.session_state.selected_file != selected_file:
            # 如果没有加载过这个文件或者是不同的文件，重新加载数据
            st.session_state.selected_file = selected_file
            st.session_state.df = load_data(selected_file)

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
                        for q_text in questions:
                            clean_q = ' '.join(q_text.strip().split())  # 清理题干的空格
                            result = df[df['题干'].str.contains(clean_q, case=False, na=False)]

                            if not result.empty:
                                answer = result.iloc[0]['答案(多选用英文逗号分隔)']
                                # 设置字体大小为 18px，并控制返回结果的样式
                                st.markdown(f"""
                                <p style="font-size:18px;"><b>题目:</b> {clean_q}</p>
                                <p style="font-size:18px;"><b>答案:</b> {answer}</p>
                                <hr style="border: 1px solid #ddd;"/>
                                """, unsafe_allow_html=True)
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
