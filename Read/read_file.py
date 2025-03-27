# *coding:utf-8 *
import streamlit as st
import pandas as pd


# 读取云端 Excel 文件（示例使用 Google Drive）
def load_data():
    # 替换为你的 Google Drive 文件 ID（在分享链接中获取）
    file_id = "1iqOn3l7PhnYTBImFsr-iT56So37r01FN"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return pd.read_excel(url)


# 页面布局
st.title("Excel 数据查询系统 🔍")

# 加载数据
df = load_data()

# 显示原始数据（可选）
with st.expander("查看完整数据"):
    st.dataframe(df)

# 查询功能
st.subheader("数据查询")
search_input = st.text_input("请输入要查询的B列内容：")

if search_input:
    # 执行查询
    result = df[df['B'].astype(str).str.contains(search_input, case=False)]

    if not result.empty:
        st.success("查询成功！找到以下匹配结果：")
        for _, row in result.iterrows():
            st.markdown(f"""
            **B列内容**: {row['B']}  
            **C列答案**: {row['C']}  
            """)
    else:
        st.warning("未找到匹配结果，请尝试其他关键词")

# 侧边栏说明
st.sidebar.markdown("""
### 使用说明
1. 确保您的 Excel 文件包含 A、B、C、D 四列
2. 将文件上传到 Google Drive 并设置共享
3. 替换代码中的文件 ID
4. 输入要查询的 B 列内容即可获取 C 列答案
""")