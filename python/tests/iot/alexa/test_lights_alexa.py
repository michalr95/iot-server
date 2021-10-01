"""import sys
from os.path import dirname, join, abspath
from unittest import main, mock, TestCase
import yaml

lights_module = mock.MagicMock()
lights_module.LightManager = mock.MagicMock()
sys.modules['iot_app.iot.lights'] = lights_module
from iot_app.alexa.alexa import LightAction


class LightsAlexaTest(TestCase):

    def setUp(self):
        self.light_manager = mock.MagicMock()
        self.light_manager.get_default_room.return_value = 'bedroom'
        self.light_manager.get_all_lights.return_value = ['bedroom', 'kitchen', 'lounge']
        self.light_manager.get_light_by_name.side_effect = self.get_light_by_name

        test_dir = dirname(__file__)
        self.templates_file = open(abspath(join(test_dir, '../templates.yaml')))
        self.templates = yaml.load(self.templates_file, Loader=yaml.SafeLoader)

    def tearDown(self):
        self.templates_file.close()

    def render_effect(self, key):
        return self.templates[key]

    def get_light_by_name(self, name):
        for light_name in self.light_manager.get_all_lights():
            if name == light_name:
                return light_name
        return None

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_start_disco_no_lights_found(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect
        self.light_manager.get_all_lights.return_value = []

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').start_disco(room=None)

        # Verify
        r = response._response
        output_speech = r['outputSpeech']['text']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.start_disco.assert_not_called()
        assert 'Sorry. No lights are currently connected.' == output_speech
        assert 'PlainText' == text_type
        assert 'Sorry. No lights are currently connected.' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_start_disco_no_such_light(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect
        self.light_manager.get_light_by_name.side_effect = self.get_light_by_name

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').start_disco(room='porch')
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['text']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.start_disco.assert_not_called()
        assert 'I\'m afraid the light called porch is not available' == output_speech
        assert 'PlainText' == text_type
        assert 'I\'m afraid the light called porch is not available' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_start_disco_default_not_available(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect
        self.light_manager.get_all_lights.return_value = ['kitchen', 'lounge']

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').start_disco(room=None)
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['text']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.start_disco.assert_not_called()
        assert 'I\'m afraid the light called bedroom is not available' == output_speech
        assert 'PlainText' == text_type
        assert 'I\'m afraid the light called bedroom is not available' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_start_disco_default_exists(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').start_disco(room=None)
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['ssml']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.start_disco.assert_any_call()
        assert 'Starting disco. Have fun!' in output_speech
        assert 'SSML' == text_type
        assert 'Started disco lights' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_start_disco_custom_room_exists(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').start_disco(room='lounge')
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['ssml']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.start_disco.assert_called_once_with('lounge')
        assert 'Starting disco. Have fun!' in output_speech
        assert 'SSML' == text_type
        assert 'Started disco lights' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_start_disco_everywhere(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').start_disco(room='everywhere')
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['ssml']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.start_disco.assert_called_once_with('bedroom', 'kitchen', 'lounge')
        assert 'Starting disco. Have fun!' in output_speech
        assert 'SSML' == text_type
        assert 'Started disco lights' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_stop_disco_all_by_default(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').stop_flow(room=None)
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['text']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.stop_flow.assert_called_once_with('bedroom', 'kitchen', 'lounge')
        assert 'OK' in output_speech
        assert 'PlainText' == text_type
        assert 'Stopped disco lights' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_stop_disco_custom_room(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').stop_flow(room='lounge')
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['text']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.stop_flow.assert_called_once_with('lounge')
        assert 'OK' in output_speech
        assert 'PlainText' == text_type
        assert 'Stopped disco lights' == card_text

    @mock.patch('iot_app.alexa.alexa.render_template')
    def test_stop_disco_no_such_room(self, mock_render):
        # Setup
        mock_render.side_effect = self.render_effect

        # Exercise
        response = LightAction(light_manager=self.light_manager,
                               card_title='Card title', card_img='Card image').stop_flow(room='porch')
        # Verify
        r = response._response
        output_speech = r['outputSpeech']['text']
        text_type = r['outputSpeech']['type']
        card_text = r['card']['text']

        self.light_manager.stop_flow.assert_not_called()
        assert 'I\'m afraid the light called porch is not available' in output_speech
        assert 'PlainText' == text_type
        assert 'I\'m afraid the light called porch is not available' == card_text

    if __name__ == '__main__':
        main()"""



