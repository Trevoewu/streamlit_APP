import streamlit as st
import pandas as pd
import numpy as np
st.title('深圳市出租轨迹分析平台')
DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
# 数据源：
DATA_URL = ('SC_GPS.csv')
COLUMN = ['VehicleNum', 'date/time', 'lon', 'lat',
          'Direction', 'Speed', 'OpenStatus', 'isEmpty']


@st.cache_data
# 放入缓存
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.columns = COLUMN
    # def lowercase(x): return str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('数据载入中...')
FILE_NAME = st.selectbox(
    '文件选择',
    ['czc_gps_date_20140613.csv', 'czc_gps_date_20140614.csv']
)
# st.c
# Load 10,000 rows of data into the dataframe.
NROWS = st.slider('数据条数', 0, 600000, 100000)
data = load_data(NROWS)

# Notify the reader that the data was successfully loaded.
data_load_state.text("载入完成! (using st.cache_data)")
st.subheader('原始数据')
if (st.checkbox(f'显示原始数据(共{NROWS}条数据)')):
    st.write(data)
st.subheader('出租车次数的时间分布')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)
hour_to_filter = 17
# min: 0h, max: 23h, default: 17h
hour_to_filter = st.slider('小时', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'{hour_to_filter}:00点时出租车分布地图')
st.map(filtered_data)
