import json
from google.cloud import pubsub_v1
from controllers.document_controller import DocumentController

# Configuration
solr_url = 'http://34.128.126.100:8983/solr'
solr_collection = 'homecollection'
project_id = 'your-gcp-project-id'
subscription_id = 'your-subscription-id'

# Initialize document controller
document_controller = DocumentController(solr_url, solr_collection)

# Initialize Pub/Sub subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received message: {message}")
    try:
        data = json.loads(message.data.decode('utf-8'))
        action = data.get('action')
        document_data_list = data.get('document_data_list')
        document_id = data.get('document_id')

        if action == 'create':
            document_controller.create_document(document_data_list)
        elif action == 'update':
            document_ids = [doc.get('id') for doc in document_data_list]
            document_controller.update_documents(document_ids, document_data_list)
        elif action == 'delete':
            document_controller.delete_document(document_id)
        else:
            print(f"Unknown action: {action}")

        message.ack()
    except Exception as e:
        print(f"Error processing message: {e}")

# Subscribe to the subscription
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

# Keep the main thread alive to listen for messages
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
