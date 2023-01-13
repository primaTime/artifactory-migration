from schema.ListItemResponse import ListItemResponse
from schema.StorageResponse import StorageResponse
from services.RequestService import RequestService
from schema.RequestMethod import RequestMethod


class DownloadService:
    __request_service: RequestService = None

    def __init__(self, request_service: RequestService):
        self.__request_service = request_service

    def __retrieve_apps(self) -> list[ListItemResponse]:
        data: StorageResponse = self.__request_service.do_json_response(RequestMethod.GET, self.__request_service.get_storage_url())
        return data["children"]

    def run(self):
        apps_list: list[ListItemResponse] = self.__retrieve_apps()
        print("")