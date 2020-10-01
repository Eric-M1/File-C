import requests
from time import sleep
from os import sys, path, system
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup

URL_PHONESC = 'https://api.phonebook.space/'
HEADERS_PHONESC = {'Authorization': 'Token  69cad03c647dd216e0666a2679e71f6bb307fc88'}


def clear():
    if sys.platform == "win32":
        system("cls")
        print("[+] Бот включён...\n")
    else:
        system("clear")
        print("[+] Бот включён...\n")

def get_proxy_from_api():
    get_proxy = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1900&country=all&anonymity=all&ssl=yes').text.split('\r\n')[:-1]

    get_content = BeautifulSoup(requests.get('https://free-proxy-list.net/').text, 'lxml')
    table = get_content.find('table')
    rows = table.find_all('tr')
    
    proxyP = []
    for row in rows:
        ip = row.contents[0].text
        port = row.contents[1].text
        anon = row.contents[4].text
        https = row.contents[6].text

        if https == 'no' and (anon == 'all' or anon == 'elite proxy'):
            proxyP.append(f'{ip}:{port}')

    return [*get_proxy, *proxyP]

def del_proxy():
    with open('help_files/work-proxy.txt', 'r') as f:
        lines = f.readlines()
    with open('help_files/work-proxy.txt', 'w') as f:
        f.writelines(lines[1::])

def get_number(number: str) -> str:
    number = ''.join([char for char in number if char in ('+1234567890')])

    if number.startswith('8'):
        number = ''.join(('7', number[1:]))
    if not number.startswith('+'):
        number = ''.join(('+', number))
    return number if len(number) in (10, 11, 12, 13, 14) else None

def get_data_from_avito(number: str) -> str:

    AVITO_API_BASE_URL = "https://mirror.bullshit.agency/"
    response_from_avito = requests.get(''.join((AVITO_API_BASE_URL, 'search_by_phone/', number)))

    if response_from_avito.status_code == 404:
        return '👨‍⚖ Авито: Объявлений не найдено\n🤷🏻‍♂️ А может повторим?.'
    if response_from_avito.status_code == 503:
        return '⚠️ Авито: Все поисковые потоки забиты, пожалуйста, повторите запрос через 3-5 минут.'

    soup = BeautifulSoup(response_from_avito.text, features="lxml")
    sells_count = f"👨‍⚖ Авито: Найдено{soup.title.string}"
    links = soup.find_all('a')
    hrefs = []
    for link in links:
        if link['href'].split(':')[0] == 'https':
            pass
        else:
            hrefs.append(link['href']) 

    herefs_len = len(hrefs)
    if int(herefs_len) > 20:
        del hrefs[20:]
        sellers_info = [f'😋 Авито: Найдено 20 объявлений по телефону {number}\n']
    else:
        sellers_info = [sells_count]
    for href in hrefs:
        response = requests.get(''.join((AVITO_API_BASE_URL, href)))
        soup = BeautifulSoup(response.text, features='lxml')
        try:
            sellers_info.append(f'📦 Продал (-ёт): {soup.h1.string}')
            sellers_info.append(f"💰 Цена: {' '.join(soup.p.string.split()[1:])}")
            sellers_info.append(f"🗺 Адрес: {soup.select('div > p')[1].get_text(strip=True)}")
            sellers_info.append(f'🎭 Лицо продавца: {soup.span.string}')
            sellers_info.append(f'👽 Имя продавца: {soup.strong.string}')
            sellers_info.append(f'🔗 Ссылка на товар: {soup.a["href"]}\n')
        except AttributeError:
            pass
    # if len(hrefs) > 17:
    #     one_msg = sellers_info[:len(sellers_info)//2]
    #     one_msg = '\n'.join(one_msg)

    #     two_msg = sellers_info[len(sellers_info)//2:]
    #     two_msg = '\n'.join(two_msg)

    #     return one_msg, two_msg
    # elif len(hrefs) > 30:
    #     one_msg = sellers_info[:len(sellers_info)//3]
    #     one_msg = '\n'.join(one_msg)

    #     two_msg = sellers_info[len(sellers_info)//3:]
    #     two_msg = '\n'.join(two_msg)
    #     return one_msg, two_msg

    # de = 'Это всё!'
    if not sellers_info:
        return '👨‍⚖ Авито: Ничего нет'
    else:
        return '\n'.join(sellers_info) 
        

