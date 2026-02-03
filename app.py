"""
app.py - نسخه آپدیت شده با SeleniumBase
"""

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tldextract
import time
import json

from google_module import GoogleSerper
from hybrid_backlink_v2 import HybridBacklinkAnalyzerV2


# =====================================
# اتصال به گوگل شیت
# =====================================
def connect_to_sheet(sheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1


# =====================================
# Flatten کامل خروجی API (تفکیک ستون‌ها)
# =====================================
def flatten_link(link: dict):
    flat = {}
    for k, v in link.items():
        if isinstance(v, (dict, list)):
            flat[k] = json.dumps(v, ensure_ascii=False)
        else:
            flat[k] = v
    return flat


# =====================================
# برنامه اصلی
# =====================================
def main():
    print("="*70)
    print("🔥 SEO BACKLINK ANALYZER - V2")
    print("="*70)
    print("\nویژگی‌های جدید:")
    print("  ✅ Ahrefs scraping با SeleniumBase (رایگان، 80-90% موفقیت)")
    print("  ✅ SE Ranking API (پولی، 100% موفقیت)")
    print("  ✅ Fallback هوشمند")
    print("  ✅ ذخیره در Google Sheets")
    print("="*70 + "\n")
    
    # دریافت ورودی‌ها
    keyword = input("🔑 کلمه کلیدی را وارد کنید: ")
    sheet_name = input("📊 نام Google Sheet [SEO_Report]: ").strip() or "SEO_Report"
    
    # انتخاب منبع بک‌لینک
    print("\n🔗 منبع بک‌لینک:")
    print("  1. Ahrefs (SeleniumBase) - رایگان")
    print("  2. SE Ranking - API")
    print("  3. هر دو (پیشنهادی)")
    
    choice = input("\nانتخاب [3]: ").strip() or "3"
    
    use_ahrefs = choice in ["1", "3"]
    use_se_ranking = choice in ["2", "3"]
    prefer_ahrefs = choice == "1"
    
    # تنظیمات Ahrefs
    headless = False
    if use_ahrefs:
        headless_input = input("🖥️  Ahrefs در حالت Headless؟ (y/n) [n]: ").strip().lower()
        headless = headless_input == 'y'
    
    # ابزارها
    google_tool = GoogleSerper()
    
    backlink_tool = HybridBacklinkAnalyzerV2(
        prefer_ahrefs=prefer_ahrefs,
        use_seleniumbase=use_ahrefs,
        headless=headless
    )
    
    print(f"\n{'='*70}")
    print(f"🚀 شروع جستجو در گوگل برای: {keyword}")
    print("="*70 + "\n")
    
    serp_results = google_tool.get_competitors(keyword)
    
    if not serp_results:
        print("❌ هیچ نتیجه‌ای از گوگل دریافت نشد.")
        return
    
    final_rows = []
    all_headers = set()
    
    print(f"✅ {len(serp_results)} سایت رقیب پیدا شد.\n")
    
    # نمایش رقبا
    print("📋 لیست رقبا:")
    for i, item in enumerate(serp_results, 1):
        domain = tldextract.extract(item.get("link", "")).registered_domain
        print(f"  {i}. {domain} (رتبه {item.get('position', 'N/A')})")
    
    print(f"\n{'='*70}")
    print("🔗 شروع تحلیل بک‌لینک‌ها...")
    print("="*70 + "\n")
    
    for idx, item in enumerate(serp_results, 1):
        url = item.get("link")
        if not url:
            continue
        
        domain = tldextract.extract(url).registered_domain
        position = item.get("position")
        
        print(f"\n[{idx}/{len(serp_results)}] 📍 {domain}")
        print("-" * 60)
        
        # دریافت بک‌لینک‌ها
        links = backlink_tool.fetch_links(
            domain,
            limit=20,  # می‌تونی تغییر بدی
            fallback=True,
            ahrefs_wait_time=10
        )
        
        if not links:
            print(f"⚠️ هیچ بک‌لینکی برای {domain} پیدا نشد")
            row = {
                "Keyword": keyword,
                "Google Pos": position,
                "Competitor": domain,
                "status": "No backlinks found"
            }
            final_rows.append(row)
            all_headers.update(row.keys())
            continue
        
        print(f"✅ {len(links)} بک‌لینک دریافت شد\n")
        
        # اضافه کردن به نتایج
        for link in links:
            flat_link = flatten_link(link)
            
            row = {
                "Keyword": keyword,
                "Google Pos": position,
                "Competitor": domain,
                **flat_link
            }
            
            final_rows.append(row)
            all_headers.update(row.keys())
        
        # تاخیر بین درخواست‌ها
        if idx < len(serp_results):
            wait = 5
            print(f"⏳ صبر {wait} ثانیه تا رقیب بعدی...\n")
            time.sleep(wait)
    
    if not final_rows:
        print("\n❌ دیتایی برای ذخیره وجود ندارد.")
        return
    
    headers = list(all_headers)
    
    # =====================================
    # ذخیره در گوگل شیت
    # =====================================
    print(f"\n{'='*70}")
    print("💾 در حال ارسال داده‌ها به گوگل شیت...")
    print("="*70)
    
    try:
        sheet = connect_to_sheet(sheet_name)
        existing_data = sheet.get_all_values()
        
        # اگر شیت خالی است، هدرها را بساز
        if not existing_data:
            sheet.append_row(headers)
            print("✅ هدرها اضافه شد")
        
        rows_to_append = [
            [row.get(h, "N/A") for h in headers]
            for row in final_rows
        ]
        
        sheet.append_rows(rows_to_append)
        print(f"✅ {len(rows_to_append)} ردیف به شیت اضافه شد")
        print("🎯 شیت با موفقیت آپدیت شد!")
        
    except Exception as e:
        print(f"❌ خطای گوگل شیت: {e}")
        print("\n💾 ذخیره در فایل CSV به عنوان backup...")
        
        df = pd.DataFrame(final_rows)
        filename = f"backup_results_{keyword.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ فایل {filename} ذخیره شد.")
    
    # خلاصه نتایج
    print(f"\n{'='*70}")
    print("📊 خلاصه نتایج:")
    print("="*70)
    print(f"  🔑 کلمه کلیدی: {keyword}")
    print(f"  🏆 تعداد رقبا: {len(serp_results)}")
    print(f"  🔗 کل بک‌لینک‌ها: {len(final_rows)}")
    print(f"  📊 Google Sheet: {sheet_name}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
