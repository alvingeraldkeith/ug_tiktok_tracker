import streamlit as st
from apify_client import ApifyClient
from datetime import datetime
import pandas as pd

# 1. SETUP
# We use st.secrets for safety. We will set this in the Streamlit dashboard later.
APIFY_TOKEN = st.secrets["apify_api_JNa9KbXtWZyveQqJS1U3h5VmCXKT913UyPna"]
target_accounts = ["cluttermycash", "getitcheaperwithsylvia", "micasa_ug"]

st.set_page_config(page_title="UG TikTok Tracker", layout="centered")
st.title("🇺🇬 UG Niche Tracker")

if st.button('🔄 Refresh Data'):
    client = ApifyClient(APIFY_TOKEN)
    
    with st.spinner('Checking Kampala trends...'):
        # Using the Scraptik TikTok API (Reliable in 2026)
        run_input = {"profiles": target_accounts, "resultsPerPage": 3}
        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        
        data_list = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            timestamp = item.get('createTime')
            # Adjust to EAT (UTC + 3)
            dt_eat = datetime.fromtimestamp(timestamp + 10800) 
            
            data_list.append({
                "Account": item.get('authorMeta', {}).get('name'),
                "Time (EAT)": dt_eat.strftime('%H:%M (%a)'),
                "Likes": item.get('diggCount'),
                "Views": item.get('playCount')
            })

        df = pd.DataFrame(data_list)
        st.write("### Latest Activity")
        st.dataframe(df, use_container_width=True)
        st.success(f"Updated at {datetime.now().strftime('%H:%M:%S')}")
else:
    st.info("Tap 'Refresh' to see when the big accounts last posted.")
