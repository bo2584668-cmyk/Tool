import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# --- إعدادات PythonAnywhere API ---
API_TOKEN = "91dfc2c16166d66229fd845f056a8fcf89c9debe"
USERNAME = "wwwwww"
# رابط الملف مباشرة عبر API المنصة
FILE_URL = f"https://www.pythonanywhere.com{USERNAME}/files/path/home/{USERNAME}/orders.txt"

def get_orders_via_api():
    print("📡 جاري سحب الطلبات باستخدام API Key...")
    headers = {'Authorization': f'Token {API_TOKEN}'}
    try:
        response = requests.get(FILE_URL, headers=headers)
        if response.status_code == 200:
            content = response.text
            orders = content.strip().split('\n')
            
            # مسح محتوى الملف بعد القراءة (إرسال نص فارغ)
            requests.set(FILE_URL, headers=headers, files={'content': ''}) 
            
            return [o.strip() for o in orders if o.strip()]
        return []
    except Exception as e:
        print(f"❌ خطأ في الـ API: {e}")
        return []

def run_bot(url):
    # كود السيلينيوم الخاص بك هنا (نفس الكود القديم)
    print(f"🚀 جاري رشق الرابط: {url}")
    # ... (باقي كود الرشق)

if __name__ == "__main__":
    orders = get_orders_via_api()
    if orders:
        for order_url in orders:
            run_bot(order_url)
    else:
        print("😴 لا توجد طلبات جديدة.")
