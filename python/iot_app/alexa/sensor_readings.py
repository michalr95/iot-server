from iot_app.assets.web_assets import pi_img, temp_img, humidity_img
from iot_app.db.sensor_readings import get_last_temp, get_last_humidity
from iot_app.alexa import with_card

from flask import render_template
from flask_ask import statement


# Slot mappings
class SensorType:
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'


def sensor_readings(sensor):
    card_title = render_template('card_title_pi')

    if sensor is None:
        answer = render_template('temp_and_humidity').format(get_last_temp(), get_last_humidity())
        return with_card(statement(answer), answer, pi_img)

    if sensor == SensorType.TEMPERATURE:
        answer = render_template('temp').format(get_last_temp())
        return with_card(statement(answer), answer, temp_img)

    answer = render_template('humidity').format(get_last_humidity())
    return with_card(statement(answer), answer, humidity_img)
