from selenium import webdriver
import sys
import mysql.connector
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
def crawling():
    # Chrome Options 설정 (User-Agent 추가)
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

# WebDriver 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

# 페이지로 이동
    url = "https://www.metacritic.com/browse/game/"
    driver.get(url)

    # 게임 페이지로 이동
    game_link = driver.find_element(By.CSS_SELECTOR, 'a.c-finderProductCard_container.g-color-gray80.u-grid')
    game_link.click()
    time.sleep(15)  # 페이지가 로드될 때까지 잠시 기다립니다.
    print('해당 게임 접속 성공')

    game_name_element = driver.find_element(By.CSS_SELECTOR, 'div.c-productHero_title.g-inner-spacing-bottom-medium.g-outer-spacing-top-medium > h1')
    game_name = game_name_element.text.strip()

    game_review_data = []

    game_info = {}
    game_info['game_name'] = game_name
    print(game_info)

    # 유저 리뷰 페이지로 이동
    try:
        review_link = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[4]/div/div[7]/div/div[2]/a')
        review_link.click()
        time.sleep(1)
        print('해당 게임 유저 리뷰 접속 성공')

    except NoSuchElementException:
        print('리뷰 링크가 없습니다.')
        driver.quit()
        sys.exit()
        
    # 스크롤 내리기 이동 전 위치
    scroll_location = 0
    new_reviews_loaded = True

    while new_reviews_loaded:
        # 현재 스크롤의 가장 아래로 내림
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # 전체 스크롤이 늘어날 때까지 대기
        time.sleep(5)
        # 현재 페이지의 리뷰 수 확인
        current_review_count = len(driver.find_elements(By.CSS_SELECTOR, 'div.c-pageProductReviews_row.g-outer-spacing-bottom-xxlarge > div'))
        # 이전 스크롤에서 새로운 리뷰가 추가되지 않았으면 종료
        if scroll_location == current_review_count:
            new_reviews_loaded = False
        else:
            scroll_location = current_review_count

    # 리뷰를 저장할 리스트 초기화
    review_list = []

    # 리뷰에서 div 태그들을 가져오기
    divs = driver.find_elements(By.CSS_SELECTOR, 'div.c-pageProductReviews_row.g-outer-spacing-bottom-xxlarge > div')

    for div in divs:
        review_info = {}
        user_reviewbox = div.find_element(By.CLASS_NAME, 'c-siteReviewHeader')
        user_name = user_reviewbox.find_element(By.CLASS_NAME, 'c-siteReviewHeader_username').text
        review_info['user_name'] = user_name
        
        # 리뷰 텍스트 추출
        review_text = div.find_element(By.CSS_SELECTOR, 'div.c-siteReview_quote span').text
        review_info['review_text'] = review_text
        
        review_list.append(review_info)
        
    game_info['reviews'] = review_list
    game_review_data.append(game_info)

    print('크롤링 완료')

    driver.quit()
    return game_review_data
