import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import seaborn as sns 
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

px.defaults.template = 'plotly_dark'

# read excel
df = pd.read_excel("USA_cars_datasets.xlsx")

# Modified Excel, memunculkan data B= Age dan D= Event
df1 = pd.read_excel("USA_cars_datasets.xlsx", usecols='L')

excel_file = 'USA_cars_datasets.xlsx'


st.set_page_config(
    page_title = 'USA Car Dataset Visualisation',
    page_icon = '🚗',
    layout = 'wide',
)

# dashboard title

st.title("Visualisasi Data Kelompok 10")



# Logo Mobil
st.sidebar.image('Logo.png', caption="Final Project Data Visualization")
    




option = st.sidebar.selectbox(
    '**Silakan pilih:**',
    ('Home','Analysis','EDA')
)

if option == 'Home' or option == '':
    st.write("""# USA Cars Dataset""") #menampilkan halaman utama
    st.markdown(
    "Kami menggunakan data penjualan mobil di USA yang terdiri dari Harga, Brand, Model, Tahun, Kondisi Kendaraan, dll.")
    
    img=Image.open('USA Cars.jpg')
    st.image(img,width=700)

    st.write('**Ini adalah data penjualan mobil di USA dari tahun 1973-2020**')
    df #menampilkan dataframe

      



