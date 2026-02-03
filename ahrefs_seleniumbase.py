
"""
Ahrefs Scraper با SeleniumBase UC Mode
# بهترین روش برای bypass کردن Cloudflare!
"""

from seleniumbase import SB
import time
import json
from typing import List, Dict, Optional


class AhrefsSeleniumBase:
    def __init__(self, headless: bool = False):
        """
        Args:
            headless: False برای دیدن مرورگر (پیشنهادی)
        """
        self.headless = headless
        self.base_url = "https://ahrefs.com/backlink-checker"
    
    def fetch_backlinks(self, domain: str, wait_time: int = 10) -> List[Dict]:
        """
#         دریافت بک‌لینک با SeleniumBase UC mode
        
        Args:
            domain: دامنه مورد نظر
            wait_time: زمان انتظار برای لود شدن جدول (ثانیه)
        
        Returns:
#             لیست بک‌لینک‌ها
        """
        backlinks = []
        
        print(f"🚀 شروع scraping برای: {domain}")
        
        with SB(uc=True, test=True, headless=self.headless, locale_code="en") as sb:
            try:
#                 # باز کردن صفحه با reconnect (برای bypass Cloudflare)
                print("🌐 در حال باز کردن Ahrefs...")
                url = f"{self.base_url}?input={domain}&mode=subdomains"
                sb.driver.uc_open_with_reconnect(url, reconnect_time=4)
                
                print("⏳ صبر برای bypass Cloudflare...")
                time.sleep(5)
                
#                 # چک کردن عنوان صفحه
                print(f"📄 عنوان صفحه: {sb.get_title()}")
                
#                 # صبر برای لود شدن جدول
                print(f"⏳ صبر {wait_time} ثانیه برای لود جدول...")
                time.sleep(wait_time)
                
                # Screenshot برای دیباگ
                screenshot_path = f"seleniumbase_{domain.replace('.', '_')}.png"
                sb.save_screenshot(screenshot_path, folder=".")
                print(f"📸 Screenshot ذخیره شد: {screenshot_path}")
                
#                 # استخراج بک‌لینک‌ها
                print("🔍 در حال استخراج بک‌لینک‌ها...")
                backlinks = self._extract_backlinks(sb, domain)
                
                if backlinks:
                    print(f"✅ {len(backlinks)} بک‌لینک پیدا شد!")
                else:
                    print("⚠️ هیچ بک‌لینکی پیدا نشد")
                    print("💡 Screenshot رو چک کن تا ببینی صفحه چطور لود شده")
                
            except Exception as e:
                print(f"❌ خطا: {e}")
                import traceback
                traceback.print_exc()
        
        return backlinks
    
    def _extract_backlinks(self, sb, domain: str) -> List[Dict]:
#         """استخراج بک‌لینک‌ها از جدول"""
        backlinks = []
        
        try:
#             # پیدا کردن جدول
            # Ahrefs از چندین selector ممکن استفاده می‌کنه
            table_selectors = [
                'table tbody tr',
                'table tr',
                'div[role="table"] div[role="row"]',
                '[class*="backlink"] tr'
            ]
            
            rows = []
            for selector in table_selectors:
                try:
                    if sb.is_element_visible(selector):
                        rows = sb.find_elements(selector)
                        print(f"✅ جدول پیدا شد با selector: {selector}")
                        print(f"📊 تعداد ردیف‌ها: {len(rows)}")
                        break
                except:
                    continue
            
            if not rows:
                print("❌ جدول پیدا نشد!")
                return []
            
#             # استخراج داده از هر ردیف
            for i, row in enumerate(rows[:100]):  # حداکثر 100
                try:
#                     # پیدا کردن لینک‌ها در ردیف
                    links = row.find_elements("tag name", "a")
                    
                    if len(links) >= 1:
                        url_from = links[0].get_attribute("href")
                        
#                         # فیلتر کردن لینک‌های داخلی Ahrefs
                        if url_from and not any(x in url_from for x in [
                            'ahrefs.com',
                            'help.ahrefs',
                            'youtube.com/c/Ahrefs',
                            'chrome.google.com/webstore',
                            'addons.mozilla.org',
                            'wordcount.com',
                            'ahrefstop.com',
                            'docs.ahrefs',
                            'tech.ahrefs'
                        ]):
