import requests
from requests.auth import HTTPBasicAuth
from schema.RequestMethod import RequestMethod


class RequestService:
    STORAGE_API_URI: str = "/api/storage"

    __user: str = ""
    __password: str = ""
    __base_url: str = ""
    __repo_uri: str = ""

    def __init__(self, user: str, password: str, base_url: str, repo_uri: str):
        self.__user = user
        self.__password = password
        self.__base_url = base_url
        self.__repo_uri = repo_uri

    def get_storage_url(self):
        return self.__base_url + self.STORAGE_API_URI + self.__repo_uri

    def do(self, method: RequestMethod, url: str) -> requests.Response:
        try:
            r = requests.request(
                method=method.value,
                url=url,
                auth=HTTPBasicAuth(self.__user, self.__password)
            )
            return r
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def do_json_response(self, method: RequestMethod, url: str) -> dict:
        return self.do(method, url).json()

