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

day_clean_df = pd.read_csv(r"C:\Users\LENOVO\Downloads\submission\submission\dashboard\main_data.csv")
hour_df = pd.read_csv(r"C:\Users\LENOVO\Downloads\Bike-sharing-dataset\hour.csv")

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
    return df.replace({"yr": {0: 2010, 1: 2011}})

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
    Berdasarkan grafik tren pola total penyewaan sepeda setiap tahun, terlihat bahwa puncak penyewaan sepeda terjadi pada bulan 6 dan 7, 
    yang kemungkinan besar mencerminkan bulan-bulan musim panas dengan kondisi cuaca yang ideal untuk bersepeda. Setelah mencapai puncaknya, 
    grafik menunjukkan penurunan signifikan dalam jumlah penyewaan sepeda, dimulai setelah bulan 7, yang dapat diinterpretasikan sebagai transisi dari musim panas 
    ke musim gugur dan kemudian musim dingin, di mana cuaca kurang mendukung untuk kegiatan bersepeda. Selain itu, ketika membandingkan data antara tahun 2010 dan 2011, 
    terdapat peningkatan jumlah penyewaan sepeda di setiap bulan pada tahun 2011, menandakan bahwa layanan bike sharing semakin populer dan mengalami 
    pertumbuhan dari tahun ke tahun.
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
    Berdasarkan grafik pertama yang menunjukkan tren penyewaan sepeda berdasarkan jam, 
    kita dapat menyimpulkan bahwa terdapat dua puncak utama penyewaan sepeda setiap hari, 
    yang terjadi sekitar jam 8 pagi dan jam 5 sore. Ini mungkin menunjukkan pola perjalanan 
    penduduk setempat yang menggunakan sepeda untuk berangkat dan pulang dari tempat kerja atau sekolah. 
    Selain itu, terlihat bahwa pada tahun 2011, jumlah penyewaan sepeda secara keseluruhan lebih tinggi dibandingkan 
    dengan tahun 2010 pada hampir setiap jam, menunjukkan peningkatan popularitas layanan bike sharing dari tahun ke tahun.
    """
)
#pola terjadi pada trend penyewaan sepeda terhadap perbedaan musim
season_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
season_df['season'] = season_df['season'].map(season_mapping)
st.subheader("Trend penyewaan sepeda berdasarkan Musim :point_down:")
fig, ax = plt.subplots()
sns.barplot(data=season_df, x="season", y="cnt", hue="yr", palette="bright")
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang disewakan berdasarkan Musim")
plt.legend(title="Tahun", loc="upper right")  
for container in ax.containers:
    ax.bar_label(container, fontsize=8, color='white', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)

#Menambahkan keterangan
with st.expander('**Bagaimana Kesimpulannya?**'):
   st.markdown(
    """
    Grafik ketiga menunjukkan tren penyewaan sepeda setiap bulan selama setahun dan mengungkapkan bahwa 
    penyewaan sepeda meningkat secara signifikan selama bulan-bulan hangat, mencapai puncaknya di bulan 
    Juni dan Juli, dan menurun menuju bulan-bulan yang lebih dingin. Juga, terdapat peningkatan jumlah 
    penyewaan sepeda secara keseluruhan dari tahun 2010 ke 2011, yang menunjukkan pertumbuhan popularitas 
    layanan bike sharing dari tahun ke tahun
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
   Pada grafik ini menunjukkan bahwa jumlah total penyewaan sepeda lebih tinggi pada hari kerja dibandingkan dengan hari libur, 
   menunjukkan bahwa sepeda banyak digunakan untuk keperluan komuter sehari-hari seperti pergi ke tempat kerja atau sekolah.
    """
)
