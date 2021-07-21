import requests
from requests.exceptions import HTTPError, ConnectionError
from resources.functions import validate_protocol


class WordPressAPI:
    """ WP API Object Definition """

    def __init__(self, domain, username, password, protocol="https", namespace="wp-json"):
        """ Object constructor """
        self.domain = domain
        self.username = username
        self.password = password
        self.protocol = protocol
        self.namespace = namespace
        self.connected = False
        self.headers = {
            "Content-Type": "application/json"
        }

    def __repr__(self):
        """ Object representation (for developers) """
        return f"WordPressAPI({self.domain}, {self.username}, {self.password})"

    def __str__(self):
        """ String representation """
        return f"WordPressAPI Object : {self.url}"

    @property
    def url(self):
        """ URL Builder for the API """
        return f"{self.protocol}://{self.domain}/{self.namespace}"

    @property
    def protocol(self):
        """ Getter for the protocol so that it's read only """
        return self.__protocol

    @protocol.setter
    def protocol(self, proto):
        """ Setter for the protocol verifying it's correct (either http or https) """
        self.__protocol = validate_protocol(proto)

    @staticmethod
    def parse_json(response):
        return response.json()

    @staticmethod
    def parse_wp_error(response):
        data = response.json()
        print(f"STATUS={data['data']['status']}\nCODE={data['code']}\nMESSAGE={data['message']}")

    def build_authentication_url(self):
        return f"{self.url}/jwt-auth/v1/token?username={self.username}&password={self.password}"

    def connect(self):
        """ Connect to the actual WP API. Returns None if connection wasn't successful """
        try:
            response = requests.post(self.build_authentication_url(), headers=self.headers)
            response.raise_for_status()
            self.connected = True
            self.headers.update({"Authorization": f"Bearer {self.parse_json(response)['token']}"})
            return response
        except HTTPError as error:
            self.parse_wp_error(error.response)
        except ConnectionError as error:
            print(error)

    def get(self, endpoint, data=None, get_response=False):
        """ Attempt a GET action. Returns None if request wasn't successful or raise Exception if attempted to GET when API is not connected """
        try:
            if self.connected:
                response = requests.get(self.url + endpoint, params=data, headers=self.headers)
                response.raise_for_status()
                return response if get_response else self.parse_json(response)
            else:
                raise Exception("API is not connected!")

        except HTTPError as error:
            self.parse_wp_error(error.response)
        except ConnectionError as error:
            print(error)


    def post(self, endpoint, data, get_response=False):
        """ Attempt a POST action. Returns None if request wasn't successful or raise Exception if attempted to GET when API is not connected """
        try:
            if self.connected:
                response = requests.post(self.url + endpoint, data=data, headers=self.headers)
                response.raise_for_status()
                return response if get_response else self.parse_json(response)
            else:
                raise Exception("API is not connected!")

        except HTTPError as error:
            self.parse_wp_error(error.response)
        except ConnectionError as error:
            print(error)

    # TODO: Need to implement other methods (PUT, DELETE, etc.)
