import os
import time
import pickle
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GH_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

def get_orders():
    url = f"https://api.github.com{REPO}/issues?state=open"
    headers = {"Authorization": f"token {GH_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def run_bot_with_cookies(target_url):
    options = uc.ChromeOptions()
    options.add_argument('--headless') # ضروري داخل جيت هاب
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 25)
    
    try:
        # 1. الدخول لموقع تيك توك أولاً لتهيئة النطاق
        driver.get("https://www.tiktok.com")
        time.sleep(5)
        
        # 2. تحميل الكوكيز (تخطي تسجيل الدخول والكابتشا)
        if os.path.exists("cookies.pkl"):
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("🍪 تم حقن الكوكيز بنجاح.")
            driver.refresh()
            time.sleep(5)

        # 3. التوجه للرابط ورشقه
        driver.get(target_url)
        print(f"🚀 معالجة الرابط: {target_url}")
        
        follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        follow_btn.click()
        print("✅ تمت المتابعة بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    orders = get_orders()
    if orders:
        for issue in orders:
            run_bot_with_cookies(issue["body"].strip())
            # إغلاق الـ Issue
            requests.patch(f"https://api.github.com{REPO}/issues/{issue['number']}", 
                           headers={"Authorization": f"token {GH_TOKEN}"}, 
                           json={"state": "closed"})

