# import requests

# class BacklinkAnalyzer:
#     def __init__(self):
#         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9" # اینجا را تغییر بده
#         self.host = "backlinks-api2.p.rapidapi.com"   # اینجا را تغییر بده

#     def fetch_links(self, domain):
#         url = f"https://{self.host}/get-backlinks" # این Endpoint ممکن است در API شما متفاوت باشد
#         headers = {
#             "X-RapidAPI-Key": self.api_key,
#             "X-RapidAPI-Host": self.host
#         }
#         querystring = {"domain": domain}

#         try:
#             response = requests.get(url, headers=headers, params=querystring)
#             if response.status_code == 200:
#                 data = response.json()
#                 # فرض بر این است که API لیستی از لینک‌ها برمی‌گرداند
#                 return data.get("backlinks", data.get("links", []))
#         except Exception as e:
#             print(f"Error fetching backlinks for {domain}: {e}")
#         return []


# import requests

# class BacklinkAnalyzer:
#     def __init__(self):
#         # self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
#         # self.host = "backlinks-api2.p.rapidapi.com"

#         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
#         self.host = "moz-backlink-checker-analyzer.p.rapidapi.com"

#     def fetch_links(self, domain):
#         url = f"https://{self.host}/get-backlinks"
#         headers = {
#             "X-RapidAPI-Key": self.api_key,
#             "X-RapidAPI-Host": self.host
#         }
#         querystring = {"domain": domain}

#         try:
#             response = requests.get(url, headers=headers, params=querystring, timeout=15)
#             if response.status_code == 200:
#                 data = response.json()
                
#                 # --- بخش کالبدشکافی (مهم) ---
#                 print(f"DEBUG raw data for {domain}: {data}") 
#                 # --------------------------

#                 # چک کردن تمام نام‌های احتمالی که API ممکن است استفاده کند
#                 links = data.get("backlinks") or data.get("links") or data.get("data") or data.get("result")
                
#                 if isinstance(links, list):
#                     return links
#                 return []
#             else:
#                 print(f"⚠️ API Error {response.status_code}")
#         except Exception as e:
#             print(f"❌ Connection Error: {e}")
#         return []

# import requests

# class BacklinkAnalyzer:
#     def __init__(self):
#         # این کلید RapidAPI توست
#         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
#         # پیشنهاد: در RapidAPI سرویس "Web Search" یا "SEO Helper" را فعال کن
#         self.host = "seo-api.p.rapidapi.com" 

#     def fetch_links(self, domain):
#         url = f"https://{self.host}/backlinks" # آدرس را بر اساس مستندات API جدیدت چک کن
#         headers = {
#             "X-RapidAPI-Key": self.api_key,
#             "X-RapidAPI-Host": self.host
#         }
#         querystring = {"domain": domain}

#         try:
#             response = requests.get(url, headers=headers, params=querystring, timeout=10)
#             if response.status_code == 200:
#                 data = response.json()
#                 # این بخش را منعطف کردیم تا با هر ساختاری کار کند
#                 return data.get("backlinks", data.get("result", data.get("data", [])))
#             else:
#                 print(f"⚠️ خطای {response.status_code} از سمت API بک‌لینک")
#                 return []
#         except:
#             return []



