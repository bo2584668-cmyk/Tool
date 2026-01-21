import time
import requests
import pickle
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. إعدادات المسارات
ORDER_FILE_URL = "https://www.pythonanywhere.com/user/wwwwww/shares/997658e3d18e4497a46147634dca7b90/"
COOKIE_FILE = "tiktok_session.pkl"

def get_driver(show_browser=True):
    options = uc.ChromeOptions()
    if not show_browser:
        options.add_argument('--headless')
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # هوية متصفح طبيعية لعام 2026
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    return driver

def run_bot(target_url, username, password):
    # تشغيل المتصفح في الوضع المرئي لحل الكابتشا يدوياً
    driver = get_driver(show_browser=True)
    wait = WebDriverWait(driver, 30)
    
    try:
        driver.get("https://www.tiktok.com")
        
        # إذا كان هناك ملف كوكيز قديم، نحاول تحميله لتخطي تسجيل الدخول
        if os.path.exists(COOKIE_FILE):
            print("🍪 جاري محاولة تحميل الجلسة السابقة...")
            cookies = pickle.load(open(COOKIE_FILE, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(5)

        # التحقق إذا كنا ما زلنا في صفحة الدخول (يعني نحتاج تسجيل دخول)
        if "login" in driver.current_url:
            print(f"👤 جاري إدخال بيانات الحساب: {username}")
            wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
            driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            print("⚠️ تنبيه: إذا ظهرت كابتشا، قم بحلها الآن يدوياً بالماوس...")
            # وقت كافٍ (60 ثانية) لكي تقوم أنت بحل الكابتشا يدوياً
            time.sleep(60) 
            
            # حفظ الجلسة بعد النجاح في الدخول
            pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
            print("✅ تم حفظ الجلسة (Cookies) لتسهيل الدخول المرة القادمة.")

        # التوجه لرابط الرشق
        print(f"🚀 التوجه للرابط المستهدف: {target_url}")
        driver.get(target_url)
        time.sleep(7)
        
        # الضغط على متابعة
        follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        follow_btn.click()
        print(f"✔️ تمت المتابعة بنجاح بواسطة {username}")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
    finally:
        driver.quit()

def start():
    print("📡 جاري فحص ملف الأوردرات المشترك...")
    try:
        response = requests.get(ORDER_FILE_URL)
        if response.status_code == 200:
            orders = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            if not orders:
                print("😴 لا توجد طلبات جديدة.")
                return

            # قراءة الحسابات من ملف accounts.txt
            with open("accounts.txt", "r") as f:
                accounts = [l.strip().split(":") for l in f if ":" in l]

            for url in orders:
                for user, pw in accounts:
                    run_bot(url, user, pw)
                    print("💤 انتظار قصير قبل الحساب التالي...")
                    time.sleep(10)
        else:
            print("❌ فشل الوصول للملف المشترك.")
    except Exception as e:
        print(f"⚠️ خطأ عام: {e}")

if __name__ == "__main__":
    start()
