import time

import re
import xlwings
from selenium import webdriver
from selenium.webdriver.common.by import By

book_obj = xlwings.App()
book = xlwings.books.active
book.save('福大教务处通知.xlsx')
sheet = book.sheets[0]
sheet.range('a1').value = '福大教务处通知(展示前100条)'
for i in range(1, 3):
    sheet.range('a%d:g%d' % (i, i)).api.Merge()
    sheet.range('a%d' % i).api.HorizontalAlignment = -4108
titles = ['日期', '通知人', '标题', '详情链接', '附件名', '附件下载次数', '附件链接']
sheet.range('a3').value = titles

option = webdriver.EdgeOptions()
option.add_argument("headless")
browser = webdriver.Edge(options=option)
browser.get(r'https://jwch.fzu.edu.cn/jxtz.htm')
time.sleep(2)

total_pages = browser.find_element(By.XPATH,
                                   '/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/div/span[1]/span[9]/a')
yeshu = int(total_pages.text)
html = total_pages.get_attribute('href')
total_pages.click()
time.sleep(2)
lis = browser.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/ul/li')

tiao = 0
for li in lis:
    tiao += 1
tiaoshu = 20 * (yeshu - 1) + tiao
sheet.range('a2').value = '共有%d页（%d条通知）' % (yeshu, tiaoshu)

for i in range(1, 6):  # 循环页数
    browser.find_element(By.ID, 'u7_goto').send_keys(i)
    time.sleep(2)
    click = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/div/span[5]/a')
    click.click()
    time.sleep(2)

    li = browser.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/ul/li')
    a = 4 + (i - 1) * 20
    for i in li:  # 循环通知
        ex0 = '\n【(.*?)】'
        i0 = re.split(ex0, i.text, re.S)
        # print(i0) #时间，通知人，标题
        sheet.range('a%d' % a).value = i0

        i1 = i.find_element(By.XPATH, './a')
        html = i1.get_attribute('href')
        i1.click()  # 循环详情页
        time.sleep(1)
        # print(html) #详情页地址
        sheet.range('d%d' % a).value = html

        browser.switch_to.window(browser.window_handles[-1])
        fujian = browser.find_elements(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/div[1]/div/ul/li')
        c1 = []
        c2 = []
        c3 = []
        g = []
        for i2 in fujian:
            ex1 = '附件【(.*?)】已下载(.*?)次'
            i3 = re.split(ex1, i2.text, re.S)  # 附件标题，次数
            i3 = [item.strip() for item in i3 if item.strip()]
            g += i3
            c1 += [g[-2]]
            c2 += [g[-1]]
            i4 = i2.find_element(By.XPATH, './a')
            i5 = (i4.get_attribute('href'))  # 附件下载地址
            c3 += [i5]
        sheet.range('e%d' % a).value = '\n'.join(c1)
        sheet.range('f%d' % a).value = '\n'.join(c2)
        sheet.range('g%d' % a).value = '\n'.join(c3)
        a += 1
        browser.switch_to.window(browser.window_handles[0])
sheet.autofit()
sheet.range('a:g').api.HorizontalAlignment = -4108
book.save()
# # book.close()
