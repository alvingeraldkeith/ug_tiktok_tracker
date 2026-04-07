import streamlit as st
from apify_client import ApifyClient
from datetime import datetime
import pandas as pd

# --- 1. FILL IN YOUR DATA HERE ---
APIFY_TOKEN = "YOUR_ACTUAL_TOKEN_FROM_APIFY"
target_accounts = ["cluttermycash", "getitcheaperwithsylvia", "micasa_ug"]

# --- 2. THE DASHBOARD ---
st.set_page_config(page_title="UG TikTok Tracker", layout="centered")
st.title("🇺🇬 UG Shopping Niche Tracker")

if st.button('🔄 Refresh Data'):
    client = ApifyClient(APIFY_TOKEN)
    
    with st.spinner('Scraping Kampala trends...'):
        # Using the TikTok Scraper actor
        run_input = {"profiles": target_accounts, "resultsPerPage": 3}
        run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        
        data_list = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            timestamp = item.get('createTime')
            # Adjusting for EAT (UTC + 3 hours)
            dt_eat = datetime.fromtimestamp(timestamp + 10800) 
            
            data_list.append({
                "Account": item.get('authorMeta', {}).get('name'),
                "Post Time (EAT)": dt_eat.strftime('%H:%M (%a)'),
                "Likes": item.get('diggCount'),
                "Views": item.get('playCount')
            })

        df = pd.DataFrame(data_list)
        st.write("### Latest Posts")
        st.table(df) # Table is easier to read on a phone
        st.success(f"Last updated at {datetime.now().strftime('%H:%M:%S')}")
