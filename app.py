from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
import numpy as np
import pickle as p
import pandas as pd
import json
import hashlib
import requests

app = Flask(__name__)





features = [

         {'type': 'datetime', 'name': 'ads_created_at', 'title': 'Дата и время публикации объявления'},
         {'type': 'integer', 'name': 'views', 'title': 'Количество просмотров'},
         {'type': 'integer', 'name': 'deposit', 'title': 'Депозит'},
         {'type': 'integer', 'name': 'client_fee', 'title': 'Клиентская плата'},
         {'type': 'categorical','name': 'communal', 'title': 'Включение коммунальных платежей в стоимость'},
        {'type': 'boolean', 'name': 'communal_included', 'title': 'Включение коммунальных платежей в стоимость'},    
        {"type":"integer", 'name': 'floor', 'title': 'Этаж'},
         {'type': 'double', 'name': 'area_total', 'title': 'Общая площадь'},
        {'type': 'double', 'name': 'area_living', 'title': 'Площадь жилая'},
        {'type': 'double', 'name': 'area_kitchen', 'title': 'Площадь кухни'},
       {'type': 'double', 'name': 'ceiling', 'title': 'Высота потолков'},
        {'type': 'integer', 'name': 'rooms', 'title': 'Количество комнат'},
        {'type': 'integer',  'name': 'bedrooms', 'title': 'Количество спален'},
        {'type': 'categorical', 'name': 'wc_combined', 'title': 'Совместный сан. узел'},
        {'type': 'categorical', 'name': 'wc_separated', 'title': 'Раздельный сан. узел'},
        {'type': 'boolean', 'name': 'is_children_allowed', 'title': 'Можно ли с детьми'},
        {'type': 'boolean', 'name': 'is_pets_allowed', 'title': 'Можно ли с животными'},
        {'type': 'boolean', 'name': 'has_ac', 'title': 'Наличие кондиционера'},
        {'type': 'boolean', 'name': 'has_fridge', 'title': 'Наличие холодильника'},
        {'type': 'boolean', 'name': 'has_washmach', 'title': 'Наличие стиральной машины'},
        {'type': 'boolean', 'name': 'has_dishwash', 'title': 'Наличие посудомоечной машины'},
        {'type': 'boolean', 'name': 'has_internet', 'title': 'Наличие интернета'},
        {'type': 'boolean', 'name': 'has_tv', 'title': 'Наличие телевизора'},
        {'type': 'boolean','name': 'has_phone','title': 'Наличие телефона'},
        {'type': 'boolean', 'name': 'has_room_furniture', 'title': 'Наличие мебели'},
        {'type': 'boolean', 'name': 'has_kitchen_furniture','title': 'Наличие кухонного гарнитура'},
        {'type': 'boolean','name': 'has_bath', 'title': 'Наличие ванны'},
        {'type': 'boolean','name': 'has_shower','title': 'Наличие душевой кабины'},
        {'type': 'boolean','name': 'has_rubbish_chute','title': 'Наличие мусоропровода'},
        {'type': 'boolean','name': 'has_parking', 'title': 'Наличие парковки'},
        {'type': 'boolean','name': 'has_iron', 'title': 'Наличие утюга'},
        {'type': 'boolean','name': 'has_microwave', 'title': 'Наличие микроволновой печи'},
        {'type': 'integer','name': 'loggias', 'title': 'Количество лоджий'},
        {'type': 'integer','name': 'balconies', 'title': 'Количество балконов'},
        {'type': 'integer','name': 'pass_lifts', 'title': 'Количество пассажирских лифтов'},
        {'type': 'integer','name': 'serv_lifts', 'title': 'Количество грузовых лифтов'},
        {'type': 'categorical', 'name': 'repair_type', 'title': 'Тип ремонта', 'options': [

            {'name': 'unknown', 'Title': '-'},
            {'name': 'cosmetic', 'title': 'Косметический'},
            {'name': 'euro', 'title': 'евро-ремонт'},
            {'name': 'design', 'title': 'design'},
         ]},

        {'type': 'categorical', 'name': 'window_view', 'title': 'Вид из окна', 'options': [

            {'name': 'unknown', 'title': ''},
            {'name': 'yard', 'title': 'yard'},
            {'name': 'street', 'title': 'street'},
            {'name': 'yard_and_street', 'title': 'yard_and_street'}

        ]},

        {'type': 'double', 'name': 'latitude', 'title': 'Долгота'},
        {'type': 'double', 'name': 'longitude', 'title': 'Широта'},
        {'type': 'integer', 'name': 'build_year', 'title': 'Год постройки'},
        {'type': 'integer', 'name': 'square_meter_price', 'title': 'Цена за квадратный метр'},
        {'type': 'integer', 'name': 'flat_count', 'title': 'Количество квартир'},
        {'type': 'integer', 'name': 'floors_count', 'title': 'Количество этажей'},
        {"type": 'integer', 'name': 'entrances', 'title': 'Количество подъездов'},
        {'type': 'categorical', 'name': 'walls_type', 'title': 'Тип здания/стен'},
        {'type': 'categorical', 'name': 'walls_type_raw', 'title': 'Тип здания/стен', 'options': [
                                                                        {'name': 'кирпич', 'title': 'Кирпич'},
                                                                        {'name': 'дерево', 'title': 'Дерево'},
                                                                        {'name': 'монолит', 'title': 'Монолит'}
                                                                    ]
         },
          {'type': 'categorical', 'name': 'beltway_hit', 'title': 'Расположенность в пределах КАД', 'options': [

            {'name': 'OUT_MKAD', 'title': 'OUT_MKAD'},
            {'name': 'IN_MKAD', 'title': 'IN_MKAD'},
            {'name': 'OUT_KAD', 'title': 'OUT_KAD'}

        ]},

        {'type': 'integer','name': 'beltway_distance', 'title': 'Расстояние до КАД'},

        {'type': 'categorical', 'name': 'region_with_type', 'title': 'Регион', 'options': [

            {'name': 'г Москва', 'title': 'г Москва'},
            {'name': 'Московская обл', 'title': 'Московская обл'}

        ]},

        {'type': 'categorical', 'name': 'city_with_type', 'title': 'Город'},
        
        {'type': 'categorical', 'name': 'city_area', 'title': 'Часть города'},
        {'type': 'categorical', 'name': 'city_district_with_type', 'title': 'Район'},
        {'type': 'categorical', 'name': 'settlement_with_type', 'title': 'Поселок'},
        {'type': 'categorical', 'name': 'metro_line', 'title': 'Линия метро'},
        {'type': 'categorical', 'name': 'metro_station', 'title': 'Станция метро'},
        {'type': 'double', 'name': 'metro_distance', 'title': 'Расстояние до станции метро'},
         {'type': 'datetime', 'name': 'closed_at', 'title': 'Дата и время закрытия объявления'},
        
        
]











