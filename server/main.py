import os
from flask import Flask
from flask import request
from google.cloud import storage
from uuid import UUID

app = Flask(__name__)

client = storage.Client()
bucket_name = 'botcontroller-267620.appspot.com'
bucket = client.bucket(bucket_name)

#@app.route('/delete', methods=['DELETE'])
#def delete():
#    blob = bucket.blob
#    commandUuid = ''
#    try:
#        commandUuid = UUID(request.form['uuid'], version=4)
#    except:
#        return 'invalid uuid!', 400
#    commandUuid = str(commandUuid)

@app.route('/')
def test():
    return '''<form method="post" action="/send">
    UUID:<br>
    <input type="text" name="uuid"><br>
    text:<br>
    <input type="text" name="text"><br>
    <input type="submit" value="Submit">
</form>'''

@app.route('/send', methods=['POST'])
def send():
    commandUuid = ''
    try:
        commandUuid = UUID(request.form['uuid'], version=4)
    except:
        return 'invalid uuid!', 400
    try:
        text = request.form['text']
        if text.find('\n') != -1 or text.find('\r') != -1:
            return 'cannot have line breaks!', 400
    except:
        return 'invalid text!', 400
    commandUuid = str(commandUuid)
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
        lines.append(text + '\n')
        f.seek(0)
        f.truncate(0)
        f.writelines(lines)
    blob.upload_from_filename(tmp_filename);
    return 'success'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)