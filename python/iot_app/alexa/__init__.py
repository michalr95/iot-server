from iot_app.assets.web_assets import pi_img

from flask_ask.models import _Response
from flask import render_template


def with_card(response: _Response, card_text: str, card_img=pi_img):
    """
    Decorates Alexa response with a card (visible in the Alexa app).
    :param response: Response object to decorate.
    :param card_text: Text to display on the card.
    :param card_img: Image to display on the card. Raspberry PI logo by default.
    :return: Decorated response object
    """
    card_title = render_template('card_title_pi')
    return response.standard_card(card_title, card_text, card_img)

from .builtin_intents import welcome
from .lights import start_effect, stop_effect
from .sensor_readings import sensor_readings