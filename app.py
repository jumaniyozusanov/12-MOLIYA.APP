import streamlit as st
import pandas as pd

st.set_page_config(page_title="Moliyaviy Hisobot", layout="wide")
st.title("Moliyaviy Hisobot Dashboard")

# Example table
data = {
    "Oy": ["Yanvar", "Fevral", "Mart"],
    "Daromad": [1200, 1500, 1100],
    "Xarajat": [800, 900, 700]
}
df = pd.DataFrame(data)

st.subheader("Oylar bo‘yicha daromad va xarajatlar")
st.table(df)

st.success("App ishga tushdi! 🎉")