elif option == 'Analysis':

    year = st.sidebar.slider(
    "Select the Year:",
    min_value=min(df["year"]),
    max_value=max(df["year"]),
    value=(min(df["year"]), max(df["year"]))
    )

    df_selection = df.query(
        "year >= @year[0] and year <= @year[1]"
    )

  
    

    # Mengelompokkan data berdasarkan brand dan tahun, kemudian menghitung total penjualan
    brand_count = df_selection.groupby(['year', 'brand']).size().reset_index(name='count')

    # Menampilkan line chart penjualan mobil per tahun
    fig = px.line(brand_count, x='year', y='count', color='brand',
                title='Trend Penjualan Brand Mobil per Tahun', labels={'year': 'Tahun', 'count': 'Jumlah Penjualan'})
    st.plotly_chart(fig)


    #LINE CHART MODEL
    
    # Mengelompokkan data berdasarkan brand dan tahun, kemudian menghitung total penjualan
    model_count = df_selection.groupby(['year', 'model']).size().reset_index(name='count')

    # Menampilkan line chart penjualan mobil per tahun
    fig = px.line(model_count, x='year', y='count', color='model',
                title='Penjualan Model Mobil per Tahun', labels={'year': 'Tahun', 'count': 'Jumlah Penjualan'})
    st.plotly_chart(fig)



    # WORD CLOUD
    st.markdown("### Word Cloud")

         # Preprocessing teks
    text = df['brand'].values
    text = ' '.join(text)

        # Sidebar untuk mengatur parameter WordCloud
    st.sidebar.title("WordCloud Options")
    max_words = st.sidebar.slider("Max Words", min_value=5, max_value=100, value=50)
    background_color = st.sidebar.selectbox("Background Color", ["black", "white"])
    collocations = st.sidebar.checkbox("Include Collocations", value=False)

        # Membuat WordCloud
    wc = WordCloud(background_color=background_color, width=1200, height=600,
                    contour_width=0, contour_color="#410F01", max_words=max_words,
                    scale=1, collocations=collocations, repeat=True, min_font_size=1)

        # Mengenerate dan menampilkan WordCloud saat ada perubahan pada parameter
    @st.cache
    def generate_wordcloud():
            wc.generate(text)
            plt.figure(figsize=[12, 6])
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            return plt

        # Menampilkan WordCloud dalam aplikasi Streamlit
    st.title("Top Words in the Text")
    st.pyplot(generate_wordcloud())




    
    # #TREND CHARTa
    # st.markdown('### Trend Chart')
    # data = pd.read_excel("USA_cars_datasets.xlsx", "trend")

    # # Group the data by year and calculate the sum of data amount
    # data_grouped = data.groupby('tahun')['jumlah'].sum().reset_index()

    # # Create a line plot to visualize the trend
    # plt.plot(data_grouped['tahun'], data_grouped['jumlah'], marker='o')
    # plt.xlabel('Tahun')
    # plt.ylabel('Jumlah Data')
    # plt.title('Trend of USA Cara Dataset')
    # plt.grid(True)

    # # Display the plot using Streamlit
    # st.pyplot(plt)


   
    



    
    #TOP 5 BRAND DIBELI

    top_5 = df['brand'].value_counts().nlargest(5).reset_index()
    fig7 = px.bar(data_frame=top_5, x='brand', y='count', title='Top 5 Brand Terpopuler')

    fig7.update_layout(
            xaxis={'title': 'Brand'},
            yaxis={'title': 'Total'}
        )

    st.plotly_chart(fig7)


    #TOP 5 BRAND BERDASARKAN BRAND FORD
    df3 = pd.read_excel("USA_cars_datasets.xlsx", 'model')
    top_5 = df3['model'].value_counts().nlargest(5).reset_index()
    fig11 = px.bar(data_frame=top_5, x='model', y='count', title='Top 5 Model Terpopuler Berdasarkan Brand Ford')

    fig11.update_layout(
            xaxis={'title': 'Model'},
            yaxis={'title': 'Total'}
        )

    st.plotly_chart(fig11)
    

    #MODEL POPULER
    top_5 = df['model'].value_counts().nlargest(5).reset_index()
    fig11 = px.bar(data_frame=top_5, x='model', y='count', title='Top 5 Model Populer Semua Brand')

    fig11.update_layout(
            xaxis={'title': 'Model'},
            yaxis={'title': 'Total'}
        )

    st.plotly_chart(fig11)



    # Top 5 WARNA MOBIl

    top_5 = df['colour'].value_counts().nlargest(5).reset_index()
    colors = ['white', 'black', 'grey', 'silver', 'red']
    fig10 = px.bar(data_frame=top_5, color=colors, x='colour', y='count', title='Top 5 Warna yang digunakan')

    fig10.update_layout(
            xaxis={'title': 'Color'},
            yaxis={'title': 'Total'}
        )

    st.plotly_chart(fig10)


    # # Menghitung jumlah total setiap warna
    # color_counts = df['color'].value_counts()

    # # Mengambil 3 warna dengan data terbanyak
    # top_colors = color_counts.head(3)

    # # Daftar warna yang akan digunakan pada histogram
    # colors = ['#47A992', 'black', 'grey']

    # # Menampilkan histogram
    # fig3, ax = plt.subplots()
    # ax.bar(top_colors.index, top_colors.values, color=colors)

    # ax.set_xlabel('Warna')
    # ax.set_ylabel('Frekuensi')
    # ax.set_title('Histogram Total Banyaknya Warna')
   

    # st.pyplot(fig3)

    



    #MOBIL TERMAHAL
    # Mengurutkan data berdasarkan harga mobil secara menurun
    df_sorted = df.sort_values(by='price', ascending=False)

    # Mengambil 5 data brand mobil dengan harga termahal
    top_brands = df_sorted['brand'].head(5)

    # Mengambil harga mobil dari 5 data brand teratas
    top_prices = df_sorted['price'].head(5)

    # Menampilkan diagram batang horizontal
    fig4, ax = plt.subplots()
    ax.barh(top_brands, top_prices)

    ax.set_xlabel('Harga Mobil')
    ax.set_ylabel('Brand Mobil')
    ax.set_title('Top 3 Mobil dengan Harga Termahal')
    ax.invert_yaxis()

    st.pyplot(fig4)


    #TOP 5 NEGARA

    # Mengambil data top 5 negara
    top_5 = df['state'].value_counts().reset_index()

    # Membuat horizontal bar chart
    fig10 = px.bar(data_frame=top_5, y='state', x='count', orientation='h', title='Top 5 Mobil Terjual Berdasarkan Kota')

    fig10.update_layout(
        xaxis={'title': 'Total'},
        yaxis={'title': 'Kota'}
    )

    # Menampilkan horizontal bar chart menggunakan Plotly
    st.plotly_chart(fig10)






    # PIE CHART
    st.write("### Pie Chart")
    # Membaca FILE EXCEL BEDA
    df55 = pd.read_excel('USA_cars_datasets.xlsx', engine='openpyxl', usecols='F,L')

    # Memilih kolom yang berisi data untuk pie chart
    column_name = st.selectbox('Pilih Kolom', df55.columns.tolist())

    # Menghitung frekuensi setiap nilai dalam kolom
    value_counts = df55[column_name].value_counts()

    # Membuat pie chart
    fig2, ax = plt.subplots()
    ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Membuat lingkaran menjadi proporsional
    ax.legend()

    # Menampilkan pie chart menggunakan Streamlit
    st.pyplot(fig2)

    # Menampilkan jumlah data
    st.write(f"Jumlah Data Keseluruhan: {len(df55)}")

    # Menampilkan jumlah data terbanyak
    most_common_value = value_counts.idxmax()
    most_common_count = value_counts.max()
    st.write(f"Jumlah Data Terbanyak ({most_common_value}): {most_common_count}")

    # Menampilkan jumlah data terkecil
    least_common_value = value_counts.idxmin()
    least_common_count = value_counts.min()
    st.write(f"Jumlah Data Terkecil ({least_common_value}): {least_common_count}")

        

  
    
    
elif option == 'EDA':
    st.write("""## EDA""") #menampilkan judul halaman dataframe

    df2 = pd.read_excel("USA_cars_datasets.xlsx", usecols='B,E,F,G')

    # Menampilkan statistik deskriptif
    st.subheader('Statistik Deskriptif')
    st.write(df2.describe())

    st.set_option('deprecation.showPyplotGlobalUse', False)

   

 

st.sidebar.info("Dikoding oleh [Alla](https://www.instagram.com/13alla_amala14/) & [Ramdani](https://www.instagram.com/rmdunn_35/) Setulus Hati")
    
    