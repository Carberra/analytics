import argparse
import datetime as dt
import json
import os
from pathlib import Path

import google.oauth2.credentials
import google_auth_oauthlib.flow
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DATA_PATH = Path("../data")
SECRET_FILE = DATA_PATH / "secrets.json"

API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"
SCOPES = (
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
)
METRICS = (
    "views",
    "redViews",
    "comments",
    "likes",
    "dislikes",
    "videosAddedToPlaylists",
    "videosRemovedFromPlaylists",
    "shares",
    "estimatedMinutesWatched",
    "estimatedRedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "annotationClickThroughRate",
    "annotationCloseRate",
    "annotationImpressions",
    "annotationClickableImpressions",
    "annotationClosableImpressions",
    "annotationClicks",
    "annotationCloses",
    "cardClickRate",
    "cardTeaserClickRate",
    "cardImpressions",
    "cardTeaserImpressions",
    "cardClicks",
    "cardTeaserClicks",
    "subscribersGained",
    "subscribersLost",
    # "uniques",
    "estimatedRevenue",
    "estimatedAdRevenue",
    "grossRevenue",
    "estimatedRedPartnerRevenue",
    "monetizedPlaybacks",
    "playbackBasedCpm",
    "adImpressions",
    "cpm",
)


class InvalidArgument(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser(
        description="Get YouTube analytics reports.",
        epilog=(
            "You need a Google Developers project with the YouTube Analytics API enabled to run this. "
            "If you don't have that, you can find instructions at https://github.com/Carberra/analytics."
        ),
    )
    parser.add_argument(
        "-f",
        "--filename",
        default=f"analytics-{dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv",
        help="The filename for the report. Defaults to 'analytics-YYYY-MM-DD-HH-MM-SS.csv'.",
    )
    parser.add_argument(
        "-s",
        "--start-date",
        default="2005-02-14",
        help="The start date for the report in YYYY-MM-DD format. Defaults to 2005-02-14.",
    )
    parser.add_argument(
        "-e",
        "--end-date",
        default=dt.date.today().strftime("%Y-%m-%d"),
        help="The start date for the report in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument(
        "-m",
        "--metrics",
        default=",".join(METRICS),
        help="A comma-seperated list of metrics to use. View the source code for a list of available metrics. Defaults to all.",
    )
    args = parser.parse_args()

    if not args.filename.endswith((".json", ".csv")):
        raise InvalidArgument("You can only save the report as a JSON or a CSV.")

    args.filetype = args.filename.split(".")[-1]

    lowest = dt.datetime(2005, 2, 14).date()
    highest = dt.date.today()
    sd = dt.datetime.strptime(args.start_date, "%Y-%m-%d").date()
    ed = dt.datetime.strptime(args.end_date, "%Y-%m-%d").date()

    if sd < lowest or ed < lowest:
        raise InvalidArgument("You cannot set a date before 14 Feb 2005.")

    if sd > dt.date.today() or ed > dt.date.today():
        raise InvalidArgument("You cannot set a date in the future.")

    if any(f := list(filter(lambda m: m not in METRICS, args.metrics.split(",")))):
        raise InvalidArgument(f"One or more invalid metrics were passed: {','.join(f)}.")

    return args


def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_analytics(service, save_func, **kwargs):
    response = service.reports().query(**kwargs).execute()
    save_func(response)


def as_json(response):
    with open(DATA_PATH / args.filename, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=4, ensure_ascii=False)


def as_csv(response):
    df = pd.DataFrame()
    df = df.append(response["rows"])
    df.columns = [c["name"] for c in response["columnHeaders"]]
    df.to_csv(DATA_PATH / args.filename)


if __name__ == "__main__":
    os.environ["OAUTH_INSECURE_TRANSPORT"] = "1"

    args = get_args()
    service = get_service()
    get_analytics(
        service,
        {"csv": as_csv, "json": as_json}[args.filetype],
        ids="channel==MINE",
        startDate=args.start_date,
        endDate=args.end_date,
        metrics=args.metrics,
        dimensions="day",
        sort="day",
    )
