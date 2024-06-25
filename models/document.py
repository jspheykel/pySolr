import json
import pysolr

class Document:
    def __init__(self, solr_url, collection_name):
        self.solr_url = solr_url
        self.collection_name = collection_name
        self.solr = pysolr.Solr(f'{solr_url}/{collection_name}')

    def test_connection(self):
        try:
            response = self.solr.ping()
            response_data = json.loads(response)
            if response_data.get('status') == "OK":
                return {"status": True, "code": 202, "msg": "Connection to Solr server successful!"}
            else:
                return {"status": False, "code": 404, "msg": "Failed to connect to Solr server. Check Solr health and configuration."}
        except Exception as e:
            return {'success': False, "code": 400, 'msg': f'Error pinging Solr server: {str(e)}'}

    def read(self):
        try:
            results = self.solr.search(q="*:*", rows=10000)
            documents = [doc for doc in results]
            if documents:
                return documents
            else:
                return None
        except Exception as e:
            print(f"Unexpected error retrieving documents: {e}")
            return None

    def create(self, document_data_list):
        try:
            self.solr.add(document_data_list)
            self.solr.commit()
        except Exception as e:
            print(f"Error adding document(s) to Solr: {e}")

    def read_one(self, document_id):
        try:
            results = self.solr.search(q=f'id:{document_id}', rows=1)
            documents = [doc for doc in results]
            if documents:
                return documents[0]
            else:
                return None
        except Exception as e:
            print(f"Error retrieving document from Solr: {e}")
            return None

    def update(self, document_ids, update_data_list):
        try:
            update_docs = [{'id': doc_id, **update_data} for doc_id, update_data in zip(document_ids, update_data_list)]
            self.solr.add(update_docs)
            self.solr.commit()
        except Exception as e:
            print(f"Error updating documents in Solr: {e}")

    def delete(self, document_id):
        try:
            self.solr.delete(id=f"{document_id}")
            self.solr.commit()
        except Exception as e:
            print(f"Error deleting document from Solr: {e}")

    def mlt(self, content_val):
        try:
            results = self.solr.more_like_this(q=f'content:{content_val}', mltfl='content')
            documents = [doc for doc in results.docs]
            return documents if documents else None
        except Exception as e:
            print(f"Error retrieving documents from Solr: {e}")
            return None
