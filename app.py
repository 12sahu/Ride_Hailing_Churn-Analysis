import streamlit as st
import pandas as pd

st.title("🚕 Ride-Hailing Churn Analysis Dashboard")

# -----------------------------
# LOAD DATA (YOUR PATHS)
# -----------------------------
@st.cache_data
def load_data():
    df_uber = pd.read_csv(r"D:\Ride Hailing Churn Analysis\uber_reviews_without_reviewid.csv")
    df_ola = pd.read_csv(r"D:\Ride Hailing Churn Analysis\Bengaluru_Ola_Booking_Data.csv")
    df_rapido = pd.read_csv(r"D:\Ride Hailing Churn Analysis\Subride - Subjectivity Detection in Ride-Hailing App Reviews.csv")
    df_subride_annotator = pd.read_csv(r"D:\Ride Hailing Churn Analysis\Subride - Subjectivity Detection in Ride-Hailing App Reviews Per Annotator.csv")

    return df_uber, df_ola, df_rapido, df_subride_annotator

df_uber, df_ola, df_rapido, df_subride_annotator = load_data()

# -----------------------------
# SHOW DATA
# -----------------------------
st.subheader("📊 Uber Data")
st.write(df_uber.head())

st.subheader("📊 Ola Data")
st.write(df_ola.head())

st.subheader("📊 SubRide Data")
st.write(df_rapido.head())

st.subheader("📊 Annotator Data")
st.write(df_subride_annotator.head())
# -----------------------------
# CLEANING FUNCTION
# -----------------------------
def clean_data(df, text_col, rating_col):
    df = df.dropna(subset=[text_col, rating_col])
    df[text_col] = df[text_col].astype(str).str.lower().str.strip()
    return df

# Apply cleaning
df_uber_clean = clean_data(df_uber, 'content', 'score')
df_rapido_clean = clean_data(df_rapido, 'translated_review', 'score')
df_annotator_clean = clean_data(df_subride_annotator, 'translated_review', 'score')

# Add platform column
df_uber_clean['platform'] = 'Uber'
df_rapido_clean['platform'] = 'SubRide'
df_annotator_clean['platform'] = 'Annotator'

# Merge review-based datasets
df_reviews = pd.concat([
    df_uber_clean[['content', 'score', 'platform']].rename(columns={'content': 'review'}),
    df_rapido_clean[['translated_review', 'score', 'platform']].rename(columns={'translated_review': 'review'}),
    df_annotator_clean[['translated_review', 'score', 'platform']].rename(columns={'translated_review': 'review'})
])

st.subheader("📊 Combined Review Data")
st.write(df_reviews.head())
# -----------------------------
# CHURN LABEL
# -----------------------------
def create_churn_label(rating):
    return 1 if rating <= 2 else 0

df_reviews['churn'] = df_reviews['score'].apply(create_churn_label)

st.subheader("⚠️ Churn Distribution")

import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
sns.countplot(x='churn', data=df_reviews, ax=ax)
st.pyplot(fig)