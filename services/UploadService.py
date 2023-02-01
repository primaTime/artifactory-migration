import os
import subprocess
from pathlib import Path

from schema.ArtifactData import ArtifactData
from schema.Params import Params
from services.PrintService import PrintService
from utils.CommandBuilder import CommandBuilder


class UploadService:

    def __init__(self, destination_url: str, token: str, only_app: str = None):
        self.__destination_url = destination_url
        self.__token = token
        self.__only_app = only_app

    def __generate_upload_command(self, pom: str):
        return CommandBuilder()\
            .add_argument("mvn") \
            .add_argument("deploy:deploy-file") \
            .add_mvn_argument("pomFile", pom) \
            .add_mvn_argument("url", self.__destination_url) \
            .add_mvn_argument("repositoryId", "github") \
            .add_mvn_argument("token", self.__token)

    def __upload(self, command_builder: CommandBuilder):
        with subprocess.Popen(command_builder.build(), stdout=subprocess.PIPE) as proc:
            PrintService.print("Command: {}".format(subprocess.list2cmdline(proc.args)))
            print(proc.stdout.read())

    def __process_version(self, version_path: str, version: str):
        PrintService.print(f"Processing version {version}...")
        data: ArtifactData = {}
        for file_name in os.listdir(version_path):
            file_path: str = os.path.join(version_path, file_name)
            if not os.path.isfile(file_path):
                continue
            file_extension: str = Path(file_name).suffix
            if "pom" in file_extension:
                data["pom"] = file_path
            elif "jar" in file_extension:
                if "sources" in file_name:
                    data["sources"] = file_path
                elif "javadoc" in file_name:
                    data["javadoc"] = file_path
                elif "with-dependencies" in file_name:
                    data["jar_with_dependencies"] = file_path
                else:
                    data["jar"] = file_path
            elif "war" in file_extension:
                data["war"] = file_path
            elif "zip" in file_extension:
                data["zip"] = file_path

        try:
            if "pom" not in data:
                raise ValueError("Pom file not found")

            builder = self.__generate_upload_command(data["pom"])

            file_arg: str = "file"
            if "jar" in data or "war" in data or "zip" in data:
                if "jar" in data:
                    builder.add_mvn_argument(file_arg, data["jar"])
                elif "war" in data:
                    builder.add_mvn_argument(file_arg, data["war"])
                elif "zip" in data:
                    builder.add_mvn_argument(file_arg, data["zip"])
            else:
                builder.add_mvn_argument(file_arg, data["pom"])

            if "sources" in data:
                builder.add_mvn_argument("sources", data["sources"])
            if "javadoc" in data:
                builder.add_mvn_argument("javadoc", data["javadoc"])

            self.__upload(builder)

            # Uploading a jar file with dependencies does not work this way.
            #if "jar_with_dependencies" in data:
            #    builder\
            #        .remove_mvn_argument("file")\
            #        .remove_mvn_argument("sources")\
            #        .remove_mvn_argument("javadoc")\
            #        .add_mvn_argument("file", data["jar_with_dependencies"])
            #    self.__upload(builder)


        except ValueError as e:
            PrintService.error(e.args[0])

        PrintService.line()


    def __process_app(self, app_name: str):
        path: str = os.path.join(Params.STORAGE_DIR, app_name)
        for version in os.listdir(path):
            version_path: str = os.path.join(path, version)
            if not os.path.isdir(version_path):
                continue
            self.__process_version(version_path, version)

    def run(self):
        PrintService.h1("Artifacts deploying")
        for app_name in os.listdir(Params.STORAGE_DIR):
            if not os.path.isdir(os.path.join(Params.STORAGE_DIR, app_name)):
                continue
            if self.__only_app is not None and app_name!=self.__only_app:
                continue
            PrintService.h2(f"App {app_name}")
            self.__process_app(app_name)