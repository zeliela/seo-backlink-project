# 🚀 راهنمای سریع Deploy در Hugging Face Spaces

## مراحل به زبان ساده:

### 1️⃣ ساخت اکانت Hugging Face
- به سایت [huggingface.co](https://huggingface.co) بروید
- Sign up کنید (رایگان)

### 2️⃣ ساخت Space جدید
1. روی عکس پروفایل کلیک کنید → **New Space**
2. تنظیمات:
   - نام Space: `seo-backlink-analyzer`
   - SDK: **Docker** (حتماً!)
   - Hardware: **CPU basic - FREE**
   - Public یا Private
3. **Create Space** کلیک کنید

### 3️⃣ آپلود فایل‌ها

#### روش ساده (Web):
1. در صفحه Space → **Files and versions**
2. **Add file** → **Upload files**
3. این فایل‌ها را آپلود کنید:
   ```
   ✅ Dockerfile
   ✅ requirements.txt
   ✅ streamlit_app.py
   ✅ google_module.py
   ✅ hybrid_backlink_v2.py
   ✅ backlink_module.py
   ✅ ahrefs_seleniumbase.py
   ```
4. پوشه `.streamlit` بسازید و `config.toml` آپلود کنید

### 4️⃣ تنظیم Google Sheets

#### الف) گرفتن Service Account:
1. [console.cloud.google.com](https://console.cloud.google.com)
2. پروژه جدید بسازید
3. **APIs & Services** → **Enable APIs**
4. فعال کنید:
   - Google Sheets API
   - Google Drive API
5. **Credentials** → **Create Credentials** → **Service Account**
6. Service Account بسازید
7. **Keys** → **Add Key** → **JSON**
8. فایل JSON دانلود می‌شود

#### ب) اضافه کردن به Hugging Face:
1. Space شما → **Settings**
2. **Repository secrets** → **New secret**
3. Name: `GCP_SERVICE_ACCOUNT`
4. Value: کل محتوای فایل JSON را Paste کنید
5. **Add secret**

#### ج) دسترسی به Sheet:
1. Google Sheet باز کنید
2. **Share** → Email سرویس اکانت اضافه کنید
   - Email از فایل JSON → `client_email`
3. دسترسی **Editor** بدهید

### 5️⃣ صبر کنید Build شود
- زمان: 5-10 دقیقه
- در بخش **Logs** پیشرفت را ببینید
- وقتی آماد شد: **App running on port 7860** نمایش داده می‌شود

### 6️⃣ باز کردن اپلیکیشن
- URL شما:
  ```
  https://huggingface.co/spaces/YOUR_USERNAME/seo-backlink-analyzer
  ```
- روی **App** کلیک کنید

## ✅ تست اولیه

1. کلمه کلیدی وارد کنید: "خرید لپ تاپ"
2. منبع: **Ahrefs (رایگان)**
3. **شروع جستجو**
4. رقبا انتخاب کنید
5. نتایج را ببینید!

## 🔧 اگر مشکلی داشت:

### Build ناموفق:
- چک کنید SDK حتماً **Docker** باشد
- Hardware: **CPU basic**
- Dockerfile درست آپلود شده؟

### Google Sheets کار نمی‌کند:
- Secret درست اضافه شده؟
- Service Account در Sheet اشتراک داده شده؟
- API ها فعال هستند؟

### Ahrefs نتیجه نمی‌دهد:
- زمان انتصار را 15-20 ثانیه کنید
- دوباره تست کنید

## 📞 کمک بیشتر

README.md کامل را بخوانید

---

**موفق باشید! 🎉**