def get_tags_by_number(number: str) -> str:
    respons = requests.get(''.join((URL_PHONESC, f"number/?number={number}")), headers=HEADERS_PHONESC).json()['tags']
    if not respons:
        return f'По "{number}" Ничего не нашёл'
    else:
        return 'Возможное имя: '+'\nТег: '.join(respons)

def get_numbers_by_name(name: str) -> str:
    try:
        respons = requests.get(''.join((URL_PHONESC, f"name/?name={name}")), headers=HEADERS_PHONESC).json()['data']
    except ValueError:
        return f'🙎🏻‍♂️ - На "{name.title()}" Ничего не найдено'
    else:
        user_name = []
        if not respons:
            return f'🙎🏻‍♂️ - На "{name.title()}" Ничего не найдено'
        else:
            for tag in respons:
                tags = "\nТег: ".join(respons[tag])
                user_name.append(f'Номер: {tag}\nТег: {tags}\n')
            return '\n'.join(user_name)


def get_data_from_num(number: str) -> str:           
    proxy = get_proxy_from_api()

    for proxy in proxy:
        try:
            print(f'[-] Прокси: {proxy}') #
            proxies = {
                'http': 'http://'+proxy,
                'https': 'http://'+proxy}
            num_P = requests.post('https://htmlweb.ru/geo/api.php?json&telcod='+str(number), proxies = proxies, timeout = 7).json()#
            if num_P['limit'] == 0:
                print('[!] Лимит: 0')
                continue #
            else:
                pass
            with open('help_files/work-proxy.txt', 'a') as w_proxy:
                w_proxy.write(f'{proxy}\n')
            data_num = []

            try:
                country = num_P['country']
                try:
                    data_num.append('Страна: '+country["name"] +', '+country["fullname"])
                except KeyError:
                    if country["country_code3"] == 'UKR':
                        data_num.append('Страна: Украина')
                    else:
                        pass
                        
                try:
                    data_num.append('Код страны: '+country["country_code3"])
                except KeyError:
                    pass


                try:
                    data_num.append('Код номера: '+str(country["telcod"]))
                except KeyError:
                    pass


                try:
                    data_num.append('Локация: '+country["location"])
                except KeyError:
                    pass
                

                try:
                    data_num.append('Язык: '+country["lang"])
                except KeyError:
                    pass
            except KeyError:
                pass

            try:
                region = num_P['region']
                endIndex = region['name'].split()
                    
                try:
                    if endIndex[1] == 'край':
                        data_num.append('Край: '+region["name"])
                except IndexError:
                    data_num.append('Неизвестное: '+region["name"])
                except KeyError:
                    pass

                try:
                    if endIndex[1] == 'область':
                        data_num.append('Область: '+region["name"])
                    else:
                        data_num.append('Неизвестное: '+region["name"])
                except IndexError:
                    pass
                
                except KeyError:
                    pass
                try:
                    data_num.append('Округ: '+region["okrug"])
                except KeyError:
                    pass
            except KeyError:
                pass

            try:
                capital = num_P['capital']
                try:
                    data_num.append('Столица: '+capital["name"])
                except KeyError:
                    pass

                try:
                    data_num.append('Код города: +'+str(capital["telcod"]).replace(",", ", "))
                except KeyError:
                    pass            
            except KeyError:
                pass

            try:
                data = num_P['0']

                try:
                    data_num.append('Город: '+data["name"])
                except KeyError:
                    pass
                
                try:
                    data_num.append('Оператор: '+data["oper_brand"])
                except KeyError:
                    pass
                try:
                    data_num.append('Широта / Долгота: '+str(num_P["latitude"]) +', '+ str(num_P["longitude"]))
                except KeyError:
                    pass

                data_num.append('\n'+get_tags_by_number(number))    
                print('[+] Лимит: '+str(num_P["limit"]))
            except KeyError:
                pass
            data_num.insert(0, '👨‍⚖ Всё что смогли найти:\n')
            return '\n'.join(data_num)

        except requests.exceptions.RequestException:
            continue
        except ValueError:
            return '👨🏻‍🔧 - Внимание: сервер отклонил ваш запрос.\n👮🏻‍♂️ - Пожалуйста дайте нам знать: @FELIX4\n💁🏻‍♂️ - Или попробуйте еще раз через 10-20 сек'

