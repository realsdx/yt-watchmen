from watchmen.models import Video
from YoutubeWatchmen.celery import app
from django.conf import settings

import googleapiclient.discovery
import googleapiclient.errors
import datetime


@app.task(name='fetch_and_update')
def fetch_youtube_data():
    """ Fetches latest Youtube data with Youtube DataAPI v3"""

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=settings.CURRENT_API_KEY,
        cache_discovery=False)

    request = youtube.search().list(part="snippet",
                                    maxResults=25,
                                    order="date",
                                    publishedAfter="2020-10-21T20:44:39Z",
                                    q="football")
    results = None
    try:
        response = request.execute()
        results = response.get("items", None)
    except googleapiclient.errors.HttpError as e:
        # print("DEBUG ",e.resp.status, e._get_reason())
        if "you have exceeded" in e._get_reason():
            print("WARNING: API Quota exceeded")
            rotate_api_key()
        else:
            print(f"ERROR: {e._get_reason()}")
            return
    except Exception as e:
        print(f"ERROR: {e._get_reason()}")
        return

    # if no data received return
    if not results:
        print("DEBUG: Got no data")
        return

    count = 0
    for result in results:
        video_id = result["id"]["videoId"]
        title = result["snippet"]["title"]
        description = result["snippet"]["description"]
        published_at = result["snippet"]["publishedAt"]
        thumbnail_url = result["snippet"]["thumbnails"]["default"]["url"]

        created = update_to_db(video_id, title, description, published_at,
                               thumbnail_url)

        # if data is not created
        if not created:
            continue
        count += 1
    print(f"{count} new videos added")


def update_to_db(video_id, title, description, published_at, thumbnail_url):
    """ Updates data to the database. Returns true is updated otherwise false"""

    try:
        published_datetime = datetime.datetime.strptime(
            published_at, "%Y-%m-%dT%H:%M:%SZ")

        obj, created = Video.objects.get_or_create(
            video_id=video_id,
            title=title,
            description=description,
            published_at=published_datetime,
            thumbnail_url=thumbnail_url)
    except Exception as e:
        print("ERROR: ", e)

    return created


def rotate_api_key():
    api_keys = settings.YT_DATA_API_KEYS
    api_key_in_use = settings.CURRENT_API_KEY
    print(f"Current API KEY: {api_key_in_use}")

    # rotate only when more than one api key
    if len(api_keys) > 1:
        ind = api_keys.index(api_key_in_use)
        ind = (ind + 1) % len(api_keys)
    else:
        print(
            "WARNING: No API Key Rotation performed. As there is only one key")
        return

    settings.CURRENT_API_KEY = api_keys[ind]
    print(f"Updated KEY: {settings.CURRENT_API_KEY}")