# =============================================================================
# import requests
# 
# class BacklinkAnalyzer:
#     def __init__(self):
#         
#         self.proxies = {
#             'http': 'socks5h://127.0.0.1:8351',   # socks5h (h برای DNS resolution روی proxy)
#             'https': 'socks5h://127.0.0.1:8351',
#         }
#         
# # =============================================================================
# #         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
# #         self.host = "backlink-checker3.p.rapidapi.com"
# #         self.url = "https://backlink-checker3.p.rapidapi.com/api/compare-competitors"
# #         
# # =============================================================================
# # =============================================================================
#         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
#         self.host = "best-backlink-checker-api.p.rapidapi.com"
#         self.url = "https://best-backlink-checker-api.p.rapidapi.com/excatbacklinks_noneng.php"
#         
#         
#         
# 
# # =============================================================================
# #         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
# #         self.host = "moz-backlink-checker-analyzer.p.rapidapi.com"
# #         self.url = "https://moz-backlink-checker-analyzer.p.rapidapi.com/"
# # 
# # =============================================================================
#     def fetch_links(self, domain):
#         headers = {
#             "Content-Type": "application/json",
#             "x-rapidapi-host": self.host,
#             "x-rapidapi-key": self.api_key
#             
#         }
#         # طبق مستندات شما، دیتا باید به صورت JSON و با متد POST ارسال شود
#         payload = {"domain": domain}
# 
#         try:
#             response = requests.post(self.url, headers=headers, json=payload, timeout=15, proxies=self.proxies)
#             
#             if response.status_code == 200:
#                 data = response.json()
#                 # چاپ برای دیباگ (بسیار مهم: ببینیم خروجی این API چه شکلی است)
#                 print(f"DEBUG raw data for {domain}: {data}")
#                 
#                 # معمولاً Moz دیتایی مثل 'backlinks' یا 'result' برمی‌گرداند
#                 return data.get("backlinks", data.get("result", []))
#             
#             elif response.status_code == 403:
#                 print(f"❌ خطا 403: یا شارژ نداری یا پلن رایگان رو در سایت RapidAPI فعال (Subscribe) نکردی.")
#             else:
#                 print(f"⚠️ خطای {response.status_code}: {response.text}")
#                 
#         except Exception as e:
#             print(f"❌ خطای اتصال: {e}")
#         return []
# =============================================================================
    
"""    
    
import nest_asyncio
nest_asyncio.apply()    
    
import asyncio
import nodriver as uc  # pip install nodriver
import random
import time

class BacklinkAnalyzer:
    def __init__(self):
        self.proxy = None  # اگر proxy داری: "http://user:pass@ip:port"

    async def fetch_ahrefs_backlinks(self, domain):
        links = []
        try:
            # تنظیم browser با proxy اگر باشه
            browser_args = ['--no-sandbox']
            if self.proxy:
                browser_args.append(f'--proxy-server={self.proxy}')

            browser = await uc.start(headless=True, browser_args=browser_args)  # headless=False برای تست
            url = f"https://ahrefs.com/backlink-checker?input={domain}&mode=subdomains"
            page = await browser.get(url)

            # صبر برای رد Cloudflare و لود کامل (۵–۱۵ ثانیه بسته به نت)
            await asyncio.sleep(8 + random.uniform(2, 5))  # رندم برای جلوگیری از تشخیص

            # چک کن صفحه لود شده (اگر Cloudflare گیر داد، ارور می‌ده)
            await page.wait_for_selector('body', timeout=30000)  # صبر برای body

            # استخراج تعداد کل بک‌لینک‌ها (اختیاری، برای دیباگ)
            try:
                total_elem = await page.select_one('[data-ui="total-backlinks"]')  # selector تقریبی
                total_text = await total_elem.text() if total_elem else "N/A"
                print(f"DEBUG: Total backlinks for {domain}: {total_text}")
            except:
                print("DEBUG: Total backlinks not found.")

            # استخراج لیست بک‌لینک‌ها (table rows)
            rows = await page.select_all('tr[data-ui="backlink-row"]')  # selector تقریبی برای rows

            for row in rows[:5]:  # فقط ۵ تا اول برای تست (Ahrefs top ۱۰۰ نشون می‌ده)
                try:
                    # selectorها رو بر اساس inspect element تنظیم کن (این‌ها تقریبی هستن)
                    source_elem = await row.select_one('td.backlink-from a')  # منبع URL
                    source_url = await source_elem.get_attribute('href') if source_elem else ""
                    source_domain = source_url.split('/')[2] if source_url and len(source_url.split('/')) > 2 else ""

                    anchor_elem = await row.select_one('td.anchor-text')  # متن انکر
                    anchor_text = await anchor_elem.text() if anchor_elem else ""

                    dr_elem = await row.select_one('td.dr')  # DR (به جای harmonic centrality)
                    dr = await dr_elem.text() if dr_elem else ""

                    # فیلدهای دیگه (Ahrefs تاریخ دقیق در free نمیده، پس N/A)
                    links.append({
                        "domain_source": source_domain,
                        "url_source": source_url,
                        "domain_target": domain,  # هدف همیشه domain ورودی
                        "url_target": f"https://{domain}",  # ساده‌سازی
                        "anchor_text": anchor_text,
                        "harmonic_centrality": dr,  # DR رو به جاش بذار (مشابه متریک)
                        "last_found_date": "N/A"  # Ahrefs در free نداره
                    })
                except Exception as e:
                    print(f"DEBUG: Error in row for {domain}: {e}")
                    continue

            await browser.stop()
            return links

        except Exception as e:
            print(f"❌ Error scraping Ahrefs for {domain}: {e}")
            return []

    def fetch_links(self, domain):
        # wrapper sync برای سازگاری با app.py
        return asyncio.run(self.fetch_ahrefs_backlinks(domain))    
    
    
    
    
"""    