def get_car_data(car_num: str) -> str:
    car_num = car_num.replace('а', 'a').replace('в', 'b').replace('е', 'e').replace('к', 'k').replace('м', 'm').replace('н', 'h').replace('о', 'o').replace('р', 'p').replace('с', 'c').replace('т', 't').replace('у', 'y').replace('х', 'x')
    result = requests.get(f'https://baza-gai.com.ua/nomer/{car_num}').text
    car_content = BeautifulSoup(result, 'html.parser')

    try:
        car_data = car_content.find('table', class_="table table-striped table-responsive tbl").text.strip().replace('\n', ' ').replace('           ', ' ').split('    ')
        car_data = [data.text.split()[::1] for data in car_content.find_all('td')]
    
        car_num_data = ['👨‍⚖ Всё что смогли найти:']
        car_num_data.append(f'📃 Регистрация: {" ".join(car_data[0])}')
        car_num_data.append(f'🚌 Модель:  {" ".join(car_data[1])}')
        car_num_data.append(f'📊 Параметры: {" ".join(car_data[2])}') 
        car_num_data.append(f'📝 Все операции: {" ".join(car_data[3])}')
        car_num_data.append(f'🗺 Адрес: {" ".join(car_data[4])}\n')
        return '\n'.join(car_num_data)
    except AttributeError:
        return '👨‍⚖ Авто не найден\n🤷🏻‍♂️ А может повторим?' 

