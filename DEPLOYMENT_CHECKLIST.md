# ✅ Checklist قبل از Deploy

## 📋 فایل‌های ضروری

- [ ] `Dockerfile` ✅
- [ ] `requirements.txt` ✅
- [ ] `streamlit_app.py` ✅
- [ ] `google_module.py` ✅
- [ ] `hybrid_backlink_v2.py` ✅
- [ ] `backlink_module.py` ✅
- [ ] `ahrefs_seleniumbase.py` ✅
- [ ] `.streamlit/config.toml` ✅
- [ ] `app.yaml` ✅
- [ ] `README.md` ✅

## 🔑 API Keys

### Google Serper (برای جستجوی Google)
- [ ] ثبت‌نام در [serper.dev](https://serper.dev)
- [ ] دریافت API Key رایگان
- [ ] جایگزینی در `google_module.py`:
  ```python
  self.api_key = "YOUR_API_KEY_HERE"
  ```

### SE Ranking (اختیاری - برای بک‌لینک)
- [ ] اگر می‌خواهید SE Ranking استفاده کنید
- [ ] جایگزینی در `backlink_module.py`:
  ```python
  self.api_key = "YOUR_SE_RANKING_KEY"
  ```

## 🗄️ Google Sheets Setup

### 1. Google Cloud Console
- [ ] پروژه جدید ساخته شد
- [ ] Google Sheets API فعال شد
- [ ] Google Drive API فعال شد
- [ ] Service Account ساخته شد
- [ ] JSON Key دانلود شد

### 2. Hugging Face Secret
- [ ] Space → Settings → Repository secrets
- [ ] Secret با نام `GCP_SERVICE_ACCOUNT` ساخته شد
- [ ] محتوای JSON کامل paste شد

### 3. Google Sheet Access
- [ ] Google Sheet ساخته شد
- [ ] Service Account email (از JSON) اشتراک گذاشته شد
- [ ] دسترسی Editor داده شد

## 🚀 Hugging Face Space

### تنظیمات Space
- [ ] SDK: **Docker** (نه Streamlit!)
- [ ] Hardware: **CPU basic** (رایگان)
- [ ] Visibility: Public یا Private

### فایل‌ها
- [ ] همه فایل‌های بالا آپلود شدند
- [ ] `.streamlit/config.toml` در پوشه درست است
- [ ] `app.yaml` در root قرار دارد

## 🧪 تست

### قبل از Deploy
- [ ] `google_module.py` API key دارد
- [ ] Secret درست تنظیم شد
- [ ] همه فایل‌ها آپلود شدند

### بعد از Deploy
- [ ] Build موفق بود (Logs چک شد)
- [ ] App روی port 7860 اجرا شد
- [ ] صفحه اصلی باز می‌شود
- [ ] جستجوی Google کار می‌کند
- [ ] Ahrefs scraping کار می‌کند
- [ ] Google Sheets ذخیره می‌کند

## 🔧 عیب‌یابی سریع

### Build Failed
```
✓ SDK را Docker انتخاب کردید؟
✓ Dockerfile درست آپلود شده؟
✓ requirements.txt کامل است؟
```

### Google Sheets Error
```
✓ Secret درست تنظیم شده؟
✓ JSON کامل paste شده؟
✓ Service Account در Sheet اشتراک دارد؟
✓ API ها فعال هستند؟
```

### Ahrefs No Results
```
✓ زمان انتظار کافی است؟ (10-15 ثانیه)
✓ دوباره تست کنید
✓ Headless را خاموش کنید برای دیباگ
```

## 📝 یادداشت‌ها

- اولین build حدود 5-10 دقیقه طول می‌کشد
- برای تست، از Headless=False استفاده کنید
- Logs را حتماً چک کنید
- برای debug، screenshot ها ذخیره می‌شوند

## ✨ وقتی همه چیز کار کرد:

🎉 **تبریک!** اپلیکیشن شما آماده است:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

این لینک را می‌توانید با دیگران به اشتراک بگذارید!

---

**نکته مهم**: Hugging Face Spaces کاملاً رایگان است و محدودیت زمانی ندارد!
