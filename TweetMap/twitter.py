from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import properties
from Map.scripts import elasticsearch_script

consumer_key, consumer_secret, access_token, access_secret = properties.getTwitterCredentials()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

id = 0


class listener(StreamListener):

    def on_data(self, data):
        global id
        tweet = json.loads(data)
        try:
            print(tweet["coordinates"]["coordinates"])
        except:
            pass
        else:
            json_data = {}
            json_data["text"] = tweet["text"]
            json_data["coordinates"] = tweet["coordinates"]["coordinates"]
            elasticsearch_script.storeToElasticsearch(id, json.dumps(json_data))
            id += 1
            print(json_data)
        return (True)

    def on_error(self, status):
        print(status)


def get_twitter_stream():
    try:
        twitterStream = Stream(auth, listener())
        twitterStream.filter(locations=[-180, -90, 180, 90])
    except:
        pass


if __name__ == "__main__":
    get_twitter_stream()
