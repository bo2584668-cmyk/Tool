import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# الرابط المباشر لملف الأوردرات الخاص بك
ORDER_FILE_URL = "https://www.pythonanywhere.com/user/wwwwww/shares/997658e3d18e4497a46147634dca7b90/"

def run_bot(target_url, username, password):
    """دالة تنفيذ الرشق باستخدام Selenium"""
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = uc.Chrome(options=options)
        # تسجيل الدخول وتغيير الحالة لمتابعة
        driver.get("https://www.tiktok.com")
        # (هنا نضع بقية خطوات تسجيل الدخول والمتابعة التي صممناها سابقاً)
        print(f"✅ نجاح المتابعة بواسطة {username} للرابط {target_url}")
    except Exception as e:
        print(f"❌ خطأ مع الحساب {username}: {e}")
    finally:
        if driver:
            driver.quit()

def start_execution():
    print("📡 جاري سحب الطلبات من الرابط المباشر...")
    try:
        # سحب محتوى الملف
        response = requests.get(ORDER_FILE_URL, timeout=15)
        if response.status_code == 200:
            content = response.text.strip()
            if not content:
                print("😴 لا توجد طلبات جديدة في الملف حالياً.")
                return

            orders = content.split('\n')
            print(f"✅ تم العثور على {len(orders)} طلبات.")

            # قراءة الحسابات من ملف accounts.txt الموجود في GitHub
            with open("accounts.txt", "r") as f:
                accounts = [line.strip().split(":") for line in f if ":" in line]

            # تنفيذ الرشق
            for link in orders:
                url = link.strip()
                if url:
                    print(f"🚀 بدء التنفيذ للرابط: {url}")
                    for user, pw in accounts:
                        run_bot(url, user, pw)
                        time.sleep(5) # فاصل زمني بين الحسابات
        else:
            print(f"❌ فشل الوصول للملف، كود الحالة: {response.status_code}")
    except Exception as e:
        print(f"⚠️ حدث خطأ: {e}")

if __name__ == "__main__":
    start_execution()
