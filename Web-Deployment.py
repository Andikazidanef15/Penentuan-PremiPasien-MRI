import streamlit as st
import pandas as pd
import altair as alt
from premi_count import premi_pasien
from CleaningData import data_cleaner

st.set_page_config(layout="wide")  # this needs to be the first Streamlit command

# Definisikan Container
header = st.container()
dataset = st.container()
EDA = st.container()
features = st.container()

# Baca data dan bersihkan data
df = pd.read_excel("C:/Users/acer/Documents/Python/venv/Pemodelan Matematika/Data MRI.xlsx")
df = data_cleaner(df)

# Sidebar
title_sidebar = st.sidebar.title("Identitas Pasien MRI : ")
nama = st.sidebar.text_input("Masukkan nama Anda : ")
usia = st.sidebar.number_input("Masukkan usia Anda : ")
jenis_pelayanan = st.sidebar.selectbox('Jenis Pelayanan :', list(df['rnmjasa'].unique()))
biaya_pengobatan = st.sidebar.number_input("Masukkan perkiraan biaya pemeriksaan MRI Anda : ")
pilih_kasus = st.sidebar.selectbox('Kasus yang dipakai :', ('KASUS 1.1','KASUS 1.2','KASUS 1.3'))

with header:
    st.title("Prediksi Premi Pasien MRI")

    st.markdown("Web ini didesain sebagai uji coba penentuan premi pasien MRI berdasarkan informasi usia dan biaya pengobatan pasien tersebut, credit to **Kelompok 18 MA3271 Pemodelan Matematika 2021/2022**")
    st.markdown("* **Sekar Annasya H - 10119001**")
    st.markdown("* **Alfini Ridatillah - 10119013**")
    st.markdown("* **Alfina Rahmadina - 10119015**")
    st.markdown("* **M. Pudja Gemilang - 10119055**")
    st.markdown("* **Andika Zidane Faturrahman - 10119111**")
    st.markdown(",dan juga dosen pembimbing Kelompok 18 : **Ibu Novriana Sumarti, S.Si., M.Si., Ph.D.**")

with dataset:
    st.header("Data Pemodelan")
    st.markdown("Data ini adalah basis untuk pemodelan premi ini, data berasal dari suatu klinik MRI")
    st.write(df.head(5))

with EDA:
    st.header("Exploratory Data Analysis (EDA)")
    st.markdown("**Jumlah pasien di setiap pelayanan**")

    # Bar Plot Jumlah Pelayanan
    pelayanan_count = df['rnmjasa'].value_counts().to_frame().sort_values(by = 'rnmjasa').reset_index()
    fig1 = alt.Chart(pelayanan_count).mark_bar().encode(x = alt.X('rnmjasa'), y = alt.Y('index', title="Pelayanan", sort='-x'))
    st.altair_chart(fig1, use_container_width = True)

    # Dinamika Premi pada Pasien Layanan Tertentu
    pasien = premi_pasien(nama, usia, jenis_pelayanan, biaya_pengobatan, "KASUS 1.3", df)
    st.markdown("**Grafik Premi dan Biaya Pasien MRI {}**".format(jenis_pelayanan))
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(pasien.dinamika_premi())

    # Distribusi Biaya
    st.markdown("**Diagram Distribusi Total Biaya**")
    total_biaya_df = df[['total_biaya']]
    fig2 = alt.Chart(total_biaya_df).mark_bar().encode(x = alt.X("total_biaya", title = "Total Biaya", bin = True), y = alt.Y('count()', title = "Jumlah Pasien"))
    st.altair_chart(fig2, use_container_width = True)

    # Distribusi Rentang Usia
    st.markdown("**Diagram Distribusi Usia Pasien**")
    usia_df = df[['umur']]
    fig3 = alt.Chart(usia_df).mark_bar().encode(x = alt.X("umur", title = "Umur Pasien", bin = True), y = alt.Y('count()', title = "Jumlah Pasien"))
    st.altair_chart(fig3, use_container_width=True)

with features:
    st.header("Informasi Pasien : ")

    pasien = premi_pasien(nama, usia, jenis_pelayanan, biaya_pengobatan, pilih_kasus, df)
    st.markdown("* **Identitas Pasien**  ")
    st.write(pasien.introduksi_pasien())

    st.markdown("* **Premi yang dibayarkan oleh Pasien** ")
    st.write(pasien.premi_yang_dibayarkan())
