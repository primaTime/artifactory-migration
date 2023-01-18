import os
from pathlib import Path
from dateutil import parser
from schema.ListItemResponse import ListItemResponse
from schema.Params import Params
from schema.StorageResponse import StorageResponse
from services.RequestService import RequestService
from schema.RequestMethod import RequestMethod
from services.PrintService import PrintService


class DownloadService:
    __request_service: RequestService = None
    __year: int = None

    def __init__(self, request_service: RequestService, year: int = None):
        self.__request_service = request_service
        self.__year = year

    def __create_directory(self, directory: str = ""):
        Path(Params.STORAGE_DIR + directory).mkdir(exist_ok=True)

    def __retrieve_apps(self) -> list[ListItemResponse]:
        data: StorageResponse = self.__request_service.do_json_response(RequestMethod.GET, self.__request_service.get_storage_url())
        return data["children"]

    def __retrieve_versions(self, uri: str) -> list[ListItemResponse]:
        data: StorageResponse = self.__request_service.do_json_response(RequestMethod.GET, self.__request_service.get_versions_url(uri))
        return data["children"]

    def __retrieve_files(self, uri_app_name: str, uri_version: str) -> list[ListItemResponse]:
        data: StorageResponse = self.__request_service.do_json_response(RequestMethod.GET, self.__request_service.get_files_list_url(uri_app_name, uri_version))
        return data["children"]

    def __retrieve_version_meta(self, uri_app_name: str, uri_version: str) -> StorageResponse:
        return self.__request_service.do_json_response(RequestMethod.GET, self.__request_service.get_files_list_url(uri_app_name, uri_version))

    def __retrieve_version_file(self, uri_app_name: str, uri_version: str, uri_file_name: str) -> bytes:
        response = self.__request_service.do(RequestMethod.GET, self.__request_service.get_file_url(uri_app_name+uri_version+uri_file_name))
        return response.content

    def __retrieve_metadata_file(self, uri_app_name: str):
        response = self.__request_service.do(RequestMethod.GET, self.__request_service.get_file_url(uri_app_name+"/maven-metadata.xml"))
        return response.content

    def __download_file(self, local_uri: str, data: bytes):
        with open(Params.STORAGE_DIR + local_uri, "wb") as file:
            file.write(data)

    def __create_apps_dirs(self, apps_list: list[ListItemResponse]):
        for app_meta in apps_list:
            if app_meta["folder"]:
                self.__create_directory(app_meta["uri"])

    def __create_version_files(self, uri_app_name: str, uri_version: str):
        files: list[ListItemResponse] = self.__retrieve_files(uri_app_name, uri_version)
        for file_meta in files:
            self.__download_file(uri_app_name+uri_version+file_meta['uri'], self.__retrieve_version_file(uri_app_name, uri_version, file_meta["uri"]))

    def __create_versions_dirs(self, app_meta: ListItemResponse):
        app_versions: list[ListItemResponse] = self.__retrieve_versions(app_meta["uri"])
        versions: dict[str, StorageResponse] = {}
        for version_meta in app_versions:
            if version_meta["folder"]:
                meta: StorageResponse = self.__retrieve_version_meta(app_meta["uri"], version_meta["uri"])
                created = parser.parse(meta["created"])
                if self.__year is not None and created.year<self.__year:
                    continue
                versions[version_meta["uri"][1:]] = meta

        for version_id, version_meta in versions.items():
            version_uri: str = f"/{version_id}"
            PrintService.print(f"Downloading version {version_uri[1:]}")
            self.__create_directory(app_meta["uri"]+version_uri)
            self.__create_version_files(app_meta["uri"], version_uri)

    def run(self):
        PrintService.h1("Resource downloading")
        self.__create_directory()
        apps_list: list[ListItemResponse] = self.__retrieve_apps()
        self.__create_apps_dirs(apps_list)
        for app_meta in apps_list:
            PrintService.h2(f"App {app_meta['uri'][1:]}")
            self.__create_versions_dirs(app_meta)