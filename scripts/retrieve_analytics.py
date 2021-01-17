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


def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_analytics(service, save_func, filename="analytics", **kwargs):
    response = service.reports().query(**kwargs).execute()
    save_func(response, filename)


def as_json(response, filename):
    with open(DATA_PATH / f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(response, f, indent=4, ensure_ascii=False)


def as_csv(response, filename):
    df = pd.DataFrame()
    df = df.append(response["rows"])
    df.columns = [c["name"] for c in response["columnHeaders"]]
    df.to_csv(DATA_PATH / f"{filename}.csv")


if __name__ == "__main__":
    os.environ["OAUTH_INSECURE_TRANSPORT"] = "1"

    service = get_service()
    get_analytics(
        service,
        as_csv,
        filename="example_carberra_2020",
        ids="channel==MINE",
        startDate="2020-01-01",
        endDate="2020-12-31",
        metrics=",".join(METRICS),
        dimensions="day",
        sort="day",
    )
