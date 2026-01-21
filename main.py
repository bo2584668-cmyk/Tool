import os
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# إعدادات جيت هاب (يتم سحبها آلياً من النظام)
GH_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

def get_orders():
    """جلب الروابط من الـ Issues المفتوحة"""
    url = f"https://api.github.com{REPO}/issues?state=open"
    headers = {"Authorization": f"token {GH_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def run_bot(target_url, user, pw):
    """تنفيذ عملية المتابعة"""
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 25)
    try:
        driver.get("https://www.tiktok.com")
        # تسجيل الدخول
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(user)
        driver.find_element(By.NAME, "password").send_keys(pw)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(20) # وقت للفحص الأمني
        
        # تنفيذ المتابعة
        driver.get(target_url)
        time.sleep(5)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        btn.click()
        print(f"✅ تمت المتابعة بنجاح بواسطة: {user}")
    except Exception as e:
        print(f"❌ فشل الحساب {user}")
    finally:
        driver.quit()

if __name__ == "__main__":
    issues = get_orders()
    if issues:
        # قراءة الحسابات من ملف accounts.txt
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as f:
                accounts = [line.strip().split(":") for line in f if ":" in line]
            
            for issue in issues:
                target = issue["body"].strip()
                print(f"🚀 معالجة الطلب: {target}")
                for u, p in accounts:
                    run_bot(target, u, p)
                
                # إغلاق التذكرة بعد الانتهاء
                requests.patch(f"https://api.github.com{REPO}/issues/{issue['number']}", 
                               headers={"Authorization": f"token {GH_TOKEN}"}, 
                               json={"state": "closed", "body": "✅ تم التنفيذ بنجاح 2026"})
    else:
        print("😴 لا توجد طلبات جديدة.")