price_studio = p.load(open('models/price_studio.pickle', 'rb'))

time_studio = p.load(open('models/time_studio.pickle', 'rb'))




#Для каждого числа комнат - свои модели
models_dict = {
    0: ('models/price_studio.pickle', 'models/time_studio.pickle'),
    1: ('models/price_one_room.pickle', 'models/time_one_room.pickle'),
    2: ('models/price_two_rooms.pickle', 'models/time_two_rooms.pickle'),
    3: ('models/price_three_rooms.pickle', 'models/time_three_rooms.pickle'),
}



def get_canonical_address(addr):
    url = 'https://geocode-maps.yandex.ru/1.x/?'
    api_key = '239260b8-0453-4bde-b6bf-dbdf49c215f3'
    params = {
        'apikey': api_key,
        'format': 'json',
        'geocode': addr,
        'rspn': 1,
        'bbox': '35.608043,56.428181~40.591202,54.838814'
    }
    json_response = requests.get(url, params=params).json()
    address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    return address




def get_address_info(can_addr):
    url = 'https://selection-api.pik-arenda.ru/get_build_info.php?'
    token = hashlib.md5((can_addr + "17137de0127e55c7de8f3ac9ad2d3ff9").encode()).hexdigest()
    params = {
        'token': token,
        'address': can_addr
    }
    try:
        json_response = requests.get(url, params=params).json()
        return json_response
    except json.decoder.JSONDecodeError:
        return None




@app.route('/form_ver2')
def form_ver2():
    return render_template('form_ver2.html', features=features)


@app.route('/get_price_ver2', methods=['POST'])
def get_price_ver2():

    form_dict = request.form

    print(form_dict)

    return "It's ok :) "



if __name__ == '__main__':
    app.run()







