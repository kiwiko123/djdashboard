import json
import urllib.parse
import urllib.request
from django.utils.decorators import method_decorator


class verify_success:
    """
    Function decorator to verify that the Hue API response is successful.

    Expected successful response is something like:
    [{'success': {'/lights/6/state/on': False}}]

    If success is not found, raises ValueError.
    Proceeds to return the original result of the decorated function.

    When decorating a method, use in conjunction with Django's method_decorator.
    """
    def __init__(self, function: callable):
        self._f = function

    def __call__(self, *args, **kwargs):
        response = self._f(*args, **kwargs)
        if not any('success' in entry for entry in response):
            raise ValueError('failed to receive success status message; received: \n{0}'.format(response))
        return response


class LightController:
    """
    Class containing methods to interact with the Philips Hue bridge via API calls.
    """

    def __init__(self, bridge_ip_address: str, hue_api_key: str):
        self._bridge_ip_address = bridge_ip_address
        self._api_key = hue_api_key


    def _form_api_call(self, command: str) -> str:
        """
        Returns a string of the URL required to make an API call.

        Example:
        To get all lights, the argument would be 'lights', returning:
        'http://{BRIDGE.IP.ADDRESS}/api/{API-USERNAME}/lights'
        """
        return 'http://{0}/api/{1}/{2}'.format(self._bridge_ip_address, self._api_key, command)


    def get(self, command: str) -> dict:
        """
        Issues an HTTP GET request using command.
        Command should be a Hue API command only - the URL will be automatically built by the method.
        Deserializes the response and returns a dictionary containing the result.
        """
        url = self._form_api_call(command)
        with urllib.request.urlopen(url) as response:
            content = response.read()
            content = content.decode(encoding='utf-8')
            return json.loads(content)


    @method_decorator(verify_success)
    def toggle(self, light_number: int, light_data: dict) -> [dict]:
        """
        Toggles the given light on/off.
        light_number is an real integer corresponding to the light, as returned by the Hue API.
        light_data is the corresponding serialized JSON dictionary for that light.

        Toggling lights via the API expects an HTTP PUT request.
        Returns the response from the API as a serialized JSON object.

        Successful response should be something like:
        [{'success': {'/lights/6/state/on': False}}]
        """
        is_light_on = light_data['state']['on']
        parameters = {'on': not is_light_on}
        payload = json.dumps(parameters)
        payload = bytes(payload, encoding='utf-8')
        url = 'http://{0}/api/{1}/lights/{2}/state'.format(self._bridge_ip_address, self._api_key, light_number)
        request = urllib.request.Request(url)
        request.get_method = lambda: 'PUT'

        with urllib.request.urlopen(request, data=payload) as response:
            content = response.read()
            content = content.decode(encoding='utf-8')
            return json.loads(content)


    def lights(self) -> [dict]:
        """
        Returns a list of all discovered lights, where each "light" is represented by its dictionary JSON response.
        """
        response = self.get('lights')
        result = []
        for number, info in response.items():
            info['number'] = int(number)
            result.append(info)
        return result