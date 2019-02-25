from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
import traceback
from time import sleep
driver = webdriver.Chrome("c:/driver/chromedriver.exe")
try:
    # サイトにアクセス
    driver.get("https://pairs.lv/")
    # ログインボタンが表示されるまで待機＆取得
    elem_register_btn = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, "registerBtn1"))
    )
    # ログインボタンを押す
    elem_register_btn.click()
    # windowが増えたことを確認
    element = WebDriverWait(driver, 100).until(
        EC.number_of_windows_to_be(2)
    )
    # 全てのウィンドウハンドルを取得
    allHandles = driver.window_handles
    # windowハンドルの切り替え
    driver.switch_to_window(allHandles[1])
    # fbのメールアドレスが表示されるまで待機＆取得
    elem_email_textbox = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#email"))
    )
    # fbのメールアドレス、パスワードを入力
    elem_email_textbox.send_keys("IDに書き換えてください)
    elem_pass_textbox = driver.find_element_by_id("pass")
    elem_pass_textbox.send_keys("パスワードに書き換えてください")
    # fbログインボタンを押す
    elem_fb_login = driver.find_element_by_id("u_0_0")
    elem_fb_login.click()

    # windowハンドルの切り替え
    driver.switch_to_window(allHandles[0])

    #キャンペーンモーダルが表示されたら閉じるボタンを押して消す
    elem_campain_close_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//a[@id = 'welcome_close_button']"))
    )
    if elem_campain_close_btn:
        elem_campain_close_btn.click()

    # 無料いいね*4のモーダルが表示されることを確認
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.button_like"))
    )
    # 無料いいね*4が完了するまでループ
    isFinishedFreeLike = False
    while not isFinishedFreeLike:
        try:
            # aタグが表示されるまで待機＆取得
            elem_free_likebtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                "//div[contains(@class, 'box_modal_window_inner')]//span[not(contains(@class, 'ng-hide'))]/a[contains(@class, 'button_like') and not(contains(@class, 'button_mitene')) and not (contains(@class, 'button_like_review'))]"))
            )
            # いいねボタンを押す
            elem_free_likebtn.click()
            # 個別のモーダルが表示されるまで待機
            elem_free_likebtn2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                "//div[@id='like_modal_area']/div[@class='box_modal_window_inner']/div[contains(@class, 'modal_button_area')]/a[contains(@class, 'button_like_b')]"))
            )
            # 個別のいいねボタンを押す
            elem_free_likebtn2.click()
            # 質問文が表示された場合適当な文章を入力する
            elem_question_textbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                "//p[contains(@class, 'form_item')]/input"))
            )
            if elem_question_textbox :
                # 回答を入力
                elem_question_textbox.send_keys("わからない")
                # OKを押す
                elem_ok_btn = driver.find_element_by_xpath(
                    "//div[contains(@class, 'modal_button')]/div[contains(@class, 'common_button_area')]/ul/li/a[contains(@class, 'button_blue_a')]"
                )
                elem_ok_btn.click()
                # いいねを取得して押す
                elem_like_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                            "//div[contains(@id, 'like_question_answer_modal')]//a[contains(@class, 'button_like_b')]"))
                )
                elem_like_btn.click()
            # 読み込むのを待つ 本来ならばクリッカブルで拾えるはずなのだが、モーダルの読み込みが上にかぶさっていてクリックできない
            sleep(5)
        except (NoSuchElementException, ElementNotVisibleException, TimeoutException):
            traceback.print_exc()
            print('エレメント取得できませんでした')
            isFinishedFreeLike = True

    # 無料いいねを押すのが終わったらモーダルを閉じる
    elem_modal_close = driver.find_element_by_xpath(
        "//div[contains(@class, 'box_modal_window') and contains(@class, 'pickup_modal')]/div[contains(@class, 'box_modal_window_inner')]/a[contains(@class, 'modal_close')]"
    )
    elem_modal_close.click()

    #１０００人に到達するまで繰り返す（足跡間隔はランダムで5〜10秒の間）
    # 開始番号と終わる番号をランダムにする
    I = random.randint(0,2000)
    footprints_num = random.randint(500,1000)
    END = I + footprints_num
    # 開始の人のページに移動
    src= "https://pairs.lv/#/search/one/%s"%str(I)
    driver.get(src)
    while I < END:
        I=I+1
        # 次へボタンを取得してクリック
        elem_next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//li[contains(@class, 'action_pager_next') and not(contains(@class, 'ng-hide'))]/a"))
        )
        # いいね数が500+だった場合お気に入りにいれる

        elem_next_btn.click()
        # 1秒から4秒ランダムに待つ
        sleep(random.randint(1,3))
    print(str(footprints_num) + "人に足跡を付けました")
except Exception:
    traceback.print_exc()
#driver.close()