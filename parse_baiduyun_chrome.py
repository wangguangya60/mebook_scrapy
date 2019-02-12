import httplib2
import xlrd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# 登录云盘
def login(driver,username,password):
    orgin_url = 'https://pan.baidu.com/'
    driver.get(orgin_url)
    time.sleep(5)
    elem_static = driver.find_element_by_id("TANGRAM__PSP_4__footerULoginBtn")
    elem_static.click()
    time.sleep(0.5)
    elem_username = driver.find_element_by_id("TANGRAM__PSP_4__userName")
    elem_username.clear()
    elem_username.send_keys(username)
    elem_userpas = driver.find_element_by_id("TANGRAM__PSP_4__password")
    elem_userpas.clear()
    elem_userpas.send_keys(password)
    elem_submit = driver.find_element_by_id("TANGRAM__PSP_4__submit")
    elem_submit.click()
    time.sleep(5)
# 将加密分享的文件保存到自己云盘的目录下[AA]
def extract(driver,srcurl,srcpwd,handle_suc,handle_fail):
    driver.get(srcurl)
    mark = 0
    try:
        #getpwd = driver.find_element_by_id("esDEV5")
        #getpwd = driver.find_element_by_id("xixp4Bk")
        try:
            getpwd = driver.find_element_by_id("zvbpPbMk")
            getpwd.send_keys(srcpwd)
        except NoSuchElementException as e:
            #print(e)
            getpwd = driver.find_element_by_id("eqqo3Jx")
            getpwd.send_keys(srcpwd)
        time.sleep(5)    
        getButton = driver.find_element_by_link_text("提取文件")
        getButton.click()
        time.sleep(8)
    #except NoSuchElementException:
    #    mark=0
	# 目前有两种情况
	# 一：分享文件是一压缩包
	# 二：分享的是一路径
        try:
            # 全选（情况二）
            selectall = driver.find_element_by_class_name("zbyDdwb") 
            selectall.click()
            time.sleep(5)
        except NoSuchElementException:
        #except:
        
            #file_name = "no_zbyDdwb.png"
            #driver.save_screenshot(file_name)
            #driver.get_screenshot_as_file(file_name)
            #handle_fail.write("%s,%s\n" %(srcurl,srcpwd))
        #mark = 0
            pass
        
        #else:
         #   handle_suc.write("%s,%s\n" %(srcurl,srcpwd))
    #try:
        savetodisk = driver.find_element_by_link_text("保存到网盘")
        savetodisk.click()
        time.sleep(5)
        ebook = driver.find_element_by_css_selector('span[node-path="/ebook"][class="treeview-txt"]')
        ebook.click()
        time.sleep(5)
    #except NoSuchElementException:
    #    mark=0
    #    pass
    #try:
        enter = driver.find_element_by_link_text("确定")
        enter.click()
        mark=1
        time.sleep(5)
    #except NoSuchElementException:
    #    mark=0
    #    pass
    #except NoSuchElementException:
    except:
        #file_name = "no_such_element.png"
        #driver.get_screenshot_as_file(file_name)
        #print(srcurl)
        #mark = 0
        pass
    if mark == 0:
        handle_fail.write("%s,%s\n" %(srcurl,srcpwd))
        handle_fail.flush()
    else:
        handle_suc.write("%s,%s\n" %(srcurl,srcpwd))
        handle_suc.flush()
# 从Excel中读取分享链接和提取密码（默认第一列是链接、第二列是提取密码）		
def read_excel(path):
    workbook = xlrd.open_workbook(path)
    sheet0=workbook.sheet_by_index(0);
    listUrl=[]
    listpwd=[]
    rownum=sheet0.nrows
    for index in range(rownum):
        listUrl.append(sheet0.cell(index,0).value.encode('utf-8'))
        listpwd.append(sheet0.cell(index,1).value.encode('utf-8'))
    return listUrl,listpwd
# 调用执行
def links_generator(filename):
    with open(filename,'r', encoding='UTF-8') as fh:
        for line in fh:
            if line.startswith('title'):
                continue
            lines = line.rstrip().split(',')
            count = line.count(",")
            if count >2:
                lines = lines[-3:]
            title,link,code = [i.strip() for i in lines]
            yield title,link,code

def doWork():
    # 存放链接的文件
    #path=r'C:\filetmp\demo.xlsx'
    #listUrl,listpwd= read_excel(path)
    links = links_generator('mebook.csv')
    listUrl = 'https://pan.baidu.com/share/init?surl=FHnc-CUY8NftuYf1GRtNrw'
    listpwd = 'r63h'
    #option = webdriver.ChromeOptions()
    #option.add_argument('headless')  # 静默模式
    
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    login(driver,"harland6","WGY123456096")
    
    handle_suc = open('success.csv', 'w+')
    handle_fail = open('fail.csv', 'w+')
    with tqdm(total=7845) as pbar:
        for title,link,code in links:
            extract(driver,link,code,handle_suc,handle_fail)
            pbar.update(1)
        #print(link)
    #extract(driver,listUrl,listpwd)
    #for index in range(len(listUrl)):
    #   srcurl=listUrl[index]
    #  srcpwd=listpwd[index]
    #    extract(driver,srcurl,srcpwd)
    #extract(driver,listUrl,listpwd)
        driver.quit()
        handle_suc.close()
        handle_fail.close()
    
if __name__ == '__main__':
    doWork()