#                             # گرفتن متن ردیف
                            row_text = row.text
                            
                            # Anchor text (معمولاً در ستون دوم یا سوم)
                            anchor = "N/A"
                            try:
                                cells = row.find_elements("tag name", "td")
                                if len(cells) >= 2:
                                    anchor = cells[1].text[:200]
                            except:
                                pass
                            
#                             # چک کردن nofollow
                            is_nofollow = "nofollow" in row_text.lower()
                            
                            backlink = {
                                "url_from": url_from,
                                "url_to": f"https://{domain}",
                                "anchor": anchor.strip() if anchor else "N/A",
                                "domain_rating": "N/A",
                                "nofollow": is_nofollow,
                                "source": "ahrefs_seleniumbase"
                            }
                            
                            backlinks.append(backlink)
                            
                            if i < 3:  # نمایش 3 تای اول
                                print(f"  {i+1}. {url_from[:60]}...")
                
                except Exception as e:
#                     # ادامه به ردیف بعدی
                    continue
        
        except Exception as e:
            print(f"❌ خطا در استخراج: {e}")
        
        return backlinks


def scrape_ahrefs_seleniumbase(
    domain: str,
    headless: bool = False,
    wait_time: int = 10
) -> List[Dict]:
    """
    Helper function برای استفاده آسان
    
    Args:
        domain: دامنه
        headless: False = مرورگر نمایش داده میشه
        wait_time: زمان انتظار برای لود (ثانیه)
    
    Returns:
#         لیست بک‌لینک‌ها
    """
    scraper = AhrefsSeleniumBase(headless=headless)
    return scraper.fetch_backlinks(domain, wait_time=wait_time)


# Test
if __name__ == "__main__":
    print("="*70)
    print("🔥 AHREFS SCRAPER - SeleniumBase UC Mode")
    print("="*70)
    print("\n✨ Features:")
    print("  ✅ Undetected Chrome (UC mode)")
    print("  ✅ Cloudflare bypass بدون دخالت دستی")
    print("  ✅ Auto reconnect")
    print("  ✅ Screenshot برای دیباگ")
    print("="*70 + "\n")
    
    domain = input("🔑 دامنه را وارد کنید: ").strip() or "kiyandaria.com"
    
    headless_input = input("🖥️  Headless mode? (y/n) [n]: ").strip().lower()
    headless = headless_input == 'y'
    
    wait_input = input("⏱️  زمان انتظار برای لود جدول (ثانیه) [10]: ").strip()
    wait_time = int(wait_input) if wait_input.isdigit() else 10
    
    print("\n" + "="*70)
    print("🚀 شروع...")
    print("="*70 + "\n")
    
    backlinks = scrape_ahrefs_seleniumbase(
        domain=domain,
        headless=headless,
        wait_time=wait_time
    )
    
    print("\n" + "="*70)
    print(f"📊 نتیجه: {len(backlinks)} بک‌لینک")
    print("="*70)
    
    if backlinks:
        print("\n✅ نمونه بک‌لینک‌ها:\n")
        for i, link in enumerate(backlinks[:5], 1):
            print(f"{i}. {link['url_from']}")
            print(f"   Anchor: {link['anchor'][:50]}")
            print(f"   Nofollow: {'بله' if link['nofollow'] else 'خیر'}\n")
        
#         # ذخیره در JSON
        filename = f"{domain.replace('.', '_')}_backlinks_sb.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backlinks, f, indent=2, ensure_ascii=False)
        
        print(f"💾 ذخیره شد در: {filename}")
    else:
        print("\n❌ هیچ بک‌لینکی استخراج نشد")
        print("\n💡 پیشنهادات:")
        print("  1. Screenshot رو چک کن")
        print("  2. wait_time رو بیشتر کن (مثلاً 15 ثانیه)")
        print("  3. دوباره امتحان کن")
        print("  4. مطمئن شو که دامنه درست وارد شده")






