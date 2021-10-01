"""
Module for handling built-in Alexa intents. Examples of built-in intents are:
- Stop (running this Alexa skill)
- Cancel (current interaction with the skill)
- Help
- Fallback (utterance not matching any intent)

Only the "stop" intent must be implemented, handling other intents is optional.
However, Amazon recommends that all built-in intents are implemented.
"""

from iot_app.alexa import with_card

from flask import render_template
from flask_ask import question, statement


def welcome():
    question_text = render_template('welcome')
    return with_card(question(question_text))


def help_():
    help_speech = render_template('help_speech')
    help_card_text = render_template('help_card_text')
    return with_card(statement(help_speech), help_card_text)
