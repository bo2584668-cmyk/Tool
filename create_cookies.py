import undetected_chromedriver as uc
import pickle
import time
import os

def create_session():
    options = uc.ChromeOptions()
    # لا نستخدم headless هنا لأننا نريد حل الكابتشا يدوياً
    driver = uc.Chrome(options=options)
    
    print("🌐 جاري فتح تيك توك... سجل دخولك الآن وحل الكابتشا يدوياً.")
    driver.get("https://www.tiktok.com")
    
    # انتظر حتى تقوم أنت بتسجيل الدخول بنجاح (معك دقيقتان)
    print("⏳ أمامك 120 ثانية لتنفيذ الدخول...")
    time.sleep(120)
    
    # حفظ الكوكيز بعد الدخول
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)
    
    print("✅ تم حفظ ملف cookies.pkl بنجاح! ارفع هذا الملف الآن إلى جيت هاب.")
    driver.quit()

if __name__ == "__main__":
    create_session()