# =============================================================================
# 
# 
# import nest_asyncio
# nest_asyncio.apply()  # برای Spyder و محیط‌های REPL
# 
# import asyncio
# import nodriver as uc
# import random
# import time
# 
# class BacklinkAnalyzer:
#     def __init__(self):
#         self.proxy = None  # اگر proxy داری: "http://user:pass@ip:port"
# 
#     async def fetch_ahrefs_backlinks(self, domain):
#         links = []
#         try:
#             # تنظیمات browser
#             browser_args = [
#                 '--no-sandbox',                # برای جلوگیری از مشکلات اتصال
#                 '--disable-dev-shm-usage',     # مفید در محیط‌های محدود (ویندوز هم گاهی کمک می‌کنه)
#                 '--disable-gpu',               # گاهی لازم
#             ]
#             if self.proxy:
#                 browser_args.append(f'--proxy-server={self.proxy}')
# 
#             browser = await uc.start(
#                 headless=True,                 # False کن اگر می‌خوای مرورگر باز ببینی
#                 no_sandbox=True,               # کلیدی برای فیکس ارور Failed to connect
#                 browser_args=browser_args
#             )
# 
#             url = f"https://ahrefs.com/backlink-checker?input={domain}&mode=subdomains"
#             page = await browser.get(url)
# 
#             # صبر رندم برای لود و رد Cloudflare
#             await asyncio.sleep(8 + random.uniform(2, 5))
# 
#             # منتظر body (برای اطمینان از لود کامل)
#             try:
#                 await page.wait_for_selector('body', timeout=45000)  # ۴۵ ثانیه تایم‌اوت بیشتر
#             except:
#                 print("DEBUG: body selector timeout - ممکنه صفحه کامل لود نشده باشه")
# 
#             # دیباگ: تعداد بک‌لینک‌ها
#             try:
#                 total_elem = await page.select_one('[data-ui="total-backlinks"], .total-backlinks, [class*="backlinks-count"]')
#                 total_text = await total_elem.text() if total_elem else "N/A"
#                 print(f"DEBUG: Total backlinks for {domain}: {total_text}")
#             except:
#                 print("DEBUG: Total backlinks selector پیدا نشد.")
# 
#             # استخراج rows بک‌لینک‌ها (selectorها تقریبی - اگر کار نکرد inspect کن)
#             rows = await page.select_all('tr[data-ui="backlink-row"], table.backlinks-table tr, .backlink-row')
#             print(f"DEBUG: {len(rows)} row پیدا شد برای {domain}")
# 
#             for row in rows[:5]:  # فقط ۵ تا اول
#                 try:
#                     source_elem = await row.select_one('td.backlink-from a, a[href^="http"], .source-url a')
#                     source_url = await source_elem.get_attribute('href') if source_elem else ""
#                     source_domain = source_url.split('/')[2] if source_url and len(source_url.split('/')) > 2 else ""
# 
#                     anchor_elem = await row.select_one('td.anchor-text, .anchor, [class*="anchor"]')
#                     anchor_text = await anchor_elem.text() if anchor_elem else ""
# 
#                     dr_elem = await row.select_one('td.dr, .dr-value, [class*="dr"]')
#                     dr = await dr_elem.text() if dr_elem else ""
# 
#                     links.append({
#                         "domain_source": source_domain,
#                         "url_source": source_url,
#                         "domain_target": domain,
#                         "url_target": f"https://{domain}",
#                         "anchor_text": anchor_text,
#                         "harmonic_centrality": dr,  # DR رو اینجا می‌ذاریم
#                         "last_found_date": "N/A"
#                     })
#                 except Exception as e:
#                     print(f"DEBUG: Error in extracting row for {domain}: {e}")
#                     continue
# 
#             await browser.stop()
#             return links
# 
#         except Exception as e:
#             print(f"❌ Error scraping Ahrefs for {domain}: {e}")
#             return []
# 
#     def fetch_links(self, domain):
#         # wrapper برای سازگاری با app.py (sync call)
#         loop = asyncio.get_event_loop()
#         if loop.is_running():
#             # اگر در Spyder/Jupyter هستیم
#             return asyncio.run_coroutine_threadsafe(self.fetch_ahrefs_backlinks(domain), loop).result()
#         else:
#             return asyncio.run(self.fetch_ahrefs_backlinks(domain))
# 
# 
# 
# =============================================================================







