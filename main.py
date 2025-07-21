
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="HealthKart Influencer Dashboard", layout="wide")
st.title("📊 HealthKart Influencer Campaign Dashboard")

# Load data
influencers = pd.read_csv("data/influencers.csv")
posts = pd.read_csv("data/posts.csv")
tracking = pd.read_csv("data/tracking_data.csv")
payouts = pd.read_csv("data/payouts.csv")

# Merge for ROAS calculations
merged = pd.merge(tracking, payouts, on="influencer_id")
merged["ROAS"] = merged["revenue"] / merged["total_payout"]
merged["ROAS"] = merged["ROAS"].replace([float('inf'), -float('inf')], 0).fillna(0)

# Tagging ROAS
merged["ROAS_Tag"] = pd.qcut(merged["ROAS"], q=3, labels=["Low", "Medium", "High"])

# Filters
platform_filter = st.sidebar.multiselect("Platform", influencers["platform"].unique(), default=influencers["platform"].unique())
category_filter = st.sidebar.multiselect("Category", influencers["category"].unique(), default=influencers["category"].unique())

filtered_influencers = influencers[
    (influencers["platform"].isin(platform_filter)) & 
    (influencers["category"].isin(category_filter))
]

filtered_merged = merged[merged["influencer_id"].isin(filtered_influencers["ID"])]
filtered_merged = pd.merge(filtered_merged, filtered_influencers, left_on="influencer_id", right_on="ID")

# Show influencer table
st.subheader("🎯 Influencer Overview")
st.dataframe(filtered_influencers)

# ROAS Chart
st.subheader("📈 ROAS by Influencer")
roas_chart = alt.Chart(filtered_merged).mark_bar().encode(
    x=alt.X('name:N', sort='-y', title='Influencer'),
    y=alt.Y('ROAS:Q', title='ROAS'),
    color='ROAS_Tag:N',
    tooltip=['name', 'revenue', 'total_payout', 'ROAS', 'ROAS_Tag']
).properties(width=800)

st.altair_chart(roas_chart, use_container_width=True)

# CSV Export
st.subheader("⬇️ Download Filtered Data")
csv = filtered_merged.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_campaign_data.csv",
    mime="text/csv"
)

# Show data tables
st.subheader("📌 Posts Data")
st.dataframe(posts[posts["influencer_id"].isin(filtered_influencers["ID"])])
st.subheader("🧾 Tracking Data")
st.dataframe(tracking[tracking["influencer_id"].isin(filtered_influencers["ID"])])
st.subheader("💰 Payouts")
st.dataframe(payouts[payouts["influencer_id"].isin(filtered_influencers["ID"])])
