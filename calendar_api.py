from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

cred = credentials.Certificate('serviceAccountKey.json')  # 請將此檔案換成您的 Firebase 服務帳戶金鑰檔名
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)


# 取得某月所有事件
@app.route('/api/events', methods=['GET'])
def get_events():
    month = request.args.get('month')  # 格式 YYYY-MM
    docs = db.collection('calender').where('date', '>=', f'{month}-01').where('date', '<=', f'{month}-31').stream()
    events = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        events.append(data)
    return jsonify(events)

# 新增事件
@app.route('/api/events', methods=['POST'])
def add_event():
    data = request.json
    event_id = str(uuid.uuid4())
    db.collection('calender').document(event_id).set({
        'date': data['date'],
        'title': data['title'],
        'color': data.get('color', '#ffda36'),
        'user': data.get('user', '')
    })
    return jsonify({'id': event_id}), 201


# 編輯事件
@app.route('/api/events/<event_id>', methods=['PUT'])
def edit_event(event_id):
    data = request.json
    db.collection('calender').document(event_id).update({
        'title': data['title'],
        'color': data.get('color', '#ffda36')
    })
    return jsonify({'status': 'ok'})


# 刪除事件
@app.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    db.collection('calender').document(event_id).delete()
    return jsonify({'status': 'ok'})


# 拖曳事件（改日期）
@app.route('/api/events/<event_id>', methods=['PATCH'])
def move_event(event_id):
    data = request.json
    db.collection('calender').document(event_id).update({
        'date': data['date']
    })
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
