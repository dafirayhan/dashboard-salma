import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

with st.sidebar:
    st.subheader('Hi! Selamat Datang di Proyek Analisa Bike Sharing :superhero:')


# Set the background to a light gray color
plt.rcParams['figure.facecolor'] = 'lightgray'
plt.rcParams['axes.facecolor'] = 'lightgray'

# Set the text color to a darker shade for better contrast
plt.rcParams['text.color'] = 'black'
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'

st.header('Dashboard Study Case Bike Sharing :man-biking:')

# Untuk mempermudah maka menyiapkan Halper Function

def create_casual_register_df(df):
    casual_year_df = df.groupby("yr")["casual"].sum().reset_index()
    casual_year_df.columns = ["yr", "total_casual"]
    reg_year_df = df.groupby("yr")["registered"].sum().reset_index()
    reg_year_df.columns = ["yr", "total_registered"]  
    casual_register_df = casual_year_df.merge(reg_year_df, on="yr")
    return casual_register_df

def create_monthly_df(df):
    monthly_df = df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return monthly_df

def create_hourly_df(df):
    hourly_df = df.groupby(by=["hr","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return hourly_df

def create_byholiday_df(df):
    holiday_df = df.groupby(by=["holiday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return holiday_df

def create_byworkingday_df(df):
    workingday_df = df.groupby(by=["workingday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return workingday_df

def create_byseason_df(df):
    season_df = df.groupby(by=["season","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return season_df

def create_byweather_df(df):
    weather_df = df.groupby(by=["weathersit","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return weather_df

# Membuat Load Cleaned Data

day_clean_df = pd.read_csv("main_data.csv")
hour_df = pd.read_csv("hour.csv")

# Membuat Load Filter Data

day_clean_df["dteday"] = pd.to_datetime(day_clean_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
min_date = day_clean_df["dteday"].min()
max_date = day_clean_df["dteday"].max()

with st.sidebar:
    # Membuat Logo pada Dashboard
    st.image("sepeda_foto.png")

    # Opsi untuk mengganti rentang waktu
    start_date, end_date = st.date_input(
        label='Analysis Time:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_clean_df[(day_clean_df["dteday"] >= str(start_date)) & 
                       (day_clean_df["dteday"] <= str(end_date))]

second_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]

# Fungsi helper untuk mengganti nilai tahun
def replace_year_values(df):
    return df.replace({"yr": {0: 0, 1: 1}})

# Mengganti nilai tahun pada semua DataFrame
casual_register_df = replace_year_values(create_casual_register_df(main_df))
monthly_df = replace_year_values(create_monthly_df(main_df))
hourly_df = replace_year_values(create_hourly_df(second_df))
holiday_df = replace_year_values(create_byholiday_df(main_df))
workingday_df = replace_year_values(create_byworkingday_df(main_df))
season_df = replace_year_values(create_byseason_df(main_df))
weather_df = replace_year_values(create_byweather_df(main_df))

#Membuka trend waktu penyewaan sepeda dari perbandingan Jam, Hari dan Tahun?

# pola yang terjadi pada jumlah total Bike Sharing 
st.subheader("Trend Pola Total Penyewaan Sepeda Setiap Tahun :point_down:")
fig, ax = plt.subplots()
sns.lineplot(data=monthly_df, x="mnth", y="cnt", hue="yr", palette="bright", marker="o")
plt.xlabel("Urutan Bulan")
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang disewakan")
plt.legend(title="Tahun", loc="upper right")  
plt.xticks(ticks=monthly_df["mnth"], labels=monthly_df["mnth"])
plt.tight_layout()
st.pyplot(fig)

#Menambahkan keterangan
with st.expander('**Bagaimana Kesimpulannya?**'):
   st.markdown(
    """
    Grafik ini menunjukkan tren penyewaan sepeda yang memiliki pola musiman, dengan peningkatan dari Januari hingga mencapai puncaknya di bulan Mei atau Juni. Peningkatan ini mungkin dipengaruhi oleh cuaca yang lebih baik dan panjangnya waktu siang hari selama musim semi dan awal musim panas, yang mendorong lebih banyak orang untuk bersepeda. Setelah mencapai puncaknya, jumlah penyewaan secara bertahap menurun hingga Desember, sebuah pola yang konsisten pada kedua tahun. Penurunan ini kemungkinan disebabkan oleh peralihan musim ke musim gugur dan musim dingin, di mana kondisi cuaca menjadi kurang mendukung untuk aktivitas luar ruangan. Selain itu, pada tahun kedua, jumlah penyewaan sepeda secara keseluruhan lebih tinggi dibandingkan tahun pertama, dengan puncak penyewaan mencapai lebih dari 200.000 pada pertengahan tahun. Hal ini menunjukkan peningkatan minat dan kebiasaan masyarakat dalam menggunakan sepeda, mungkin dipengaruhi oleh kesadaran akan kesehatan, kebijakan transportasi, atau promosi dari layanan penyewaan sepeda. Penurunan drastis pada bulan Oktober hingga Desember juga dapat dikaitkan dengan cuaca yang kurang kondusif seperti hujan atau suhu yang lebih rendah, yang mengurangi aktivitas bersepeda.
    """
)

# pola yang terjadi pada jumlah total penyewaan sepeda berdasarkan Jam
st.subheader("Trend Penyewaan Sepeda Berdasarkan Jam :point_down:")
fig, ax = plt.subplots()
sns.lineplot(data=hourly_df, x="hr", y="cnt", hue="yr", palette="bright", marker="o")
plt.xlabel("Urutan Jam")
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang disewakan berdasarkan Jam dan tahun")
plt.legend(title="Tahun", loc="upper right")  
plt.xticks(ticks=hourly_df["hr"], labels=hourly_df["hr"])
plt.tight_layout()
st.pyplot(fig)

#Menambahkan keterangan
with st.expander('**Bagaimana Kesimpulannya?**'):
   st.markdown(
    """
    Grafik ini menggambarkan pola penyewaan sepeda dalam dua tahun yang berbeda, menunjukkan bagaimana aktivitas bersepeda memiliki ritme tertentu sepanjang hari. Terlihat jelas bahwa puncak penyewaan terjadi di pagi hari sekitar pukul 7-8 dan kembali meningkat di sore hari sekitar pukul 17. Hal ini seolah menggambarkan rutinitas harian masyarakat yang mungkin menggunakan sepeda sebagai sarana transportasi saat berangkat dan pulang kerja atau sekolah.

Menariknya, di tahun kedua (tahun '1' pada grafik), jumlah penyewaan sepeda meningkat secara signifikan dibandingkan tahun sebelumnya. Ini mungkin menunjukkan adanya peningkatan minat terhadap transportasi yang lebih ramah lingkungan atau bisa juga menjadi refleksi dari perubahan gaya hidup masyarakat. Di sisi lain, penyewaan sepeda paling sepi terjadi pada malam hingga dini hari (sekitar pukul 2-5 pagi), yang wajar karena kebanyakan orang sedang beristirahat.
    """
)

   
#Pola Trend Penyewa sepeda saat Hari Kerja dan Libur Kerja
st.subheader("Trend penyewaan sepeda Berdasarkan Hari Libur dan Hari Kerja :point_down:")
col_holiday, col_workingday = st.columns([1, 1])
with col_holiday:
    fig, ax = plt.subplots()
    sns.barplot(data=holiday_df, x="holiday", y="cnt", hue="yr", palette="bright")
    plt.ylabel("Jumlah")
    plt.title("Jumlah total sepeda yang disewakan berdasarkan hari Libur")
    plt.legend(title="Tahun", loc="upper right")  
    for container in ax.containers:
        ax.bar_label(container, fontsize=8, color='white', weight='bold', label_type='edge')
    plt.tight_layout()
    st.pyplot(fig)
with col_workingday:
    fig, ax = plt.subplots()
    sns.barplot(data=workingday_df, x="workingday", y="cnt", hue="yr", palette="bright")
    plt.ylabel("Jumlah")
    plt.title("Jumlah total sepeda yang disewakan berdasarkan hari Kerja")
    plt.legend(title="Tahun", loc="upper right")  
    for container in ax.containers:
        ax.bar_label(container, fontsize=8, color='white', weight='bold', label_type='edge')
    plt.tight_layout()
    st.pyplot(fig)

#Menambahkan keterangan
with st.expander('**Bagaimana Kesimpulannya?**'):
   st.markdown(
    """
   Grafik ini menunjukkan bahwa jumlah penyewaan sepeda lebih tinggi selama hari kerja (weekdays) dibandingkan dengan akhir pekan (weekends) pada kedua tahun yang dianalisis. Hal ini mengindikasikan bahwa sepeda lebih sering digunakan sebagai sarana transportasi harian, seperti untuk keperluan komuter atau sekolah selama hari kerja. Selain itu, terdapat peningkatan jumlah penyewaan sepeda dari tahun pertama ke tahun kedua, baik pada weekdays maupun weekends. Peningkatan ini lebih signifikan pada hari kerja, yang mungkin mencerminkan perubahan gaya hidup atau kebijakan yang mendorong penggunaan sepeda, seperti kesadaran terhadap kesehatan atau dukungan kebijakan transportasi. Meskipun terjadi peningkatan aktivitas penyewaan pada akhir pekan di tahun kedua, jumlahnya tetap lebih rendah dibandingkan hari kerja, menunjukkan bahwa sepeda lebih sering digunakan dalam rutinitas sehari-hari. Puncak jumlah penyewaan tertinggi terjadi pada hari kerja di tahun kedua, dengan lebih dari 1,4 juta penyewaan, memperkuat tren positif dalam penggunaan sepeda sebagai moda transportasi sehari-hari.
    """
)
