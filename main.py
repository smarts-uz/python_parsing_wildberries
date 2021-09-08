from random import randrange
import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random



user_agent_lists=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'
]

headers={
    'Accept': '*/*',
    'User-Agent': f'{random.choice(user_agent_lists)}'
}
cookie={
    'cookie':'cookie: uid=08fbd572-9de1-487f-85e2-558495e241ab; uid3pd=4530643d-44a9-4215-aaef-254f3d061cfb'
}



all_categories_dict={
    'Смартфоны':'https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony'
}

all_pages=[14]



def check_exists(cate_name,prod_name):
    filees=os.path.isfile(f'd:/parsing5/{cate_name}/{prod_name}/product_detail.html')
    return filees


def test_request(url,headers=headers,retry=5,cookie=cookie):

    try:
        response=requests.get(url,headers=headers,cookies=cookie)
    except Exception as ex:
        if retry:
            return test_request(url,headers=headers,retry={retry-1},cookie=cookie)
        else:
            raise
    else:
        return response

def html_yaratish(res,cat_name,prod_name):
    with open(f"d:/parsing5/{cat_name}/{prod_name}/product_detail.html",'w',encoding='utf-8')as file:
        file.write(res)



def cate_dir(name):
    parent_dir=f'd:/parsing5/'
    path=os.path.join(parent_dir,f'{name}')
    os.mkdir(path)



# # 1 coment boshlandi ###########################################
count=0
for category_name,category_href in all_categories_dict.items():
    if not os.path.isdir(f'd:/parsing5/{category_name}'):
        cate_dir(category_name)
    else:
        continue

    for i in range(1,all_pages[count]+1):
        response =test_request(f'{category_href}?page={i}')
        source =response.text
        with open(f"{category_name}/{i}.html",'w',encoding='utf-8')as file:
            file.write(source)
    count+=1
    
###### 1 comment tugdi
# # 2 comment boshlandi #################################

    
def nom(product_href):
    l=''
    for i in reversed(product_href[:-25]):
        if i != '/':
            l+=i
        else:
            break
        s=''
        for i in reversed(l):
            s+=i
    return s

def prod_papka_yaratish(cate_name,nomi):
    if not os.path.isdir(f'{cate_name}/{nomi}'):
        return True
    else: 
        return False
    

def product_css(source,category_name):
    soup=BeautifulSoup(source,'lxml')
    all_product=soup.find_all(class_='product-card j-card-item')
    for product_hrefs in all_product:
        product_href=product_hrefs.find(class_='j-open-full-product-card').get('href')
        papka=nom(product_href)

        if prod_papka_yaratish(category_name,papka):
            parent_dir=f'd:/parsing5/{category_name}/'
            path=os.path.join(parent_dir,f'{papka}')
            os.mkdir(path)
            par_img=f'd:/parsing5/{category_name}/{papka}/'
            path_img=os.path.join(par_img,'images')
            os.mkdir(path_img)
        else:
            continue
        if check_exists(category_name,papka):

            product_names={}
            response=test_request(f'https://www.wildberries.ru{product_href}')
            source =response.text
        with open(f"{category_name}/{papka}/product_detail.html",'w',encoding='utf-8')as file:
            file.write(source)
        


        brand_name=product_hrefs.find(class_='product-card__brand-name').find(class_='brand-name').get_text()
        product_name=product_hrefs.find(class_='product-card__brand-name').find(class_='goods-name').get_text()
        
        product_names['product-link']=f'https://www.wildberries.ru{product_href}'
        product_names['brand-name']=f'{brand_name}'
        product_names['product-name']=f'{product_name}'
        

        with open(f"d:/parsing5/{category_name}/{papka}/product_and_brand_name.json",'w',encoding='utf-8')as file:
            json.dump(product_names,file,indent=4,ensure_ascii=False)


for category_name,category_href in all_categories_dict.items():
    for i in range(1,15):
        with open(f"{category_name}/{i}.html",encoding='utf-8')as file:
            source=file.read()
        product_css(source,category_name)


    


# 2 chi comment tugadi###############################
# 3 chi comment boshlanishi rasm saqlash############################

def check_img_dir(category_name,papka,images):
    if os.path.isdir(f'd:/parsing5/{category_name}/{papka}/{images}'):
        return True
    else:
        return False



