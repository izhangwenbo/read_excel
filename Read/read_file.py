import streamlit as st
import pandas as pd


# 认证逻辑封装
def check_password():
    correct_pass = st.secrets.get("PASSWORD", "")

    # 如果 session_state 没有存储认证状态
    if "auth" not in st.session_state:
        password = st.text_input("请输入访问密码：", type="password")
        if password == correct_pass:
            st.session_state.auth = True
        elif password != "":
            st.error("密码错误，禁止访问")
            st.stop()

    elif st.session_state.auth is False:
        st.error("认证失败，禁止访问")
        st.stop()


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


# 页面布局
st.title("Excel 数据查询系统 🔍")

# 加载数据（只在没有加载过的情况下）
if 'df' not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

if not df.empty:
    with st.expander("查看完整数据"):
        st.dataframe(df)

    st.subheader("数据查询")
    search_input = st.text_input("请输入要查询的B列内容：")

    if search_input:
        if '题干' in df.columns and '答案(多选用英文逗号分隔)' in df.columns:
            result = df[df['题干'].astype(str).str.contains(search_input, case=False, na=False)]

            if not result.empty:
                st.success("查询成功！找到以下匹配结果：")
                for _, row in result.iterrows():
                    st.markdown(f"""
                    **B列内容**: {row['题干']}  
                    **I列答案**: {row['答案(多选用英文逗号分隔)']}  
                    """)
            else:
                st.warning("未找到匹配结果，请尝试其他关键词")
        else:
            st.error("数据中缺少 '题干' 或 '答案(多选用英文逗号分隔)' 列，无法执行查询。请检查数据文件。")
else:
    st.error("数据加载失败，请检查文件链接或格式。")

# 侧边栏说明
st.sidebar.markdown("""
### 使用说明
1. 确保您的 Excel 文件包含 '题干' 和 '答案(多选用英文逗号分隔)' 两列。
2. 将文件上传到 Google Drive 并设置共享。
3. 替换代码中的文件 ID。
4. 输入要查询的 B 列内容即可获取对应的答案。
""")
