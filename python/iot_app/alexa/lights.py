from flask import render_template
from flask_ask import statement
from iot_app.assets.web_assets import light_img
from iot_app.iot.lights import LightManager, Light

from typing import Optional, List


class Room:
    ALL = 'all'
    LOUNGE = 'lounge'
    BEDROOM = 'bedroom'


class LightCheckResult:

    def __init__(self, is_successful: bool, failure_cause: Optional[statement] = None,
                 lights_to_use: Optional[List[Light]] = None):
        self.__is_successful = is_successful
        self.__cause = failure_cause
        self.__lights = lights_to_use

    def is_successful(self) -> bool:
        return self.__is_successful

    def get_failure_cause(self) -> statement:
        return self.__cause

    def get_lights(self) -> List[Light]:
        return self.__lights


lm = LightManager.instance()


def start_effect(room, effect):
    return LightAction(render_template('card_title_lights'), light_img).start_effect(room, effect)


def stop_effect(room):
    return LightAction(render_template('card_title_lights'), light_img).stop_effect(room)


class LightAction:
    def __init__(self, card_title: str, card_img: str):
        self.card_title = card_title
        self.card_img = card_img

    def start_effect(self, room, effect) -> statement:
        check_result = self.__check_lights(room)
        if not check_result.is_successful():
            return check_result.get_failure_cause()

        for light in check_result.get_lights():
            light.set_effect(effect, {})

    def stop_effect(self, room):
        check_result = self.__check_lights(room)
        if not check_result.is_successful():
            return check_result.get_failure_cause()

        for light in check_result.get_lights():
            light.set_effect(None)
        return self.__stmt_stop_effect()

    def __card_effect_ok(self):
        return self.card_title, render_template('effect_start_card'), self.card_img

    def __card_no_lights(self):
        return self.card_title, render_template('no_lights'), self.card_img

    def __card_no_default_lights(self):
        return self.card_title, render_template('no_default_lights'), self.card_img

    def __card_no_such_light(self, light_name):
        return self.card_title, render_template('no_such_light').format(light_name), self.card_img

    def __card_stop_effect(self):
        return self.card_title, render_template('effect_stop_card'), self.card_img

    def __stmt_effect_ok(self):
        return statement(render_template('effect_start')).standard_card(*self.__card_effect_ok())

    def __stmt_no_lights(self):
        return statement(render_template('no_lights')).standard_card(*self.__card_no_lights())

    def __stmt_no_default_lights(self):
        return statement(render_template('no_default_lights')).standard_card(*self.__card_no_default_lights())

    def __stmt_no_such_light(self, light_name):
        return statement(render_template('no_such_light').format(
            light_name)).standard_card(*self.__card_no_such_light(light_name))

    def __stmt_stop_effect(self):
        return statement('OK').standard_card(*self.__card_stop_effect())

    def __check_lights(self, room):
        all_lights = lm.get_all_lights()
        if len(all_lights) == 0:
            return LightCheckResult(is_successful=False, failure_cause=self.__stmt_no_lights())

        if room == Room.ALL:
            return LightCheckResult(is_successful=True, lights_to_use=all_lights)

        if room is None:
            if len(lm.default_lights) == 0:
                return LightCheckResult(is_successful=False, failure_cause=self.__stmt_no_default_lights())
            return LightCheckResult(is_successful=True, lights_to_use=lm.default_lights)

        light = lm.get_light_by_name(room)
        if light is None:
            return LightCheckResult(is_successful=False, failure_cause=self.__stmt_no_such_light(room))
        return LightCheckResult(is_successful=True, lights_to_use=[light])
