import streamlit as st
import pandas as pd

# Fungsi untuk membaca data CSV dari file lokal
@st.cache_data
def load_data():
    data = pd.read_csv("journal_articles.csv")
    return data

# Fungsi untuk menampilkan card
def display_card(article_name, journal_name, article_url):
    return f"""
    <div style="border:1px solid #ccc; padding: 20px; margin: 15px; border-radius: 5px; width: 100%; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); text-align: justify;">
        <h5 style="margin: 0; font-size: 1.2em;">{article_name}</h5>
        <p style="margin: 5px 0; text-align: justify;">{journal_name}</p>
        <a href="{article_url}" target="_blank">
            <button style="background-color: #4CAF50; color: white; border: none; padding: 5px 7px; margin-top: 5px; border-radius: 5px; font-size: 0.9em;">
                Kunjungi Artikel
            </button>
        </a>
    </div>
    """

# Fungsi untuk menampilkan data dalam 3 kolom
def display_data(data, start_index, end_index):
    cols = st.columns(3)  # Buat 3 kolom
    for i in range(start_index, end_index):
        article_name = data.iloc[i]['article_name']
        journal_name = data.iloc[i]['journal_name']
        article_url = data.iloc[i]['article_url']
        
        # Menentukan kolom yang akan digunakan
        col_index = (i - start_index) % 3
        cols[col_index].markdown(display_card(article_name, journal_name, article_url), unsafe_allow_html=True)

# Main app
def main():
    st.set_page_config(page_title="ID CS Journal Aggregator", layout="wide")  # Set layout lebar
    
    # Judul terpusat
    st.markdown("<h1 style='text-align: center;'>Indonesian Computer Science<br>Journal Aggregator</h1>", unsafe_allow_html=True)

    # Load data dari file CSV
    data = load_data()

    # Inisialisasi jumlah data yang ditampilkan
    if 'num_displayed' not in st.session_state:
        st.session_state.num_displayed = 9  # Jumlah card yang ditampilkan awalnya

    # Tampilkan data
    end_index = min(st.session_state.num_displayed, len(data))
    display_data(data, 0, end_index)

    # Tombol "Show More"
    if st.session_state.num_displayed < len(data):
        if st.button("Show More"):
            st.session_state.num_displayed += 9  # Tambah jumlah card yang ditampilkan

if __name__ == "__main__":
    main()