# =============================================================================
# 
# """
# ahrefs_seleniumbase.py - Fixed version
# فیکس مشکل Permission Denied و دانلود تکراری chromedriver
# """
# 
# import json
# import time
# import os
# from typing import List, Dict
# 
# # ✅ FIX: chromedriver رو به پوشه پروژه دانلود کنه نه site-packages
# # این باید قبل از import SB باشه!
# DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver_local")
# os.makedirs(DRIVER_PATH, exist_ok=True)
# os.environ["CHROMEDRIVER_PATH"] = DRIVER_PATH
# 
# from seleniumbase import SB
# 
# 
# class AhrefsSeleniumBase:
#     def __init__(self, headless: bool = False):
#         self.headless = headless
#         self.base_url = "https://ahrefs.com/backlink-checker"
#     
#     def fetch_backlinks(self, domain: str, wait_time: int = 10) -> List[Dict]:
#         backlinks = []
#         print(f"🚀 شروع scraping برای: {domain}")
#         
#         try:
#             with SB(uc=True, test=True, headless=self.headless, locale_code="en") as sb:
#                 try:
#                     print("🌐 در حال باز کردن Ahrefs...")
#                     url = f"{self.base_url}?input={domain}&mode=subdomains"
#                     sb.driver.uc_open_with_reconnect(url, reconnect_time=4)
#                     
#                     print("⏳ صبر برای bypass Cloudflare...")
#                     time.sleep(5)
#                     
#                     print(f"📄 عنوان صفحه: {sb.get_title()}")
#                     
#                     print(f"⏳ صبر {wait_time} ثانیه برای لود جدول...")
#                     time.sleep(wait_time)
#                     
#                     screenshot_path = f"seleniumbase_{domain.replace('.', '_')}.png"
#                     sb.save_screenshot(screenshot_path, folder=".")
#                     print(f"📸 Screenshot: {screenshot_path}")
#                     
#                     print("🔍 استخراج بک‌لینک‌ها...")
#                     backlinks = self._extract_backlinks(sb, domain)
#                     
#                     if backlinks:
#                         print(f"✅ {len(backlinks)} بک‌لینک پیدا شد!")
#                     else:
#                         print("⚠️ هیچ بک‌لینکی پیدا نشد")
#                 
#                 except Exception as e:
#                     print(f"❌ خطا: {e}")
#                     import traceback
#                     traceback.print_exc()
#         
#         except Exception as e:
#             print(f"❌ خطا در شروع SeleniumBase: {e}")
#             if "Permission denied" in str(e) or "Errno 13" in str(e):
#                 print("💡 chromedriver_local پوشه ساخته شده - دوباره سعی کن")
#         
#         return backlinks
#     
#     def _extract_backlinks(self, sb, domain: str) -> List[Dict]:
#         backlinks = []
#         try:
#             table_selectors = [
#                 'table tbody tr',
#                 'table tr',
#                 'div[role="table"] div[role="row"]',
#                 '[class*="backlink"] tr'
#             ]
#             
#             rows = []
#             for selector in table_selectors:
#                 try:
#                     if sb.is_element_visible(selector):
#                         rows = sb.find_elements(selector)
#                         if rows:
#                             print(f"✅ جدول پیدا شد: {selector} ({len(rows)} row)")
#                             break
#                 except:
#                     continue
#             
#             if not rows:
#                 print("⚠️ هیچ جدولی پیدا نشد")
#                 return backlinks
#             
#             for row in rows[1:]:
#                 try:
#                     cells = row.find_elements("css selector", "td")
#                     if len(cells) >= 2:
#                         backlink = {
#                             "url_from": cells[0].text.strip() if len(cells) > 0 else "N/A",
#                             "url_to": cells[1].text.strip() if len(cells) > 1 else "N/A",
#                             "anchor": cells[2].text.strip() if len(cells) > 2 else "N/A",
#                             "nofollow": False,
#                             "domain_rating": "N/A",
#                             "source": "ahrefs"
#                         }
#                         backlinks.append(backlink)
#                 except:
#                     continue
#         except Exception as e:
#             print(f"❌ خطا در استخراج: {e}")
#         
#         return backlinks
# 
# 
# def scrape_ahrefs_seleniumbase(domain: str, headless: bool = False, wait_time: int = 10) -> List[Dict]:
#     scraper = AhrefsSeleniumBase(headless=headless)
#     return scraper.fetch_backlinks(domain, wait_time=wait_time)
# 
# 
# if __name__ == "__main__":
#     print("=" * 50)
#     print("🔥 AHREFS SCRAPER - Fixed")
#     print("=" * 50)
#     domain = input("دامنه: ").strip() or "kiyandaria.com"
#     backlinks = scrape_ahrefs_seleniumbase(domain=domain, headless=False, wait_time=10)
#     print(f"\n📊 نتیجه: {len(backlinks)} بک‌لینک")
#     for i, link in enumerate(backlinks[:5], 1):
#         print(f"{i}. {link['url_from']}")
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# =============================================================================











