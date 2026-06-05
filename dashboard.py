import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Ayrılan Gemiler Dashboard")

# CSV dosyası
df = pd.read_csv("data/departures.csv")

st.subheader("Gemi Listesi")
st.dataframe(df)

st.subheader("Günlük Ayrılan Gemi Sayısı")
# arrival tarihi üzerinden count
df['departure'] = pd.to_datetime(df['departure'], errors='coerce')
daily_count = df.groupby(df['departure'].dt.date).size()

fig, ax = plt.subplots()
daily_count.plot(kind='bar', ax=ax)
ax.set_xlabel("Tarih")
ax.set_ylabel("Gemi Sayısı")
st.pyplot(fig)
