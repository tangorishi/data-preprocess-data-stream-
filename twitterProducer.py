import json
from kafka import KafkaProducer
from tweepy import OAuthHandler, Stream, StreamListener


class TwitterListener(StreamListener):
    def on_data(self, data):
        try:
            producer.send("twitter_covid", json.dumps(data).encode("utf-8"))
            producer.flush()
            return True
        except Exception as e:
            print(e)
            
            return False


    def on_error(self, status_code):
        print(status_code)


access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    api_version=(0, 1, 0),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

t = TwitterListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

stream = Stream(auth, t)
stream.filter(track=["#COVID"])
