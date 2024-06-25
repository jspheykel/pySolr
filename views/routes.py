from flask import Flask, request, jsonify
from controllers.document_controller import DocumentController

solr_url = 'http://34.34.222.41:8983/solr'
solr_collection = 'myNewCollection'

app = Flask(__name__)

document_controller = DocumentController(solr_url, solr_collection)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(document_controller.test_connection())

@app.route('/solr/add', methods=['POST'])
def create_document():
    document_data_list = request.json
    if document_data_list and isinstance(document_data_list, list):
        document_controller.create_document(document_data_list)
        return jsonify({"message": "Documents created successfully!"}), 200
    else:
        return jsonify({"error": "No valid document data provided or data is not a list."}), 400

@app.route('/solr/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    document = document_controller.get_document(document_id)
    if document:
        return jsonify(document)
    else:
        return jsonify({"message": f"Document with ID '{document_id}' not found."}), 404

@app.route("/solr/documents", methods=["GET"])
def get_all_documents():
    try:
        documents = document_controller.get_all_documents()
        if documents:
            return jsonify(documents)
        else:
            return jsonify({"error": "No documents found"}), 404
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/solr/updates', methods=['POST'])
def update_documents():
    update_data_list = request.json
    if isinstance(update_data_list, list):
        document_ids = [update_data.get('id') for update_data in update_data_list]
        if all(document_ids):
            document_controller.update_documents(document_ids, update_data_list)
            return jsonify({"message": "Documents updated successfully!"}), 200
        else:
            return jsonify({"error": "Document ID not provided for one or more documents. Cannot update."}), 400
    else:
        return jsonify({"error": "Invalid data format. Expected a list of documents in JSON format."}), 400

@app.route('/solr/deletes/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        document_controller.delete_document(document_id)
        return jsonify({"message": f"Document with ID '{document_id}' deleted successfully!"}), 200
    except Exception as e:
        print(f"Error deleting document: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/solr/content/<content_val>', methods=['GET'])
def get_content(content_val):
    document = document_controller.get_similar_documents(content_val)
    if document:
        return jsonify(document)
    else:
        return jsonify({"message": f"No similar content found for value '{content_val}'."}), 404

if __name__ == '__main__':
    app.run(debug=True)
