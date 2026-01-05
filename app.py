import streamlit as st
import pandas as pd
import numpy as np

# Sarlavha
st.title("Salom, Streamlit ishga tushdi!")

# Oddiy ma'lumotlar jadvali
st.write("Quyida oddiy DataFrame ko'rsatiladi:")
df = pd.DataFrame({
    "Sonlar": np.arange(1, 6),
    "Kvadratlari": np.arange(1, 6)**2
})
st.dataframe(df)

# Oddiy chizma
st.write("Oddiy chizma:")
st.line_chart(df["Kvadratlari"])
