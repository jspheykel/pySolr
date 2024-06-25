from models.document import Document

class DocumentController:
    def __init__(self, solr_url, collection_name):
        self.document_model = Document(solr_url, collection_name)

    def test_connection(self):
        return self.document_model.test_connection()

    def create_document(self, document_data_list):
        self.document_model.create(document_data_list)

    def get_document(self, document_id):
        return self.document_model.read_one(document_id)

    def get_all_documents(self):
        return self.document_model.read()

    def update_documents(self, document_ids, update_data_list):
        self.document_model.update(document_ids, update_data_list)

    def delete_document(self, document_id):
        self.document_model.delete(document_id)

    def get_similar_documents(self, content_val):
        return self.document_model.mlt(content_val)
