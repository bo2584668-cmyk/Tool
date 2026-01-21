import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- إعدادات الربط بموقعك ---
# تأكد أنك أضفت مسار /api/get_orders في ملف flask_app.py كما شرحنا سابقاً
API_URL = "https://wwwwww.pythonanywhere.com"

def run_bot(target_url, username, password):
    options = uc.ChromeOptions()
    options.add_argument('--headless') # ضروري للعمل على سيرفرات GitHub
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = uc.Chrome(options=options)
        driver.get("https://www.tiktok.com")
        
        wait = WebDriverWait(driver, 20)
        # تسجيل الدخول
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(15) # انتظار تسجيل الدخول (فحص أمني)

        # تنفيذ المتابعة للرابط المطلوب
        driver.get(target_url)
        time.sleep(5)
        follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        follow_btn.click()
        print(f"✅ نجاح: {username} تابع {target_url}")
        
    except Exception as e:
        print(f"❌ خطأ مع الحساب {username}: {e}")
    finally:
        if driver:
            driver.quit()

def start():
    print("📡 جاري سحب الطلبات من الموقع...")
    try:
        response = requests.get(API_URL)
        data = response.json()
        orders = data.get("orders", [])

        if not orders:
            print("😴 لا توجد طلبات جديدة.")
            return

        # قراءة الحسابات من الملف
        with open("accounts.txt", "r") as f:
            accounts = [line.strip().split(":") for line in f if ":" in line]

        for url in orders:
            print(f"🚀 بدء تنفيذ الطلب للرابط: {url}")
            for user, pw in accounts:
                run_bot(url, user, pw)
                time.sleep(5) # فاصل زمني بسيط بين الحسابات
                
    except Exception as e:
        print(f"⚠️ فشل الاتصال بالسيرفر: {e}")

if __name__ == "__main__":
    start()

