import json
import urllib.request


class LightController:

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


    def lights(self) -> [dict]:
        """
        Returns a list of all discovered lights, where each "light" is represented by its dictionary JSON response.
        """
        result = self.get('lights')
        return list(result.values())