##################### کد مخصوص برای این ای پی 

# =============================================================================
# import requests
# 
# class BacklinkAnalyzer:
#     def __init__(self):
#         self.api_key = "c748f1cf0cmsh260949e38535d40p140fb1jsnbcd0202cd7c9"
#         self.host = "best-backlink-checker-api.p.rapidapi.com"
#         self.endpoint = "/backlinks.php"  # ← این endpoint درست از مثال cURL
# 
#         self.proxies = {
#             'http':  'socks5h://127.0.0.1:8351',
#             'https': 'socks5h://127.0.0.1:8351',
#         }
# 
#     def fetch_links(self, domain):
#         url = f"https://{self.host}{self.endpoint}"
# 
#         headers = {
#             "x-rapidapi-host": self.host,
#             "x-rapidapi-key": self.api_key
#         }
# 
#         params = {
#             "domain": domain  # پارامتر اصلی domain هست
#         }
# 
#         try:
#             response = requests.get(
#                 url,
#                 headers=headers,
#                 params=params,
#                 timeout=20,
#                 proxies=self.proxies
#             )
# 
#             print(f"DEBUG status code: {response.status_code}")
#             print(f"DEBUG full URL sent: {response.request.url}")
# 
#             if response.status_code == 200:
#                 data = response.json()
#                 print(f"DEBUG raw data for {domain}: {data}")
#                 # ساختار خروجی رو بر اساس DEBUG تنظیم کن
#                 # مثلاً اگر لیست بک‌لینک‌ها در کلید "backlinks" یا "links" بود
#                 return data.get("backlinks", data.get("links", data.get("results", [])))
# 
#             elif response.status_code == 404:
#                 print("❌ 404: endpoint اشتباه یا API تغییر کرده - playground چک کن")
#             elif response.status_code == 401 or response.status_code == 403:
#                 print("❌ 401/403: مشکل key یا subscription - پلن رو چک کن")
#             else:
#                 print(f"⚠️ خطای {response.status_code}: {response.text}")
# 
#         except requests.exceptions.ProxyError as e:
#             print(f"❌ مشکل پروکسی: {e} - فیلترشکن چک کن")
#         except Exception as e:
#             print(f"❌ خطای کلی: {e}")
# 
#         return []
# 
# 
# 
# =============================================================================


# seRanking

