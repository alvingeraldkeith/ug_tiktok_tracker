import streamlit as st
from apify_client import ApifyClient
from datetime import datetime
import pandas as pd

# 1. SETUP
# Ensure "APIFY_TOKEN" is set in your Streamlit Cloud Secrets
APIFY_TOKEN = st.secrets["APIFY_TOKEN"]
target_accounts = ["cluttermycash", "getitcheaperwithsylvia", "micasa_ug"]

st.set_page_config(page_title="UG TikTok Tracker", layout="centered")
st.title("Declutter accounts  Tracker uganda  ")

if st.button('🔄 Refresh Data'):
    client = ApifyClient(APIFY_TOKEN)
    
    with st.spinner('Checking Kampala trends...'):
        # Using the TikTok Scraper actor
        run_input = {"profiles": target_accounts, "resultsPerPage": 3}
        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        
        data_list = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            timestamp = item.get('createTime')
            
            # --- THE SAFETY CHECK ---
            if timestamp is not None:
                # Adjust to EAT (UTC + 3 hours)
                dt_eat = datetime.fromtimestamp(timestamp + 10800) 
                
                data_list.append({
                    "Account": item.get('authorMeta', {}).get('name'),
                    "Time (EAT)": dt_eat.strftime('%H:%M (%a)'),
                    "Likes": item.get('diggCount'),
                    "Views": item.get('playCount')
                })

        # 2. DISPLAY DATA
        if data_list:
            df = pd.DataFrame(data_list)
            st.write("### Latest Activity")
            st.dataframe(df, use_container_width=True)
            st.success(f"Updated at {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.warning("No recent posts found. Try refreshing again in a few minutes.")
else:
    st.info("Tap 'Refresh' to see when the big accounts last posted.")
