from watchmen.models import Video

import googleapiclient.discovery
import datetime

apiKey = "AIzaSyDOq977tqm05ZW4IjHJm1fBpiucT3HghfI"


def fetch_youtube_data():
    """ Fetches latest Youtube data with Youtube DataAPI v3"""

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name,
                                              api_version,
                                              developerKey=apiKey)

    request = youtube.search().list(part="snippet",
                                    maxResults=25,
                                    order="date",
                                    publishedAfter="2020-10-21T20:44:39Z",
                                    q="football")
    response = request.execute()
    results = response.get("items", None)

    for result in results:
        video_id = result["id"]["videoId"]
        title = result["snippet"]["title"]
        description = result["snippet"]["description"]
        published_at = result["snippet"]["publishedAt"]
        thumbnail_url = result["snippet"]["thumbnails"]["default"]["url"]

        print(f"{video_id} {published_at}\n")
        created = update_to_db(video_id, title, description, published_at, thumbnail_url)
        if not created:
            break
        print(f"Created on db: {video_id}")



def update_to_db(video_id, title, description, published_at, thumbnail_url):
    """ Updates data to the database. Returns true is updated otherwise false"""

    try:
        published_datetime = datetime.datetime.strptime(published_at,
                                                        "%Y-%m-%dT%H:%M:%SZ")

        obj, created = Video.objects.get_or_create(
            video_id=video_id,
            title=title,
            description=description,
            published_at=published_datetime,
            thumbnail_url=thumbnail_url
        )
    except Exception as e:
        print("ERROR ==== ", e)

    return created



if __name__ == "__main__":
    fetch_youtube_data()