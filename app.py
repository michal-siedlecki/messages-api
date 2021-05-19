import views
from config import app, API_URL


# A route to return app info.
@app.route('/', methods=['GET'])
def info():
    return views.info_view()


# A route to return all of the available entries in the system.
@app.route('/' + API_URL + '/messages', methods=['GET'])
def list_view() -> object:
    return views.messages_list_view()

# A route to get message details.
@app.route('/' + API_URL + '/messages/<pk>', methods=['GET'])
def detail(pk) -> object:
    return views.message_detail_view(pk)


# A route to create a new message.
@app.route('/' + API_URL + '/messages', methods=['POST'])
def create() -> object:
    return views.message_create_view()


# A route to create a new message.
@app.route('/' + API_URL + '/messages/<pk>', methods=['PATCH'])
def update(pk) -> object:
    return views.message_update_view(pk)


# A route to delete message.
@app.route('/' + API_URL + '/messages/<pk>', methods=['DELETE'])
def delete(pk) -> object:
    return views.message_delete_view(pk)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
