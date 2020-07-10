from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
import numpy as np
import pickle as p
import pandas as pd
import json
import hashlib
import requests

app = Flask(__name__)


feature_names = ['']


def func(form_dict):

    for elem in form_dict:

        if form_dict[elem] == 'on':
            form_dict[elem] = 'True'






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


def func(features):
    address = features.get('full_address')

    canonical_address = get_canonical_address(address)

    print(canonical_address)

    address_info = get_address_info(canonical_address)

    features['square_meter_price'] = address_info['square_meter_price']
    features['city_district_with_type'] = address_info['city_district_with_type']



@app.route('/get_price', methods=['POST'])
def get_price():

    data = request.get_json()

    features_dict = data.get('features')

   #print(features_dict)

   #func(features_dict)

   #print("==========================================")

    print(features_dict)

    rooms = features_dict.get('rooms')



    features_array = np.array(list(features_dict.values()))


    price_model_path, time_exp_model_path = models_dict[rooms]

    price_model = p.load(open(price_model_path, 'rb'))
    time_exp_model = p.load(open(time_exp_model_path, 'rb'))


    price_pred = price_model.predict(features_array.reshape(1, -1))

    new_features = np.insert(features_array, 0, price_pred)

    print(map(lambda x: round(x, 2), new_features))

    time_exp_pred = time_exp_model.predict(new_features.reshape(1, -1))


    return jsonify({'price': price_pred[0], 'time_exp': time_exp_pred[0]})


@app.route('/get_time_exp', methods=['POST'])
def get_time_exp():
    data = request.get_json()
    prices = data.get('prices')

    prices = np.array(prices).reshape(-1, 1)
    prediction = np.array2string(model2.predict(prices).flatten())

    return jsonify(prediction)

@app.route('/form')
def form():
    return render_template('form.html', features=features)



@app.route('/form_ver2')
def form_ver2():
    return render_template('form_ver2.html', features=features)


@app.route('/get_price_ver2', methods=['POST'])
def get_price_ver2():

    form_dict = request.form

    df = pd.DataFrame(request.form, index=[0])

    rooms = df.iloc[0]['rooms']



    #print(rooms)

    return "It's ok"

    #rooms = int(request.form.get('rooms'))
    #print(rooms)
    #features_array = [float(str(value)) for value in request.form.values()]
    #print(features_array)
    #features_array = np.array(features_array).reshape(1, -1)

    #price_model_path, time_exp_model_path = models_dict[rooms]

    #price_model = p.load(open(price_model_path, 'rb'))
    #time_exp_model = p.load(open(time_exp_model_path, 'rb'))

    #price_pred = price_model.predict(features_array.reshape(1, -1))

    #new_features = np.insert(features_array, 0, price_pred)

    #print(new_features)

    #time_exp_pred = time_exp_model.predict(new_features.reshape(1, -1))

    #return jsonify({'price_pred': price_pred[0], 'time_exp_pred': time_exp_pred[0]})


if __name__ == '__main__':
    app.run()







