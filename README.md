# Twitter Data Pipeline: Technical Documentation

## Overview

This pipeline is designed to consume Twitter data and extract meaningful insights on various topics. It integrates the following technologies: Twitter API, Apache Kafka, MongoDB, and Tableau. Each component has been chosen for its ability to handle specific tasks within the pipeline efficiently.

## Architecture

1. **Twitter API**: Used to obtain real-time tweets based on specified criteria.
2. **Apache Kafka**: Serves as the messaging system to stream data between components.
3. **MongoDB**: A NoSQL database that stores tweets for subsequent analysis.
4. **Tableau**: A powerful visualization tool used to create insightful dashboards.

## Detailed Components and Flow

### 1. Twitter API

The Twitter API provides a robust interface to access Twitter data, including tweets, user profiles, and trends. The API allows for the following:

- **Authentication**: OAuth 2.0 is used to securely connect and authenticate API requests.
- **Data Retrieval**: Tweets are fetched in real-time based on specified keywords, hashtags, user accounts, or geographical locations.

### 2. Apache Kafka

Apache Kafka is a distributed streaming platform that is used for building real-time data pipelines. In this pipeline, Kafka serves the following purposes:

- **Producer**: The Twitter API client acts as a producer, sending fetched tweets to Kafka topics.
- **Broker**: Kafka brokers manage the storage and transmission of the tweet streams.
- **Consumer**: Various downstream applications, including the data storage system, act as consumers that process the incoming tweet streams.

Kafka provides high-throughput and fault-tolerant messaging, ensuring that our pipeline remains robust and scalable.

### 3. MongoDB

MongoDB is a NoSQL database well-suited for storing large volumes of unstructured data such as tweets. The database stores the tweet data received from Kafka, providing the following features:

- **Flexible Schema**: The JSON-like document model of MongoDB accommodates the varied structure of tweet data.
- **Scalability**: MongoDB’s ability to scale horizontally allows for the handling of high-velocity data streams.
- **Indexing and Querying**: Efficient querying and indexing facilitate quick retrieval and analysis of stored tweets.

### 4. Tableau

Tableau is a powerful tool for data visualization, enabling the creation of interactive and meaningful dashboards. With Tableau, the pipeline achieves the following:

- **Data Connection**: Connects directly to MongoDB to fetch the latest data.
- **Visualization**: Generates dynamic and interactive visualizations such as charts, graphs, and maps to represent tweet data.
- **Insights**: Provides capabilities to drill down into data, helping to uncover trends and insights.

## Data Flow

1. **Data Ingestion**: Tweets are ingested from Twitter using the Twitter API.
2. **Data Streaming**: Ingested tweets are sent to Kafka as messages.
3. **Data Storage**: Kafka consumers retrieve the messages and store them in MongoDB.
4. **Data Visualization**: Tableau connects to MongoDB to visualize the stored tweet data.

## Installation and Setup

### Prerequisites

- **Twitter Developer Account**: Required to access the Twitter API.
- **Kafka Installation**: A running instance of Apache Kafka.
- **MongoDB Installation**: A running instance of MongoDB.
- **Tableau Installation**: Tableau Desktop or Tableau Server for creating visualizations.

### Step-by-Step Guide

1. **Twitter API Setup**:
   - Create a Twitter Developer account and set up a project to obtain API keys.
   - Configure OAuth 2.0 authentication.

2. **Kafka Setup**:
   - Download and install Apache Kafka.
   - Configure Kafka brokers and create necessary topics for tweet streams.

3. **MongoDB Setup**:
   - Download and install MongoDB.
   - Configure MongoDB and set up collections for storing tweets.

4. **Pipeline Configuration**:
   - Develop a Python script or use a Kafka connector to fetch tweets from the Twitter API and send them to Kafka.
   - Implement Kafka consumers to read messages from Kafka topics and write them to MongoDB.
   
5. **Tableau Setup**:
   - Connect Tableau to MongoDB.
   - Create visualizations based on the tweet data stored in MongoDB.

## Example Code

### Twitter API to Kafka Producer

```python
import tweepy
from kafka import KafkaProducer
import json

# Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# Kafka configuration
kafka_topic = 'twitter_topic'
kafka_broker = 'localhost:9092'

# Setup Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Kafka producer
producer = KafkaProducer(bootstrap_servers=[kafka_broker], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet = {
            'text': status.text,
            'created_at': str(status.created_at),
            'user': status.user.screen_name
        }
        producer.send(kafka_topic, value=tweet)

# Stream tweets
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['keyword'])

