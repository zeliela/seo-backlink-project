"""
این کد با اون فایل تکی که کلود داد جایگزین شد


"""

"""
google_module.py - Fixed version
دریافت 10 نتیجه اول گوگل
"""

import requests


class GoogleSerper:
    def __init__(self):
        self.api_key = "3763f809f57f27585449c4628d451a54dfca73a8"
        self.url = "https://google.serper.dev/search"
    
    def get_competitors(self, keyword, num_results=4):
        """
        دریافت رقبا از گوگل
        
        Args:
            keyword: کلمه کلیدی
            num_results: تعداد نتایج (پیش‌فرض: 10)
        
        Returns:
            لیست نتایج گوگل
        """
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": keyword,
            "gl": "ir",
            "hl": "fa",
            "num": num_results  # تغییر از 1 به num_results
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            
            if response.status_code == 200:
                results = response.json().get("organic", [])
                print(f"✅ {len(results)} نتیجه از گوگل دریافت شد")
                return results
            else:
                print(f"❌ خطای API گوگل: {response.status_code}")
                return []
        
        except Exception as e:
            print(f"❌ خطا در دریافت از گوگل: {e}")
            return []


# Test
# =============================================================================
# if __name__ == "__main__":
#     google = GoogleSerper()
#     results = google.get_competitors("خرید لپ تاپ", num_results=10)
#     
#     print(f"\n📊 {len(results)} نتیجه:")
#     for i, item in enumerate(results, 1):
#         print(f"{i}. {item.get('title', 'N/A')}")
#         print(f"   {item.get('link', 'N/A')}\n")
# =============================================================================
