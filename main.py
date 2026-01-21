import time
import requests
import pickle
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. إعدادات المسارات (تأكد من صحة الرابط أو استخدم الرابط المباشر)
# ملاحظة 2026: روابط المشاركة في PythonAnywhere قد تتطلب User-Agent
ORDER_FILE_URL = "https://www.pythonanywhere.com/user/wwwwww/shares/997658e3d18e4497a46147634dca7b90/"
COOKIE_FILE = "tiktok_session.pkl"

def get_driver(show_browser=True):
    options = uc.ChromeOptions()
    if not show_browser:
        options.add_argument('--headless')
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    return driver

def run_bot(target_url, username, password):
    driver = get_driver(show_browser=True)
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get("https://www.tiktok.com")
        
        if os.path.exists(COOKIE_FILE):
            print("🍪 جاري تحميل الجلسة...")
            cookies = pickle.load(open(COOKIE_FILE, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(5)

        if "login" in driver.current_url or not os.path.exists(COOKIE_FILE):
            print(f"👤 تسجيل دخول: {username}")
            # تحديث محددات العناصر لتناسب تيك توك 2026
            wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
            driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            print("⚠️ حل الكابتشا الآن يدوياً (أمامك 60 ثانية)...")
            time.sleep(60) 
            
            pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))

        print(f"🚀 التوجه للهدف: {target_url}")
        driver.get(target_url)
        time.sleep(7)
        
        follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        follow_btn.click()
        print(f"✔️ نجاح المتابعة: {username}")

    except Exception as e:
        print(f"❌ خطأ في التنفيذ: {e}")
    finally:
        driver.quit()

def start():
    print("📡 جاري فحص الملف المشترك...")
    # إضافة Headers لأن السيرفرات في 2026 تحظر البوتات البسيطة
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(ORDER_FILE_URL, headers=headers, timeout=20)
        
        # التأكد من نجاح الاتصال
        if response.status_code == 200:
            # تنظيف النص المستلم من أي كود HTML إذا وجد
            raw_text = response.text
            if "<html" in raw_text.lower():
                print("❌ خطأ: الرابط يفتح صفحة ويب وليس ملف نصي. تأكد من تفعيل 'Direct Link'.")
                return

            orders = [line.strip() for line in raw_text.split('\n') if line.strip()]
            
            if not orders:
                print("😴 لا توجد طلبات.")
                return

            with open("accounts.txt", "r") as f:
                accounts = [l.strip().split(":") for l in f if ":" in l]

            for url in orders:
                for user, pw in accounts:
                    run_bot(url, user, pw)
                    time.sleep(10)
        else:
            print(f"❌ فشل الوصول. كود الحالة: {response.status_code}")
    except Exception as e:
        print(f"⚠️ خطأ عام: {e}")

if __name__ == "__main__":
    start()
