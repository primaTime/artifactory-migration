import requests
from requests.auth import HTTPBasicAuth

from schema.Params import Params
from schema.RequestMethod import RequestMethod


class RequestService:

    def __init__(self, user: str, password: str, base_url: str, repo_uri: str):
        self.__user = user
        self.__password = password
        self.__base_url = base_url
        self.__repo_uri = repo_uri

    def get_storage_url(self):
        return self.__base_url + Params.STORAGE_API_URI + self.__repo_uri

    def get_versions_url(self, uri: str):
        return self.get_storage_url() + uri

    def get_files_list_url(self, uri_app_name: str, uri_version: str):
        return self.get_versions_url(uri_app_name) + uri_version

    def get_file_url(self, uri: str):
        return self.__base_url + self.__repo_uri + uri

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