def get_account(name: str) -> str:
    user_name = ''.join([char for char in name if char in ('_-1234567890qwertyuiopasdfghjklzxcvbnm.')])
    if not user_name:
        return '⚠️ Введите имя в Англ формате!'
    all_site = ['Всё что смогли найти:']
    file = open('help_files/link_file.txt', 'r')

    def get_response(user_name):
        for link in file:
            found = link.strip().split('www.')[1].title()
            link = link.strip()
            try:
                response = requests.get(f'{link}/{user_name}')
                if response.status_code == 200:
                    all_site.append(f'👨‍⚖ Аккаунт найден в: {found}\nСсылка: {link}/{user_name}\n')
            except requests.exceptions.RequestException:
                pass
        

    threads = []
    for i in range(26):
        t = Thread(target=get_response, args=(user_name,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    return all_site

def get_inn_data(inn):
    URL = 'https://zachestnyibiznes.ru'
    response = requests.get(''.join((URL, '/search?query=', inn))).text
    content = BeautifulSoup(response, 'html.parser').find('table', class_='table table-bordered table-striped rwd-table')
    link = ''.join((URL, content.find('a')['href'])) 

    response_pro = requests.get(link).text
    content_pro = BeautifulSoup(response_pro, 'html.parser').find('div', class_='col-xs-12 col-md-6')

    h2_f5 = content_pro.find('h2', class_='f-s-16 f-w-400 m-b-15').text.strip()
    mt_15 = content_pro.find('div', class_='m-t-15').text.strip()
    span_address = content_pro.find('span', itemprop='address').text.strip()
    span_work = content_pro.find('span', itemprop='isicV4').nextSibling
 
    tax_data = [tax_fond.text.strip() for tax_fond in content_pro.find('div', class_='m-t-15 m-b-15').find('thead', class_='text-left').findNext('tbody').find_all('td')]
    pfr = tax_data[0].replace('\xa0\n?', '')
    reg_n = tax_data[1]
    reg_date = tax_data[2].replace('По данным портала ЗАЧЕСТНЫЙБИЗНЕС', '')

    tax_mark = [tax_market.text.strip() for tax_market in content_pro.find('table', class_='m-t-5').find_all('span')]
    tax_okato = tax_mark[0]
    tax_okopf = tax_mark[1]
    tax_okfs = tax_mark[2]

    all_inn_data = []
    all_inn_data.append('\n')
    try:
        all_inn_data.append('Цель: ' + h2_f5.replace('По данным портала ЗАЧЕСТНЫЙБИЗНЕС', ''))
    except AttributeError:
        pass
    try:
        all_inn_data.append(mt_15.replace(' По данным портала ЗАЧЕСТНЫЙБИЗНЕС', '').replace('?', '')) 
    except AttributeError:
        pass
    try:
        all_inn_data.append('Окпо: ' + content_pro.find('span', id='okpo').text)
    except AttributeError:
        pass
    try:
        all_inn_data.append('Октмо: ' + content_pro.find('span', id='oktmo').text)
    except AttributeError:
        pass
    try:
        all_inn_data.append('Местоположение: ' + span_address.replace('По данным портала ЗАЧЕСТНЫЙБИЗНЕС', ''))
    except AttributeError:
        pass
    try:
        all_inn_data.append('Основной вид деятельности: ' + span_work.replace('По данным портала ЗАЧЕСТНЫЙБИЗНЕС', '').strip().title())
    except AttributeError:
        pass
    try:
        all_inn_data.append(f'\nРегистрация во внебюджетных фондах:\nФонд: {pfr}\nРег.номер: {reg_n}\nДата регистрации: {reg_date}')
    except AttributeError:
        pass
    try:
        all_inn_data.append(f'\nКоды статистики:\nОкато: {tax_okato}\nОкопф: {tax_okopf}\nОкфс: {tax_okfs}')
    except AttributeError:
        pass
    return all_inn_data

def get_inn(user_name):
    json = {'query': user_name.strip().title(),}
    nalog_site = requests.post('https://egrul.nalog.ru/', json=json).json()['t']
    get_response = requests.get('https://egrul.nalog.ru/search-result/'+ nalog_site)

    try:
        data_inn = ['Всё что смогли найти:\n']
        try:
            list_peolple = get_response.json()['rows']
        except (KeyError, AttributeError):
  	        first_choice = {'n':'0'}
        else:
            first_choice = list_peolple[0]
            inn_all_d = get_inn_data(first_choice["i"])

        if first_choice["n"].title() != user_name:
            return '😩 ФИО: Подходящих людей под этим именем нет\n🤔 А может вы ошиблись?'
        else:
            data_inn.append(f'Всего людей: {first_choice.get("tot", "Ничего нет")}')
            data_inn.append(f'Фио: {first_choice.get("n", "Ничего нет").title()}')
            data_inn.append(f'Инн: {first_choice.get("i", "Ничего нет")}')
            data_inn.append(f'Огрнип: {first_choice.get("o", "Ничего нет")}')
            data_inn.append(f'Дата присвоения огрнип: {first_choice.get("r", "Ничего нет")}')
            data_inn.append(f'Дата прекращения деятельности: {first_choice.get("e", "Ничего нет")}')
    except IndexError:
        return '😩 ФИО: Ничего нет\n🤔 А может вы ошиблись?'
    dat_in = '\n'.join(data_inn)
    dat_all_in = '\n'.join(inn_all_d)
    return dat_in + dat_all_in 

def get_car_photo(car_number):
    car_number_au = car_number.replace('а', 'a').replace('в', 'b').replace('е', 'e').replace('к', 'k').replace('м', 'm').replace('н', 'h').replace('о', 'o').replace('р', 'p').replace('с', 'c').replace('т', 't').replace('у', 'y').replace('х', 'x')
    get_c = requests.get(f"https://auto.ru/history/{car_number_au}/")
    _csrf_token = dict(get_c.cookies).get("_csrf_token", "Токена нет")
    if _csrf_token == 'Токена нет':
        car_in = []
        car_in_p = []
        return car_in, car_in_p
    else:
        headers = {"x-csrf-token":_csrf_token}
        cookies = dict(_csrf_token=_csrf_token)

        response = requests.post("https://auto.ru/-/ajax/desktop/getRichVinReport/",data={"vin_or_license_plate":car_number, "isCardPage":"false", "geo_radius":300, "geo_id":[62]}, headers=headers, cookies=cookies)
        report = response.json().get('report', "Токена нет")
        if report == 'Токена нет':
            car_in = []
            car_in_p = []
            return car_in, car_in_p
        else:
            car_info = []

            try:
                car_info.append(f'🏎 Модель машины: {report["header"]["title"].split(", ")[0]}')
            except KeyError:
                car_info.append("🏎 Модель машины: Не определён")

            try:
                car_info.append(f'📆 Год выпуска: {report["pts_info"]["year"]["value"]}')
            except KeyError:
                car_info.append("📆 Год выпуска: Не определён")

            try:
                car_info.append(f'🔋 Двигатель: {report["pts_info"]["displacement"]["value_text"]} / {report["pts_info"]["horse_power"]["value_text"]}')
            except KeyError:
                car_info.append("🔋 Двигатель: Не определён")

            try:
                car_info.append(f'🎨 Цвет: {report["pts_info"]["color"]["value"]}')
            except KeyError:
                car_info.append("🎨 Цвет: Не определён")

            try:
                car_info.append(f'🧯 Важно: {str(report["content"]["items"][0]["key"])}, {str(report["content"]["items"][0]["value"])}')
            except KeyError:
                car_info.append("🧯 Важно: Не определён")

            try:
                car_info.append(f'⏰ Время поиска: {str(report["headerData"]["date"])}')
            except KeyError:
                car_info.append("⏰ Время поиска: Не определён")
            
            try:
                car_info.append(f'🧰 VIN номер: {str(report["headerData"]["vin"])}')
            except KeyError:
                car_info.append("🧰 VIN номер: Не определён")


            links = []
            URL = 'https://avto-nomer.ru'
            
            car_number_ru = car_number.replace('a', 'а').replace('b', 'в').replace('e', 'е').replace('k', 'к').replace('m', 'м').replace('h', 'н').replace('o', 'о').replace('p', 'р').replace('c', 'с').replace('t', 'т').replace('y', 'у').replace('x', 'х')
            res = requests.get(''.join((URL, '/gallery.php?fastsearch=', car_number_ru))).text
            co = BeautifulSoup(res, 'html.parser')
            h1_text = co.find('h1', class_='pull-left').text.strip()

            if h1_text == 'Найдено номеров 0':
                pass
            else:
                site_find = co.find('div', class_='col-md-9')
                for divs in site_find.find_all('div', class_='row margin-bottom-10'):
                    for col in divs.find_all('div', class_='col-sm-6 col-xs-12'):
                        panel_grey = col.find('div', class_='panel panel-grey')
                        panel_body = panel_grey.find('div', class_='panel-body')
                        row = panel_body.find('div', class_='row')

                        link = row.find('a')['href'].replace('/nomer', '/foto')
                        photo_st = requests.get(''.join((URL, link))).text
                        car_photo_site = BeautifulSoup(photo_st, 'html.parser')
                        links.append(car_photo_site.find('div', class_='wrapper').find('img')['src'])
                    
            return car_info, links


def all_users_f():
    users = open('help_files/users_id.txt', 'r').readlines()
    return len([user for user in users])


    