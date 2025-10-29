import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Housing Data Analysis by Jue Gong", layout="wide")

st.title("房屋数据可视化分析")

df=pd.read_csv('housing.csv')


if df is not None:
    st.sidebar.header("数据筛选")
    
    ocean_proximity = df['ocean_proximity'].unique()
    selected_proximity = st.sidebar.multiselect(
        "选择沿海距离",
        options=ocean_proximity,
        default=ocean_proximity
    )
    
    price_min, price_max = st.sidebar.slider(
        "房屋价格范围",
        min_value=float(df['median_house_value'].min()),
        max_value=float(df['median_house_value'].max()),
        value=(float(df['median_house_value'].min()), float(df['median_house_value'].max()))
    )
    
    filtered_df = df[
        (df['ocean_proximity'].isin(selected_proximity)) &
        (df['median_house_value'] >= price_min) &
        (df['median_house_value'] <= price_max)
    ]
    
    st.subheader("数据预览")
    st.dataframe(filtered_df.head(10))
    
    st.subheader("数据统计摘要")
    st.write(filtered_df.describe())
    
    st.subheader("房屋价格分布")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(filtered_df['median_house_value'], bins=30, alpha=0.7)
    ax.set_xlabel("房屋中位数价格")
    ax.set_ylabel("数量")
    ax.set_title("房屋价格分布直方图")
    st.pyplot(fig)
    
    st.subheader("收入与房价关系")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(filtered_df['median_income'], filtered_df['median_house_value'], alpha=0.5)
    ax.set_xlabel("中位数收入")
    ax.set_ylabel("房屋中位数价格")
    ax.set_title("收入与房价关系散点图")
    st.pyplot(fig)
    
    st.subheader("地理位置分布")
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        filtered_df['longitude'], 
        filtered_df['latitude'], 
        c=filtered_df['median_house_value'], 
        alpha=0.4, 
        s=filtered_df['population']/100,
        cmap='viridis'
    )
    plt.colorbar(scatter, ax=ax, label='房屋中位数价格')
    ax.set_xlabel("经度")
    ax.set_ylabel("纬度")
    ax.set_title("地理位置与房价分布")
    st.pyplot(fig)



