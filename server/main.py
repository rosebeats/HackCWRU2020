import os
from flask import Flask
from flask import request
from google.cloud import storage
from uuid import UUID

app = Flask(__name__)

client = storage.Client()
bucket_name = 'botcontroller-267620.appspot.com'
bucket = client.bucket(bucket_name)

@app.route('/commands/<commandUuid>', methods=['GET', 'POST', 'DELETE'])
def commands(commandUuid):
    try:
        commandUuid = UUID(commandUuid, version=4)
        commandUuid = str(commandUuid)
    except:
        return 'invalid uuid!', 400

    if request.method == 'POST':
        return send(commandUuid)
    blob = bucket.blob(commandUuid)
    if not blob.exists():
        return 'not found!', 404
    if request.method == 'GET':
        return blob.download_as_string();
    else:
        blob.delete()
        return 'success'

def send(commandUuid):
    try:
        text = request.data.decode('ascii')
        if len(text) == 0:
            return 'empty message!', 400
        if text.find('\n') != -1 or text.find('\r') != -1:
            return 'cannot have line breaks!', 400
    except:
        return 'invalid text!', 400

    blob = bucket.blob(commandUuid)
    tmp_filename = os.path.join('/tmp', commandUuid)
    if blob.exists():
        blob.download_to_filename(tmp_filename)
    else:
        with open(tmp_filename, 'w') as f:
            pass
    with open(tmp_filename, 'r+') as f:
        lines = f.readlines()
        lines = lines[-10:]
        num = 0
        try:
            num = int(lines[-1].split(',')[0])
        except:
            pass
        lines.append(str(num + 1) + ',' + text + '\n')
        f.seek(0)
        f.truncate(0)
        f.writelines(lines)
    blob.upload_from_filename(tmp_filename);
    return 'success'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)