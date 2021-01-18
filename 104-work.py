from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import os


chrome_options = Options()
chrome_options.add_argument('--disable-gpu')                         #google文件提到需要加上這個屬性來規避bug
chrome_options.add_argument('--hide-scrollbars')                     #隱藏滾動條, 應對一些特殊頁面
chrome_options.add_argument('blink-settings=imagesEnabled=false')    #不載入圖片, 提升速度
chrome_options.add_argument('--headless')                            #瀏覽器不提供視覺化頁面
driver = webdriver.Chrome(options=chrome_options)
driver1 = webdriver.Chrome(options=chrome_options)

url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E8%B3%87%E6%96%99%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page=2&mode=s&jobsource=2018indexpoc'

if not os.path.exists('./104works'):
    os.mkdir('./104works')


driver.get(url)         #取得原始網頁

n=50
for i in range(0,n):
    driver.execute_script('var s = document.documentElement.scrollTop=1000000')      #模擬滾動頁面
    time.sleep(3)


    html = driver.page_source                  #source能抓到網頁原始碼
    soup = BeautifulSoup(html,'html.parser')

    alldata =[]
    for jobs in soup.select('article.js-job-item'):

        job_urls = jobs.select('a.js-job-link')
        for i in job_urls:
            job_url = "https:" + i["href"]
            # print(job_url)  # 職缺網址
            title = i.text
            # print(title)  # 職缺

            driver1.get(job_url)
            time.sleep(2)  # delay一段時間等待網頁更新完成
            html = driver1.page_source
            soup1 = BeautifulSoup(html, 'html.parser')
            # print(soup1)
            try:
                com_name = soup1.select_one('a[class="btn-link t3 mr-6"]').text.replace(" ",'')     # 公司名稱
                # print(com_name)
                work_list = soup1.find('div', class_='col main').find('p', class_='mb-5 r3 job-description__content text-break').text.replace(" ",'')    # 工作內容
                # print(work_list)
                work_list1 = soup1.select('div[class="trigger"]')
                # print("職務類別:", work_list1[0].text, work_list1[1].text, work_list1[2].text)
                position = work_list1[0].text
                position += " %s" % (work_list1[1].text)
                position += " %s" % (work_list1[2].text)
                position += " %s" % (work_list1[3].text)
                # print(position)                            # 職務類別
                work_sal = soup1.find('div', class_='col main').find('p', class_='t3 mb-0 mr-2 monthly-salary text-primary font-weight-bold float-left').text.replace(" ",'')
                # print("工作待遇:",work_sal)     #工作待遇
                work_list2 = soup1.select('p[class="t3 mb-0"]')
                # print(work_inf)
                # print("工作性質:", work_list2[0].text.replace(" ", ''))      #工作性質
                # print("工作地點:", work_list2[1].text.replace(" ", ''))      #工作地點
                # print("管理責任:", work_list2[2].text.replace(" ", ''))      #工作性質
                # print("出差外派:", work_list2[3].text.replace(" ", ''))      #管理責任
                # print("上班時段:", work_list2[4].text.replace(" ", ''))      #上班時段
                # print("上班時段:", work_list2[5].text.replace(" ", ''))      #上班時段
                # print("可上班日:", work_list2[6].text.replace(" ", ''))      #可上班日
                # print("需求人數:", work_list2[7].text.replace(" ", ''))      #需求人數

                work_inf = soup1.select('div[class="col p-0 job-requirement-table__data"]')
                # print("接受身份:", work_inf[0].text.replace(" ", ''))        #接受身份
                # print("工作經歷:", work_inf[1].text.replace(" ", ''))        #工作經歷
                # print("學歷要求:", work_inf[2].text.replace(" ", ''))        #學歷要求
                # print("科系要求:", work_inf[3].text.replace(" ", ''))        #科系要求
                # print("語文條件:", work_inf[4].text.replace(" ", ''))        #語文條件
                # print("擅長工具:", work_inf[5].text.replace(" ", ''))        #擅長工具
                # print("工作技能:", work_inf[6].text.replace(" ", ''))        #工作技能
                # print("其他條件:", work_inf[7].text.replace(" ", ''))        #其他條件
                work_bonus = soup1.select('p[class="r3 mb-0 text-break"]')[0].text
                # print("福利:\n",work_bonus)
                #
                # title += "\n聯絡網址: %s ," % (job_url)
                # title += "公司名稱: %s ," % (com_name)
                # title += "工作內容: %s ," % (work_list)
                # title += "職務類別: %s ," % (position)
                # title += "工作待遇: %s ," % (work_sal)
                nature = "%s" % (work_list2[0].text.replace(" ", ''))
                loc = "%s" % (work_list2[1].text.replace(" ", ''))
                responsibility = "%s" % (work_list2[2].text.replace(" ", ''))
                worktrip = "%s" % (work_list2[3].text.replace(" ", ''))
                worktime = "%s" % (work_list2[4].text.replace(" ", ''))
                workbreak = "%s" % (work_list2[5].text.replace(" ", ''))
                workdate = "%s" % (work_list2[6].text.replace(" ", ''))
                need = "%s" % (work_list2[7].text.replace(" ", ''))
                Identity = "%s" % (work_inf[0].text.replace(" ", ''))
                exp = "%s" % (work_inf[1].text.replace(" ", ''))
                Education = "%s" % (work_inf[2].text.replace(" ", ''))
                dep = "%s" % (work_inf[3].text.replace(" ", ''))
                Language = "%s" % (work_inf[4].text.replace(" ", ''))
                tool = "%s" % (work_inf[5].text.replace(" ", ''))
                skill = "%s" % (work_inf[6].text.replace(" ", ''))
                other = "%s" % (work_inf[7].text.replace(" ", ''))
                # title += "福利:\n %s" % (work_bonus)
                # print(type(title))

                data = {
                    '職缺':title,'聯絡網址':job_url,'公司名稱':com_name,'工作內容':work_list,'職務類別':position,
                    '工作待遇':work_sal,'工作性質':nature,'工作地點':loc,'管理責任':responsibility,'出差外派':worktrip,
                    '上班時段':workdate,'休假制度':workbreak,'可上班日':workdate,'需求人數':need,'接受身份':Identity,
                    '工作經歷':exp,'學歷要求':Education,'科系要求':dep,'語文條件':Language,'擅長工具':tool,'工作技能':skill,
                    '其他條件':other,'福利':work_bonus
                }
                print(data)

                print('=' * 50)
                alldata.append(data)
                try:
                    fn = '104workall.csv'
                    # 設定csv檔欄位
                    columnsname = [
                        '職缺', '聯絡網址', '公司名稱', '工作內容', '職務類別', '工作待遇', '工作性質', '工作地點', '管理責任',
                        '出差外派', '上班時段', '休假制度', '可上班日', '需求人數', '接受身份', '工作經歷', '學歷要求', '科系要求',
                        '語文條件', '擅長工具', '工作技能', '其他條件', '福利'
                    ]
                     #用 newline讓它自動換行寫入data
                    with open('./104works/all.csv', 'w', newline='',encoding='utf-8') as csvFile:

                        writer = csv.DictWriter(csvFile, fieldnames=columnsname)
                        writer.writeheader()
                        for data in alldata:       #用for迴圈重複寫入不同data
                            writer.writerow(data)
                except PermissionError:
                    pass
                # driver1.close()
            except AttributeError:
                pass
            except IndexError:
                pass
            except UnicodeEncodeError:
                pass
# driver.close()


