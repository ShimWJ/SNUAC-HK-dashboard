import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 내 스트림릿 주소 (본인의 주소로 수정하세요!)
URL = "https://snuac-hk-dashboard.streamlit.app/"

def wake_streamlit():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 화면 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"접속 시도 중: {URL}")
        driver.get(URL)
        time.sleep(10)  # 페이지 로딩 대기

        # "Yes, get this app back up!" 버튼 찾기
        # 이 버튼의 텍스트나 구조가 바뀌어도 대응하도록 'Wake'라는 단어를 포함한 버튼을 찾습니다.
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if "Wake" in btn.text or "back up" in btn.text:
                btn.click()
                print("성공: 슬립 모드 해제 버튼을 눌렀습니다!")
                time.sleep(5)
                break
        else:
            print("알림: 슬립 모드가 아니거나 버튼을 찾지 못했습니다.")
            
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    wake_streamlit()
