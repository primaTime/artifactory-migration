from services.DownloadService import DownloadService
from services.RequestService import RequestService
import argparse

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

    args = vars(ap.parse_args())

    request_service = RequestService(
        user=args["user"],
        password=args["password"],
        base_url=args["base_url"],
        repo_uri=args["repo_uri"]
    )

    download_service = DownloadService(request_service)
    download_service.run()

