from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
import numpy as np
import pickle as p
import json


app = Flask(__name__)


features = ['deposit', 'client_fee', 'floor', 'area_total', 'area_living', 'area_kitchen', 'ceiling', 'rooms',
            'is_children_allowed', 'is_pets_allowed', 'has_fridge', 'has_washmach', 'has_internet', 'has_tv',
            'has_room_furniture', 'has_kitchen_furniture', 'has_bath', 'has_rubbish_chute', 'loggias', 'balconies',
            'pass_lifts', 'serv_lifts', 'repair_type', 'window_view', 'latitude', 'longitude', 'build_year', 'square_meter_price',
            'floors_count', 'entrances', 'walls_type_raw', 'beltway_hit', 'beltway_distance', 'region_with_type', 'city_with_type',
            'city_area', 'city_district_with_type', 'metro_distance', 'occupancy_in_percent', 'month_open', 'line_station']


price_studio = p.load(open('models/price_studio.pickle', 'rb'))

time_studio = p.load(open('models/time_studio.pickle', 'rb'))




#Для каждого числа комнат - свои модели
models_dict = {
    0: ('models/price_studio.pickle', 'models/time_studio.pickle'),
    1: ('models/price_one_room.pickle', 'models/time_one_room.pickle'),
    2: ('models/price_two_rooms.pickle', 'models/time_two_rooms.pickle'),
    3: ('models/price_three_rooms.pickle', 'models/time_three_rooms.pickle'),
}


@app.route('/get_price', methods=['POST'])
def get_price():

    data = request.get_json()

    print(data)

    features_dict = data.get('features')

    print(features_dict)

    rooms = features_dict.get('rooms')



    features_array = np.array(list(features_dict.values()))


    price_model_path, time_exp_model_path = models_dict[rooms]

    price_model = p.load(open(price_model_path, 'rb'))
    time_exp_model = p.load(open(time_exp_model_path, 'rb'))


    price_pred = price_model.predict(features_array.reshape(1, -1))

    new_features = np.insert(features_array, 0, price_pred)

    print(new_features)

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
    rooms = int(request.form.get('rooms'))
    print(rooms)
    features_array = [float(str(value)) for value in request.form.values()]
    print(features_array)
    features_array = np.array(features_array).reshape(1, -1)

    price_model_path, time_exp_model_path = models_dict[rooms]

    price_model = p.load(open(price_model_path, 'rb'))
    time_exp_model = p.load(open(time_exp_model_path, 'rb'))

    price_pred = price_model.predict(features_array.reshape(1, -1))

    new_features = np.insert(features_array, 0, price_pred)

    print(new_features)

    time_exp_pred = time_exp_model.predict(new_features.reshape(1, -1))

    return jsonify({'price_pred': price_pred[0], 'time_exp_pred': time_exp_pred[0]})


if __name__ == '__main__':
    app.run()







