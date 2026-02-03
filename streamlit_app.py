import streamlit as st
import pandas as pd
import gspread
import tldextract
import time
import json
import os
from datetime import datetime
import plotly.express as px

from google_module import GoogleSerper
from hybrid_backlink_v2 import HybridBacklinkAnalyzerV2

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="SEO Backlink Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# Custom CSS
# =====================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================
# Google Sheets Connection
# =====================================
@st.cache_resource
def connect_to_sheet(sheet_name):
    """اتصال به Google Sheet"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    try:
        # Hugging Face Spaces
        if os.environ.get("GCP_SERVICE_ACCOUNT"):
            from google.oauth2.service_account import Credentials
            creds_dict = json.loads(os.environ.get("GCP_SERVICE_ACCOUNT"))
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            client = gspread.authorize(creds)
        # Streamlit Cloud
        elif hasattr(st, 'secrets') and "gcp_service_account" in st.secrets:
            from google.oauth2.service_account import Credentials
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            client = gspread.authorize(creds)
        # Local
        elif os.path.exists("credentials.json"):
            from oauth2client.service_account import ServiceAccountCredentials
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            client = gspread.authorize(creds)
        else:
            st.error("❌ Google Sheets credential یافت نشد")
            return None
        
        return client.open(sheet_name)
    except Exception as e:
        st.error(f"❌ خطا: {e}")
        return None

def flatten_link(link: dict):
    flat = {}
    for k, v in link.items():
        if isinstance(v, (dict, list)):
            flat[k] = json.dumps(v, ensure_ascii=False)
        else:
            flat[k] = v
    return flat

def save_to_sheets_v2(spreadsheet, keyword, serp_results, all_backlinks_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_keyword = keyword.replace(" ", "_").replace("/", "_")[:30]
    sheet_name = f"{safe_keyword}_{datetime.now().strftime('%m%d')}"
    
    try:
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except:
            worksheet = spreadsheet.add_worksheet(sheet_name, 1000, 30)
        
        existing_data = worksheet.get_all_values()
        
        if not existing_data:
            worksheet.append_row(["اطلاعات جستجو"])
            worksheet.append_row(["Timestamp", "Keyword", "Total Competitors", "Total Backlinks"])
            total_backlinks = sum(len(b['backlinks']) for b in all_backlinks_data)
            worksheet.append_row([timestamp, keyword, len(all_backlinks_data), total_backlinks])
            worksheet.append_row([])
            worksheet.append_row(["نتایج Google"])
            worksheet.append_row(["Position", "Domain", "URL", "Title", "Backlinks"])
        
        for item in serp_results:
            url = item.get("link", "N/A")
            domain = tldextract.extract(url).registered_domain if url != "N/A" else "N/A"
            backlink_count = next((len(b['backlinks']) for b in all_backlinks_data if b['domain'] == domain), 0)
            worksheet.append_row([item.get("position", "N/A"), domain, url, item.get("title", "N/A"), backlink_count])
        
        worksheet.append_row([])
        worksheet.append_row(["جزئیات Backlinks"])
        worksheet.append_row(["Competitor", "Position", "URL From", "URL To", "Anchor", "Nofollow", "DR", "Source", "First Seen"])
        
        backlink_rows = []
        for comp in all_backlinks_data:
            for link in comp['backlinks']:
                row = [
                    comp['domain'], comp['position'], link.get("url_from", "N/A"),
                    link.get("url_to", "N/A"), link.get("anchor", "N/A")[:200],
                    "Yes" if link.get("nofollow") == 1 else "No",
                    link.get("domain_inlink_rank", "N/A"), link.get("source", "N/A"),
                    link.get("first_seen", "N/A")
                ]
                backlink_rows.append(row)
        
        if backlink_rows:
            worksheet.append_rows(backlink_rows)
        
        return True
    except Exception as e:
        st.error(f"❌ خطا در ذخیره: {e}")
        return False

def main():
    if 'serp_results' not in st.session_state:
        st.session_state.serp_results = None
    if 'selected_indices' not in st.session_state:
        st.session_state.selected_indices = []
    if 'analysis_started' not in st.session_state:
        st.session_state.analysis_started = False
    
    st.markdown('<h1 class="main-header">🔍 SEO Backlink Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("ℹ️ درباره ابزار"):
        st.markdown("""
        ### قابلیت‌ها:
        - 🔍 جستجو در Google
        - 🔗 تحلیل بک‌لینک با Ahrefs (SeleniumBase)
        - 📊 ذخیره در Google Sheets
        - 📈 گراف‌های تحلیلی
        """)
    
    with st.sidebar:
        st.header("⚙️ تنظیمات")
        keyword = st.text_input("🔑 کلمه کلیدی:", placeholder="خرید لپ تاپ")
        sheet_name = st.text_input("📊 Google Sheet:", value="SEO_Report")
        
        st.markdown("---")
        data_source = st.radio("🔗 منبع:", ["Ahrefs (رایگان)", "SE Ranking", "هر دو"], index=0)
        
        if "Ahrefs" in data_source:
            headless_mode = st.checkbox("Headless", value=True)
            ahrefs_wait = st.slider("زمان انتظار", 5, 20, 10)
        else:
            headless_mode = True
            ahrefs_wait = 10
        
        max_backlinks = st.number_input("حداکثر بک‌لینک:", 10, 200, 50, 10)
        search_button = st.button("🚀 شروع", use_container_width=True, type="primary")
    
    if not keyword:
        st.info("👈 کلمه کلیدی وارد کنید")
        return
    
    if search_button:
        st.session_state.serp_results = None
        st.session_state.selected_indices = []
        st.session_state.analysis_started = False
        st.session_state.keyword = keyword
        st.session_state.sheet_name = sheet_name
        st.session_state.data_source = data_source
        st.session_state.headless_mode = headless_mode
        st.session_state.ahrefs_wait = ahrefs_wait
        st.session_state.max_backlinks = max_backlinks
        
        with st.spinner("🔍 جستجو..."):
            google_tool = GoogleSerper()
            serp_results = google_tool.get_competitors(keyword, num_results=10)
        
        if not serp_results:
            st.error("❌ نتیجه‌ای یافت نشد")
            return
        
        st.session_state.serp_results = serp_results
        st.success(f"✅ {len(serp_results)} رقیب یافت شد")
        st.rerun()
    
    if st.session_state.serp_results and not st.session_state.analysis_started:
        serp_results = st.session_state.serp_results
        st.header("📋 رقبا")
        
        competitors_data = []
        for item in serp_results:
            domain = tldextract.extract(item.get("link", "")).registered_domain
            competitors_data.append({
                "رتبه": item.get("position", "N/A"),
                "دامنه": domain,
                "عنوان": item.get("title", "N/A")[:60] + "..."
            })
        
        df = pd.DataFrame(competitors_data)
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            mode = st.radio("انتخاب:", ["همه", "دستی", "5 تا اول"], horizontal=True)
        with col2:
            confirm = st.button("✅ تایید", use_container_width=True)
        
        if mode == "دستی":
            selected = []
            cols = st.columns(5)
            for i, c in enumerate(competitors_data):
                with cols[i % 5]:
                    if st.checkbox(f"#{c['رتبه']} {c['دامنه']}", key=f"c_{i}"):
                        selected.append(i)
            st.session_state.selected_indices = selected
        elif mode == "5 تا اول":
            st.session_state.selected_indices = list(range(min(5, len(serp_results))))
        else:
            st.session_state.selected_indices = list(range(len(serp_results)))
        
        if confirm:
            if not st.session_state.selected_indices:
                st.error("❌ انتخاب کنید!")
                return
            st.session_state.analysis_started = True
            st.rerun()
    
    if st.session_state.analysis_started:
        serp_results = st.session_state.serp_results
        selected_indices = st.session_state.selected_indices
        selected_results = [serp_results[i] for i in selected_indices]
        
        st.success(f"✅ {len(selected_results)} رقیب")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        use_sb = "Ahrefs" in st.session_state.data_source
        prefer_ah = "Ahrefs" in st.session_state.data_source and "هر دو" not in st.session_state.data_source
        
        tool = HybridBacklinkAnalyzerV2(prefer_ahrefs=prefer_ah, use_seleniumbase=use_sb, headless=st.session_state.headless_mode)
        
        st.header("🔗 تحلیل بک‌لینک")
        all_data = []
        total = len(selected_results)
        
        for idx, item in enumerate(selected_results):
            url = item.get("link")
            if not url:
                continue
            
            domain = tldextract.extract(url).registered_domain
            status_text.text(f"🔗 {domain} ({idx+1}/{total})")
            
            links = tool.fetch_links(domain, st.session_state.max_backlinks, True, st.session_state.ahrefs_wait)
            all_data.append({"domain": domain, "position": item.get("position"), "backlinks": links})
            progress_bar.progress(int((idx + 1) / total * 80))
            time.sleep(1)
        
        status_text.text("💾 ذخیره...")
        sheet = connect_to_sheet(st.session_state.sheet_name)
        
        if sheet:
            if save_to_sheets_v2(sheet, st.session_state.keyword, selected_results, all_data):
                progress_bar.progress(100)
                st.balloons()
                st.success("✅ ذخیره شد!")
        
        st.header("📊 نتایج")
        total_bl = sum(len(b['backlinks']) for b in all_data)
        avg_bl = total_bl / len(all_data) if all_data else 0
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("رقبا", len(selected_results))
        c2.metric("کل", total_bl)
        c3.metric("میانگین", f"{avg_bl:.1f}")
        
        with c4:
            if st.button("🔄 جدید"):
                st.session_state.serp_results = None
                st.session_state.selected_indices = []
                st.session_state.analysis_started = False
                st.rerun()
        
        chart_df = pd.DataFrame([{"دامنه": b['domain'], "تعداد": len(b['backlinks'])} for b in all_data])
        fig = px.bar(chart_df, x="دامنه", y="تعداد", title="بک‌لینک‌ها", color="تعداد")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("🔗 جزئیات"):
            for c in all_data:
                if c['backlinks']:
                    st.subheader(f"{c['domain']} (#{c['position']})")
                    st.dataframe(pd.DataFrame([flatten_link(l) for l in c['backlinks'][:10]]))
        
        csv_data = []
        for c in all_data:
            for l in c['backlinks']:
                csv_data.append({"Keyword": st.session_state.keyword, "Competitor": c['domain'], "Position": c['position'], **flatten_link(l)})
        
        if csv_data:
            csv = pd.DataFrame(csv_data).to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 CSV", csv, f"backlinks_{st.session_state.keyword}_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

if __name__ == "__main__":
    main()
