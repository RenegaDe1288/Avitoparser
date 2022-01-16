from bs4 import BeautifulSoup
import requests
import fake_useragent
import csv
import re


def main(response):
    data = BeautifulSoup(response, 'lxml')
    list = data.find('div', class_='items-items-kAJAg')
    list_1 = list.find_all('div',
                           class_='iva-item-root-Nj_hb photo-slider-slider-_PvpN iva-item-list-H_dpX iva-item-redesign-nV4C4 iva-item-responsive-gIKjW items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum')
    return list_1


def check(list_1):
    count = 1
    yt = 0
    for i in list_1:
        yt += 1
        print('Объявление №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№ ', yt)

        title = i.find('h3',
                       class_='title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO').text
        title = re.sub('[^A-Za-zА-яЁа-яе .,!?:%^&\\\*#@=+()0-9/\-\\n\\t]', '', title)
        print(count)
        print(title)
        link = 'https://www.avito.ru' + i.find('div', class_='iva-item-titleStep-_CxvN').find('a').get('href')
        print(link)

        try:
            pic_link = i.find('ul', class_='photo-slider-list-xFf2c').find('li').get('data-marker')[19:]
        except AttributeError:
            pic_link = 'нет фото'
        print(pic_link)

        try:
            price = i.find('span', class_="price-price-BQkOZ").text
            price = int(re.sub('[^0-9]','',price))
        except ValueError:
            price = 'Цена  не указана'
        print(price)

        try:
            params = i.find('div', class_="iva-item-text-_s_vh text-text-LurtD text-size-s-BxGpL").text
            params = re.sub('[^A-Za-zА-яЁа-яе .,!?:%^&\\\*#@=+()0-9/\-\\n\\t]', '', params)
        except AttributeError:
            params = 'None'
        print(params)

        try:
            description = i.find('div', class_="iva-item-text-_s_vh iva-item-description-S2pXQ text-text-LurtD text-size-s-BxGpL").text
            description= re.sub('[^A-Za-zА-яЁа-яе .,!?:%^&*#@=+()0-9/\-\\n\\t\\\]','',description)
        except AttributeError:
            description = 'Нет описания'


        try:
            adress = i.find('span', class_="geo-address-QTv9k text-text-LurtD text-size-s-BxGpL").text
        except AttributeError:
            # adress = i.find('div', class_="geo-georeferences-2gY4s text-text-1la7J text-size-s-2vtIX").text
            adress = 'No adress'

        print(adress)

        try:
            date = i.find('div', class_="date-text-VwmJG text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs").text
        except AttributeError:
            date = ' нет даты'
        print(date)

        try:
            name = i.find('div', class_='styles-root-JMoCE text-text-LurtD text-size-s-BxGpL').find('a').get('title')
        except AttributeError:
            name = 'нет имени'
            print('exception')
        print(name)

        try:
            company = i.find('span',
                         class_='iva-item-text-_s_vh iva-item-textColor-gray44-Fq8XF text-text-LurtD text-size-s-BxGpL').text
        except AttributeError:
            company= 'Нет компании'
        print(company)
        count += 1
        write(title, link, pic_link, price, params, description, adress, date, name, company)



def write(title, link, pic_link, price, params, description, adress, date, name, company):
    try:
        with open('parser.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([title, link, pic_link, price, params, description, adress, date, name, company])
    except UnicodeEncodeError:
        print('ERRROR')
        with open('parser.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([title, link, pic_link, price, params])


def load():
    n = 1

    with open('parser.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Название', 'Ссылка на объявление', 'Ссылка на фото', 'Цена', 'Параметры', 'Описание', 'Адрес', 'Дата', 'Имя',
             'Компания'])


    link = 'https://www.avito.ru/rossiya/avtomobili?q=mitsubishi+galant+8'
    while True:
        new_link = f'{link}&p={str(n)}'
        print(new_link)

        user = fake_useragent.UserAgent().random
        headers = {'header': user}
        print(headers)

        response = requests.get(new_link, headers=headers).text
        response = main(response)
        if len(response)!=0:
            check(response)
            n += 1

        else:
            break

load()