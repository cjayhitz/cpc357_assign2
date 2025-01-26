import pymongo
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["smarthome"]
collection = db["iot"]

# MQTT configuration
mqtt_broker_address = "35.198.230.42"  # Replace with your MQTT broker IP
mqtt_topics = ["iot", "iot/pir", "iot/temp"]  # List of topics to subscribe to

# Callback for successful connection
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Successfully connected to MQTT broker.")
        for topic in mqtt_topics:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")

# Callback for incoming messages
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Received message from {message.topic}: {payload}")

    # Add a timestamp and store the message in MongoDB
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    document = {"timestamp": timestamp, "topic": message.topic, "data": payload}
    collection.insert_one(document)
    print("Data ingested into MongoDB.")

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker_address, 1883, 60)

# Start listening for messages
client.loop_forever()
