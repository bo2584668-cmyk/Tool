import os
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# جلب البيانات من بيئة GitHub
GH_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")

def get_orders():
    url = f"https://api.github.com{REPO}/issues?state=open"
    headers = {"Authorization": f"token {GH_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def run_bot(target_url, user, pw):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    try:
        driver.get("https://www.tiktok.com")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(user)
        driver.find_element(By.NAME, "password").send_keys(pw)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(15) # وقت لحل الكابتشا آلياً
        driver.get(target_url)
        time.sleep(5)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Follow') or contains(., 'متابعة')]")))
        btn.click()
        print(f"✅ تمت المتابعة بواسطة {user}")
    finally:
        driver.quit()

if __name__ == "__main__":
    issues = get_orders()
    if issues:
        with open("accounts.txt", "r") as f:
            accounts = [line.strip().split(":") for line in f if ":" in line]
        for issue in issues:
            target = issue["body"].strip()
            print(f"🚀 بدء التنفيذ للرابط: {target}")
            for u, p in accounts:
                run_bot(target, u, p)
            # إغلاق الـ Issue بعد التنفيذ
            requests.patch(f"https://api.github.com{REPO}/issues/{issue['number']}", 
                           headers={"Authorization": f"token {GH_TOKEN}"}, json={"state": "closed"})
