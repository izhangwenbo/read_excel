# *coding:utf-8 *
import streamlit as st
import pandas as pd

# 读取云端 Excel 文件（示例使用 Google Drive）
def load_data():
    try:
        file_id = "1iqOn3l7PhnYTBImFsr-iT56So37r01FN"
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")
        return pd.DataFrame()

# 页面布局
st.title("Excel 数据查询系统 🔍")

# 加载数据
df = load_data()

if not df.empty:
    with st.expander("查看完整数据"):
        st.dataframe(df)

    st.subheader("数据查询")
    search_input = st.text_input("请输入要查询的B列内容：")

    if search_input:
        if '题干' in df.columns and '答案(多选用英文逗号分隔)' in df.columns:
            result = df[df['题干'].astype(str).str.contains(search_input, case=False)]

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
            st.error("数据中缺少 'B' 列或 'C' 列，无法执行查询。请检查数据文件。")
else:
    st.error("数据加载失败，请检查文件链接或格式。")

# 侧边栏说明
st.sidebar.markdown("""
### 使用说明
1. 确保您的 Excel 文件包含 A、B、C、D 四列
2. 将文件上传到 Google Drive 并设置共享
3. 替换代码中的文件 ID
4. 输入要查询的 B 列内容即可获取 C 列答案
""")
