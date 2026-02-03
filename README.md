# 🔍 SEO Backlink Analyzer

ابزار قدرتمند تحلیل بک‌لینک SEO با قابلیت اسکرپ مستقیم Ahrefs

## ✨ ویژگی‌ها

- 🔍 **جستجوی هوشمند Google**: یافتن رقبای برتر برای هر کلمه کلیدی
- 🔗 **تحلیل بک‌لینک چندمنبعی**:
  - Ahrefs (رایگان) - اسکرپ مستقیم با SeleniumBase
  - SE Ranking API (پولی) - دقت بالا
- 📊 **ذخیره خودکار در Google Sheets**
- 📈 **گراف‌های تحلیلی تعاملی**
- 💾 **دانلود نتایج به صورت CSV**

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.10+
- Google Chrome (برای SeleniumBase)
- Google Sheets API credentials

### نصب Local

```bash
# Clone repository
git clone <your-repo-url>
cd seo-backlink-project

# نصب dependencies
pip install -r requirements.txt

# نصب ChromeDriver
python -m seleniumbase install chromedriver

# اجرا
streamlit run streamlit_app.py
```

## 🌐 Deploy در Hugging Face Spaces

### مرحله 1: ساخت Space

1. به [Hugging Face](https://huggingface.co) وارد شوید
2. به بخش **Spaces** بروید
3. کلیک کنید روی **Create new Space**
4. تنظیمات:
   - **Space name**: seo-backlink-analyzer (یا هر نام دیگری)
   - **License**: MIT
   - **Select SDK**: **Docker**
   - **Hardware**: CPU basic (رایگان)
   - **Space visibility**: Public یا Private

### مرحله 2: آپلود فایل‌ها

دو روش برای آپلود:

#### روش 1: Git (پیشنهادی)

```bash
# Clone کردن Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# کپی کردن فایل‌ها
cp /path/to/project/* .

# Push کردن
git add .
git commit -m "Initial commit"
git push
```

#### روش 2: Web Interface

در صفحه Space، روی **Files** کلیک کنید و فایل‌های زیر را آپلود کنید:
- `Dockerfile`
- `requirements.txt`
- `streamlit_app.py`
- `google_module.py`
- `hybrid_backlink_v2.py`
- `backlink_module.py`
- `ahrefs_seleniumbase.py`
- `.streamlit/config.toml`

### مرحله 3: تنظیم Google Sheets API

#### الف) دریافت Credentials

1. به [Google Cloud Console](https://console.cloud.google.com) بروید
2. یک پروژه جدید بسازید
3. **APIs & Services** → **Enable APIs**
4. فعال کنید: **Google Sheets API** و **Google Drive API**
5. **Credentials** → **Create Credentials** → **Service Account**
6. یک Service Account بسازید
7. **Keys** → **Add Key** → **JSON** → فایل JSON دانلود می‌شود

#### ب) تنظیم در Hugging Face

1. در صفحه Space، به **Settings** بروید
2. بخش **Repository secrets** را پیدا کنید
3. **New secret** کلیک کنید:
   - **Name**: `GCP_SERVICE_ACCOUNT`
   - **Value**: کل محتوای فایل JSON را کپی کنید

**مثال محتوای JSON:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@project.iam.gserviceaccount.com",
  ...
}
```

#### ج) اشتراک‌گذاری Google Sheet

1. Google Sheet خود را باز کنید
2. **Share** کلیک کنید
3. **Email** سرویس اکانت را اضافه کنید (از فایل JSON: `client_email`)
4. **Editor** دسترسی بدهید

### مرحله 4: راه‌اندازی

پس از آپلود فایل‌ها، Hugging Face به طور خودکار:
1. Dockerfile را build می‌کند
2. Chrome و ChromeDriver نصب می‌کند
3. Python packages نصب می‌شود
4. Streamlit اجرا می‌شود

**زمان build**: 5-10 دقیقه (اولین بار)

### مرحله 5: دسترسی به اپلیکیشن

URL شما:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

## 🔧 تنظیمات

### Google Serper API (برای جستجوی Google)

در فایل `google_module.py` کلید API خود را وارد کنید:

```python
self.api_key = "YOUR_SERPER_API_KEY"
```

دریافت کلید رایگان: [serper.dev](https://serper.dev)

### SE Ranking API (اختیاری)

در فایل `backlink_module.py`:

```python
self.api_key = "YOUR_SE_RANKING_API_KEY"
```

## 📖 نحوه استفاده

1. **کلمه کلیدی وارد کنید**: مثلاً "خرید لپ تاپ"
2. **منبع بک‌لینک انتخاب کنید**:
   - Ahrefs (رایگان) - پیشنهادی
   - SE Ranking (پولی)
   - هر دو
3. **تنظیمات Ahrefs** (اختیاری):
   - Headless mode: مرورگر مخفی (سریعتر)
   - زمان انتظار: 5-20 ثانیه
4. **کلیک روی "شروع جستجو"**
5. **رقبا را انتخاب کنید** (همه / دستی / 5 تا اول)
6. **نتایج را مشاهده کنید**:
   - نمایش در UI
   - ذخیره در Google Sheets
   - دانلود CSV

## 🛠️ عیب‌یابی

### مشکلات رایج

#### 1. Google Sheets ذخیره نمی‌شود
- بررسی کنید `GCP_SERVICE_ACCOUNT` در Secrets درست است
- Service Account در Sheet اشتراک داده شده؟
- API های Google Sheets و Drive فعال هستند؟

#### 2. Ahrefs کار نمی‌کند
- زمان انتظار را بیشتر کنید (15-20 ثانیه)
- Headless را خاموش کنید (تست)
- Logs را چک کنید

#### 3. Build ناموفق
- بررسی کنید Dockerfile صحیح است
- Hardware را CPU basic انتخاب کرده‌اید؟

## 📊 ساختار پروژه

```
seo-backlink-project/
├── Dockerfile                    # تنظیمات Docker
├── requirements.txt              # Python packages
├── streamlit_app.py             # UI اصلی
├── google_module.py             # Google Search
├── hybrid_backlink_v2.py        # منطق اصلی بک‌لینک
├── backlink_module.py           # SE Ranking API
├── ahrefs_seleniumbase.py       # Ahrefs scraper
└── .streamlit/
    └── config.toml              # تنظیمات Streamlit
```

## 🌟 مزایای Hugging Face Spaces

✅ **رایگان 100%** (تا 16GB RAM)  
✅ **پشتیبانی از Docker و Chrome**  
✅ **URL عمومی دائمی**  
✅ **بدون نیاز به کارت اعتباری**  
✅ **Auto-restart** در صورت خطا  
✅ **SSL/HTTPS** رایگان  

## 📝 نکات مهم

⚠️ **Ahrefs**: ممکن است Cloudflare چالش بدهد - زمان انتظار را افزایش دهید  
⚠️ **Rate Limiting**: از تعداد زیاد درخواست همزمان پرهیز کنید  
⚠️ **Google Sheets**: هر Sheet محدودیت 10 میلیون سلول دارد  

## 🤝 مشارکت

Pull request ها خوشامد است!

## 📄 مجوز

MIT License

## 💬 پشتیبانی

برای مشکلات یا سوالات، یک Issue باز کنید.

---

**ساخته شده با ❤️ برای تحلیل SEO**
