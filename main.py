import time
import requests
import pickle
import os
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 1. الإعدادات (تأكد من صحتها) ---
USERNAME = "wwwwww"  # اسم مستخدمك في PythonAnywhere
API_URL = f"https://{USERNAME}://"
COOKIE_FILE = "tiktok_session.pkl"

def get_driver(show_browser=True):
    """إعداد المتصفح لعام 2026 مع تخطي كشف البوتات"""
    options = uc.ChromeOptions()
    if not show_browser:
        options.add_argument('--headless')
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    return driver

def run_bot(target_url, username, password):
    """دالة التنفيذ مع إمكانية التدخل اليدوي لحل الكابتشا"""
    driver = get_driver(show_browser=True)
    wait = WebDriverWait(driver, 30)
    
    try:
        # الدخول لصفحة تيك توك
        driver.get("https://www.tiktok.com")
        
        # 1. محاولة تحميل الجلسة (Cookies) لتجنب الدخول المتكرر
        if os.path.exists(COOKIE_FILE):
            print("🍪 تحميل الجلسة السابقة...")
            cookies = pickle.load(open(COOKIE_FILE, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(5)

        # 2. إذا تطلب الأمر تسجيل دخول جديد
        if "login" in driver.current_url:
            print(f"👤 تسجيل دخول بالحساب: {username}")
            u_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            for char in username: u_field.send_keys(char); time.sleep(0.1)
            
            p_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            for char in password: p_field.send_keys(char); time.sleep(0.1)
            
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            print("⚠️ تنبيه تعليمي: قم بحل الكابتشا يدوياً الآن إذا ظهرت (أمامك 60 ثانية)...")
            time.sleep(60) 
            
            # حفظ الجلسة بعد النجاح
            pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
            print("✅ تم حفظ الجلسة بنجاح.")

        # 3. التوجه للرابط المستهدف
        print(f"🚀 معالجة الرابط: {target_url}")
        driver.get(target_url)
        time.sleep(random.uniform(5, 8))
        
        # 4. محاكاة الضغط على زر المتابعة
        follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        follow_btn.click()
        print(f"✔️ تمت المهمة بنجاح للحساب: {target_url}")

    except Exception as e:
        print(f"❌ خطأ أثناء التنفيذ: {e}")
    finally:
        driver.quit()

def start():
    """سحب الطلبات من API الموقع والبدء في المعالجة"""
    print(f"📡 جاري الاتصال بـ API الموقع: {API_URL}")
    try:
        response = requests.get(API_URL, timeout=20)
        if response.status_code == 200:
            data = response.json()
            orders = data.get("orders", [])
            
            if not orders:
                print("😴 لا توجد طلبات جديدة في قاعدة البيانات حالياً.")
                return

            print(f"✅ تم العثور على ({len(orders)}) طلبات جديدة.")

            # قراءة الحسابات المحلية
            if not os.path.exists("accounts.txt"):
                print("❌ خطأ: ملف accounts.txt غير موجود!")
                return

            with open("accounts.txt", "r") as f:
                accounts = [l.strip().split(":") for l in f if ":" in l]

            for url in orders:
                for user, pw in accounts:
                    run_bot(url, user, pw)
                    print("💤 انتظار أمني بين الحسابات...")
                    time.sleep(random.randint(10, 20))
        else:
            print(f"❌ فشل السحب. كود الحالة من السيرفر: {response.status_code}")
    except Exception as e:
        print(f"⚠️ خطأ في الاتصال بالشبكة: {e}")

if __name__ == "__main__":
    start()
