from services.DownloadService import DownloadService
from services.RequestService import RequestService
import argparse

from services.UploadService import UploadService

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-u",
        "--user",
        type=str,
        required=True,
        default=None,
        help="Username",
    )
    ap.add_argument(
        "-p",
        "--password",
        type=str,
        required=True,
        default=None,
        help="Password",
    )
    ap.add_argument(
        "-b",
        "--base_url",
        type=str,
        required=True,
        default=None,
        help="Base Artifactory URL",
    )
    ap.add_argument(
        "-r",
        "--repo_uri",
        type=str,
        required=True,
        default=None,
        help="Relative path to main repo directory (for example /repo/eu/abra/primaerp/)",
    )
    ap.add_argument(
        "-y",
        "--year",
        type=int,
        required=False,
        default=None,
        help="If specified, only versions created in this year or later will be taken."
    )
    ap.add_argument(
        "-s",
        "--skip_downloading",
        action="store_true",
        help="Skip the download phase"
    )
    ap.add_argument(
        "-t",
        "--token",
        type=str,
        required=True,
        default=None,
        help="GitHub personal access token (classic) with packages write permission"
    )
    ap.add_argument(
        "-d",
        "--destination_url",
        type=str,
        required=True,
        default=None,
        help="Destination repository URL"
    )
    ap.add_argument(
        "-o",
        "--only_app",
        type=str,
        required=False,
        default=None,
        help="Specify if you want to apply the script to only one application/repository (specify its name, e.g. api-client)."
    )

    args = vars(ap.parse_args())

    request_service = RequestService(
        user=args["user"],
        password=args["password"],
        base_url=args["base_url"],
        repo_uri=args["repo_uri"]
    )

    if not args["skip_downloading"]:
        download_service = DownloadService(request_service, args["year"], args["only_app"])
        download_service.run()
    upload_service = UploadService(args["destination_url"], args["token"], args["only_app"])
    upload_service.run()

