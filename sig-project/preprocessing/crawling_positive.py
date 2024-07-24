from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd

def setup_driver(): # Chrome Options 설정
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    options.add_argument(f'user-agent={user_agent}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_game_links(driver, url): 
    driver.get(url)
    time.sleep(1)
    game_links = []
    game_elements = driver.find_elements(By.CSS_SELECTOR, 'a.c-finderProductCard_container.g-color-gray80.u-grid')
    game_links = [elem.get_attribute('href') for elem in game_elements]
    return game_links
    
def navigate_to_game_page(driver, game_link):  
    driver.get(game_link)
    time.sleep(1)
    print('해당 게임 접속 성공')

def get_game_name(driver): # 게임 이름 얻어오기
    game_name_element = driver.find_element(By.CSS_SELECTOR, 'div.c-productHero_title.g-inner-spacing-bottom-medium.g-outer-spacing-top-medium > h1')
    game_name = game_name_element.text.strip()
    return game_name

def navigate_to_review_page(driver): # 해당 게임리뷰페이지 접속
    try:
        review_link = driver.find_element(By.CSS_SELECTOR, 'div.c-reviewsSection_seeAllButton.g-bg-gray80.u-text-center.g-outer-spacing-top-medium > a')
        review_link.click()
        time.sleep(1)
        current_url = driver.current_url
        filtered_url = current_url + "&filter=Positive%20Reviews"
        driver.get(filtered_url)
        time.sleep(1)
        print('해당 게임 유저 리뷰 접속 성공')
        return True
    
    except NoSuchElementException:
        print('리뷰 링크가 없습니다.')
        return False

def scroll_to_load_reviews(driver): # 스크롤
    scroll_location = 0
    new_reviews_loaded = True

    while new_reviews_loaded:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        current_review_count = len(driver.find_elements(By.CSS_SELECTOR, 'div.c-pageProductReviews_row.g-outer-spacing-bottom-xxlarge > div'))
        if scroll_location == current_review_count:
            new_reviews_loaded = False
        else:
            scroll_location = current_review_count

def extract_reviews(driver): # 긍정 리뷰 이동 후 리뷰추출
    review_list = []

    divs = driver.find_elements(By.CSS_SELECTOR, 'div.c-pageProductReviews_row.g-outer-spacing-bottom-xxlarge > div')
    for div in divs:
        review_info = {}
        try:
            # StaleElementReferenceException 예외가 발생할 경우 다시 시도
            while True:
                try:
                    user_reviewbox = div.find_element(By.CLASS_NAME, 'c-siteReviewHeader')
                    break
                except StaleElementReferenceException:
                    time.sleep(2)
                    div = driver.find_element(By.CSS_SELECTOR, 'div.c-pageProductReviews_row.g-outer-spacing-bottom-xxlarge > div')
                    
            user_name = user_reviewbox.find_element(By.CLASS_NAME, 'c-siteReviewHeader_username').text
            review_info['user_name'] = user_name
            review_text = div.find_element(By.CSS_SELECTOR, 'div.c-siteReview_quote span').text
            review_info['review_text'] = review_text
            review_list.append(review_info)
        except NoSuchElementException:
            continue
    return review_list

def to_nextpage(driver):    #다음 페이지로 넘어가기
    try:
        next_page_element = driver.find_element(By.CSS_SELECTOR, 'span.c-navigationPagination_item.c-navigationPagination_item--next.enabled')
        next_page_element.click()
        time.sleep(1)
        print("다음 페이지로 넘어갑니다.")
        return True
    except NoSuchElementException:
        print('마지막 페이지입니다.')
        return False

def main(): # 실행
    driver = setup_driver()
    game_review_data = []

    url = "https://www.metacritic.com/browse/game/"

    b = True
    while b:
        game_links = get_game_links(driver, url)

        for game_link in game_links:
            navigate_to_game_page(driver, game_link)
            game_name = get_game_name(driver)
            game_info = {'game_name': game_name}
            
            if not navigate_to_review_page(driver): #리뷰가 없는 게임
                game_info['reviews'] = '-'
                print("리뷰가 없는 게임")
                game_review_data.append(game_info)
                continue
            else:
                scroll_to_load_reviews(driver)
                reviews = extract_reviews(driver)
                game_info['reviews'] = reviews
                game_review_data.append(game_info)
        
        driver.get(url)
        time.sleep(3)
        b = to_nextpage(driver)
        url = driver.current_url

    
    driver.quit()

     # CSV 파일로 저장
    data = []
    for game in game_review_data:
        game_name = game['game_name']
        reviews = game['reviews']
        if reviews == '-':
            data.append([game_name, '-', '-'])
        else:
            for review in reviews:
                data.append([game_name, review['user_name'], review['review_text']])
    
    df = pd.DataFrame(data, columns=['Game Name', 'User Name', 'Review Text'])
    df.to_csv('game_reviews.csv', index=False, encoding='utf-8-sig')

    print("CSV 파일 저장 완료")
    print(game_review_data)

if __name__ == "__main__":
    main()
