import requests
import time
import os

# --- الإعدادات الصحيحة ---
API_TOKEN = "91dfc2c16166d66229fd845f056a8fcf89c9debe"
USERNAME = "wwwwww"
# المسار الصحيح للملف عبر API المنصة
FILE_URL = f"https://www.pythonanywhere.com{USERNAME}/files/path/home/{USERNAME}/orders.txt"

def get_orders():
    print("📡 جاري فحص ملف الطلبات عبر API الخاص بـ PythonAnywhere...")
    headers = {'Authorization': f'Token {API_TOKEN}'}
    
    try:
        # 1. طلب محتوى الملف
        response = requests.get(FILE_URL, headers=headers)
        
        if response.status_code == 200:
            content = response.text.strip()
            if not content:
                print("😴 الملف فارغ، لا توجد طلبات جديدة.")
                return []
            
            orders = content.split('\n')
            print(f"✅ تم العثور على {len(orders)} طلبات.")
            
            # 2. مسح الملف بعد القراءة (إرسال محتوى فارغ لكي لا يتكرر الرشق)
            empty_data = {'content': ''}
            requests.post(FILE_URL, headers=headers, files=empty_data)
            
            return [o.strip() for o in orders if o.strip()]
        
        elif response.status_code == 404:
            print("❌ خطأ: ملف orders.txt غير موجود. تأكد أن أحداً قد طلب من موقعك أولاً.")
            return []
        else:
            print(f"⚠️ فشل الاتصال: كود الحالة {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ حدث خطأ تقني: {e}")
        return []

def run_bot(url):
    # هنا تضع كود السيلينيوم (Selenium) الذي كتبناه سابقاً
    print(f"🚀 جاري الآن رشق الرابط: {url}")
    # (تأكد من إضافة كود undetected_chromedriver هنا)

if __name__ == "__main__":
    orders_list = get_orders()
    if orders_list:
        for link in orders_list:
            run_bot(link)
            time.sleep(5)
    print("🏁 انتهت العملية.")