# =============================================================================
# import requests
# 
# class BacklinkAnalyzer:
#     def __init__(self):
#         self.api_key = "9ddab358-0fce-1998-0630-8f5e965de4c6"  # کلید API خود را وارد کنید
#         self.base_url = "https://api.seranking.com/v1"  # URL SE Ranking API
#         self.site_id = "35fc70ecf1d8be2248951955db3d10475bb2a5fb"  # شناسه سایت خود را وارد کنید
# 
#     def fetch_links(self, limit=100, offset=0):
#         url = f"{self.base_url}/backlinks/{self.site_id}?limit={limit}&offset={offset}"
# 
#         headers = {
#             "Authorization": f"Token {self.api_key}",  # استفاده از "Token" برای احراز هویت
#         }
# 
#         try:
#             response = requests.get(url, headers=headers, timeout=20)
# 
#             print(f"DEBUG status code: {response.status_code}")
#             print(f"DEBUG full URL sent: {response.request.url}")
# 
#             if response.status_code == 200:
#                 data = response.json()
#                 print(f"DEBUG raw data: {data}")
#                 # استخراج بک‌لینک‌ها از داده‌های پاسخ
#                 return data.get("backlinks", data.get("results", []))
# 
#             elif response.status_code == 404:
#                 print("❌ 404: Endpoint اشتباه یا API تغییر کرده - لطفاً playground چک کنید")
#             elif response.status_code == 401 or response.status_code == 403:
#                 print("❌ 401/403: مشکل در API Key یا اشتراک - پلن را چک کنید")
#             else:
#                 print(f"⚠️ خطای {response.status_code}: {response.text}")
# 
#         except requests.exceptions.RequestException as e:
#             print(f"❌ خطای درخواست: {e}")
# 
#         return []
# 
# # استفاده از کد
# 
# =============================================================================

# backlink_module.py


import requests
import json

class BacklinkAnalyzer:
    def __init__(self):
        # کلید Data API که تو داشبورد ساختی (backlink - Data)
        self.api_key = "9ddab358-0fce-1998-0630-8f5e965de4c6"  # ← اینو عوض کن با کلید واقعی خودت
        
        self.base_url = "https://api.seranking.com"
        # بهترین endpoint برای لیست بک‌لینک‌ها: /v1/backlinks/all یا /v1/backlinks/raw (برای pagination بهتر)
        self.endpoint = "/v1/backlinks/all"  # یا "/v1/backlinks/raw" اگر حجم خیلی زیاد داری

        # اگر هنوز پروکسی لازم داری (اختیاری)
        
    def fetch_links(self, domain, limit=20, offset=0, mode="domain"):
        
        url = f"{self.base_url}{self.endpoint}"

        headers = {
            "Authorization": f"Token {self.api_key}",  # روش پیشنهادی و امن
            "Content-Type": "application/json"
        }

        params = {
            "target": domain,
            "mode": mode,          # domain / host / url
            "limit": limit,
            "offset": 0,
            "order_by": "date_found",               # جدیدترین بک‌لینک‌ها اول میان
            "nofollow_filter": "dofollow_only",     # فقط dofollow – این درستشه
            "min_domain_inlink_rank": 5,            # حداقل InLink Rank دامنه رفرینگ
            "min_inlink_rank": 3,                   # حداقل InLink Rank صفحه لینک‌دهنده
            
            
            
            
            
            
            
            # اختیاری‌های مفید:
            # "order_by": "inlink_rank",  # یا date_found, domain_inlink_rank و ...
            # "per_domain": 1,            # حداکثر ۱ لینک از هر دامنه
            # "nofollow_filter": "dofollow",
            # "output": "json"
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            print(f"DEBUG status code: {response.status_code}")
            print(f"DEBUG full URL sent: {response.request.url}")

            if response.status_code == 200:
                data = response.json()
                print(f"DEBUG raw data keys: {list(data.keys())}")  # ببین ساختار چیه

                # ساختار معمول خروجی /all:
                # لیست مستقیم از دیکشنری‌ها (هر آیتم یک بک‌لینک)
                # کلیدهای مهم: url_from, url_to, anchor, nofollow, inlink_rank, domain_inlink_rank, first_seen, ...
                backlinks = data if isinstance(data, list) else data.get("backlinks", [])
                
                print(f"تعداد بک‌لینک‌های دریافتی: {len(backlinks)}")
                return backlinks

            elif response.status_code in (401, 403):
                print("❌ 401/403: کلید API اشتباه یا منقضی شده - داشبورد SE Ranking چک کن")
            elif response.status_code == 429:
                print("❌ 429: Rate limit - credits تموم شده یا درخواست زیاد")
            else:
                print(f"⚠️ خطای {response.status_code}: {response.text}")

        except requests.exceptions.ProxyError as e:
            print(f"❌ مشکل پروکسی: {e}")
        except Exception as e:
            print(f"❌ خطای کلی: {e}")

        return []

# مثال استفاده