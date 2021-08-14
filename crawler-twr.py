import requests
from bs4 import BeautifulSoup
import time

tr_url = 'https://tip.railway.gov.tw/tra-tip-web/tip'
station_dic = {}

def getTrip(url, s_station, e_station, today, start_time, end_time):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('{} 發生錯誤'.format(url))
        return
    
    soup = BeautifulSoup(resp.text, 'html5lib')
    stations = soup.find(id = 'cityHot').ul.find_all('li')
    for station in stations:
        station_name = station.button.text
        station_id = station.button['title']
        station_dic[station_name] = station_id
    
    csrf = soup.find(id = 'queryForm').find('input', {'name':'_csrf'})['value']
    form_data = {
        'trainTypeList':'ALL',
        'transfer':'ONE',
        'startOrEndTime':'true',
        'startStation':station_dic[s_station],
        'endStation':station_dic[e_station],
        'rideDate':today,
        'startTime':start_time,
        'endTime':end_time
    }

    query_url = soup.find(id = 'queryForm')['action']
    q_resp = requests.post('https://tip.railway.gov.tw' + query_url, data=form_data)
    q_soup = BeautifulSoup(q_resp.text, 'html5lib')
    trs = q_soup.find_all('tr', 'trip-column')
    for tr in trs:
        td = tr.find_all('td')
        td_li = ''.join(list(td[0].li.stripped_strings))
        print('車種車次: {}, 出發時間: {}, 抵達時間: {}'.format(td_li, td[1].text, td[2].text))

getTrip(tr_url, '臺北', '臺南', '2021/08/20', '06:00', '20:00')
