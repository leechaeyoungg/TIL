from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1920x1080')
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")

# 브라우저 실행
driver = webdriver.Chrome(options=options)

# Google 접속
logger.info("Navigating to Google...")
driver.get("https://www.google.com")

# 'manure' 검색
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("manure")
search_box.submit()

# 이미지 탭 클릭
logger.info("Clicking on the Images tab...")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "이미지"))).click()

# 이미지 저장 폴더 설정
output_dir = "D:\\manure_images3"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 스크롤하여 페이지의 모든 이미지 로드
logger.info("Scrolling down the page...")
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

logger.info("Taking a screenshot after scrolling.")
driver.save_screenshot('post_scroll_screenshot.png')

# 이미지 크롤링 시작
logger.info("Starting to crawl images...")
downloaded_images = set()

try:
    thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')
    logger.info(f"Found {len(thumbnails)} thumbnails.")
    
    for index, thumbnail in enumerate(thumbnails):
        try:
            logger.info(f"Clicking thumbnail {index + 1}")
            thumbnail.click()

            # 큰 이미지 로드 대기 및 가져오기
            large_image_xpath = '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]'
            try:
                large_image = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, large_image_xpath))
                )
                src = large_image.get_attribute("src")

                # 썸네일 URL을 제외하도록 조건 추가
                if "http" in src and "encrypted-tbn0.gstatic.com" not in src and src not in downloaded_images:
                    # 이미지 다운로드
                    img_data = requests.get(src).content
                    img_name = os.path.join(output_dir, f"image_{index + 1}.jpg")
                    with open(img_name, 'wb') as handler:
                        handler.write(img_data)
                    
                    downloaded_images.add(src)
                    logger.info(f"Downloaded image {index + 1}: {src}")
                else:
                    logger.info(f"Image {index + 1} already downloaded or skipped due to domain, skipping.")

                # 로그인 창 등 팝업이 발생했을 경우 예외 처리
                if "로그인" in driver.page_source:
                    logger.info("Login page detected, skipping to next image.")
                    continue
                
                # 다음 썸네일을 클릭하기 전에 약간의 대기 시간 추가
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error clicking or downloading image {index + 1}: {e}")
                continue  # 다음 썸네일로 계속 진행
        except Exception as e:
            logger.error(f"Error during processing: {e}")
            continue

finally:
    logger.info("Closing the browser.")
    driver.quit()