def product_all_images(source,category_name):
    soup=BeautifulSoup(source,'lxml')
    all_product=soup.find_all(class_='product-card j-card-item')
    for product_hrefs in all_product:
        product_href=product_hrefs.find(class_='j-open-full-product-card').get('href')
        papka=nom(product_href)
        with open(f"{category_name}/{papka}/product_detail.html",encoding='utf-8')as file:
            soup=file.read()
        if check_img_dir(category_name,papka,'images'):
            source=BeautifulSoup(soup,'lxml')
            prod_images=source.find(class_='swiper-container j-sw-images-carousel').find('ul').find_all('li')
            count_img=1
            print(papka)
            for prod_image in prod_images:
                if 'slide--video' in prod_image['class']:
                    continue
                else:
                    image=prod_image.find('img').get('src')
                    req_img=test_request(f'https:{image}').content
                    with open(f"{category_name}/{papka}/images/{papka}-{count_img}.jpg",'wb')as file:
                        file.write(req_img)
                    count_img+=1
            prod_valid=source.find(class_='sw-slider-colorpicker').find(class_='swiper-wrapper').find_all(class_='swiper-slide j-color')
            if not prod_valid:
                continue
            else:
                val_count=1
                for val_images in prod_valid:
                    val_image=val_images.find('img').get('src')
                    val_img=test_request(f'https:{val_image}').content
                    with open(f"{category_name}/{papka}/images/{val_count}.jpg",'wb')as file:
                        file.write(val_img)
                    val_count+=1
            brand_img_href=source.find(class_='same-part-kt__brand-logo').find('img').get('src')
            if brand_img_href !=None:
                brand1=test_request(f'https:{brand_img_href}')
                brand=brand1.content
                with open(f"{category_name}/{papka}/images/brand.jpg",'wb')as file:
                        file.write(brand)
        else:
            par_img=f'd:/parsing5/{category_name}/{papka}/'
            path_img=os.path.join(par_img,'images')
            os.mkdir(path_img)



for category_name,category_href in all_categories_dict.items():
    for i in range(1,6):

        with open(f"{category_name}/{i}.html",encoding='utf-8')as file:
            source=file.read()
        product_all_images(source,category_name)




# #3 chi tugadi ############################

# # # 4 chi boshlanishi ######################


def product_characters(source,category_name):
    soup=BeautifulSoup(source,'lxml')
    all_product=soup.find_all(class_='product-card j-card-item')
    
    for product_hrefs in all_product:
        product_href=product_hrefs.find(class_='j-open-full-product-card').get('href')
        papka=nom(product_href)
        with open(f"{category_name}/{papka}/product_detail.html",encoding='utf-8')as file:
            soup=file.read()
        print(papka)
        source=BeautifulSoup(soup,'lxml')
        caption=source.find(class_='product-params').find(class_='product-params__table').find('caption')
        
        caption_name='Общие характеристики'
        cap_dict={}
        sub_cap_dict={}
        if caption !=None:
            for a in caption.next_siblings:
                if a.name=='caption':
                    cap_dict[f'{caption_name}']=f'{sub_cap_dict}'
                    caption_name=a.get_text()
                    sub_cap_dict={}
                else:
                    if a.find('tr')!=-1 and a.find('tr')!=None:
                        sub_name=a.find('tr').find('th').find('span').find('span').get_text()
                        sub_value=a.find('tr').find('td').get_text()
                        sub_cap_dict[f'{sub_name}']=f'{sub_value}'
                    else:
                        continue
            cap_dict[f'{caption_name}']=f'{sub_cap_dict}'
        else:
            for a in source.find(class_='product-params').find(class_='product-params__table').find_all('tbody'):
                sub_name=a.find('tr').find('th').find('span').find('span').get_text()
                sub_value=a.find('tr').find('td').get_text()
                sub_cap_dict[f'{sub_name}']=f'{sub_value}'

            cap_dict[f'{caption_name}']=f'{sub_cap_dict}'
        # if description_title=source.find(class_='product-detail__details details').find(class_='details__header-wrap') !=None:    
        for desc in source.find_all(class_='product-detail__details details'):
            description_title=desc.find('h2').get_text()
            description_text=desc.find(class_='details__content').find('p').get_text()
            cap_dict[f'{description_title}']=f'{description_text}'
        
    with open(f"d:/parsing5/{category_name}/{papka}/product_characters.json",'w',encoding='utf-8')as file:
            json.dump(cap_dict,file,indent=4,ensure_ascii=False)
       
        # with open(f"d:/parsing5/json/product_characters.json",'w',encoding='utf-8')as file:
        #     json.dump(cap_dict,file,indent=4,ensure_ascii=False)



for category_name,category_href in all_categories_dict.items():

    for i in range(1,15):

        with open(f"{category_name}/{i}.html",encoding='utf-8')as file:
            source=file.read()
        product_characters(source,category_name)



# # 4 chi tugashi ############################










