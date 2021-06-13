
# Message
# shows a single message item and lets you delete a message item
from datetime import datetime

from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort

from app import db


class Message(Resource):
    @jwt_required()
    def get(self, id):
        msg_id = ObjectId(id)
        current_user = get_jwt_identity()
        message = db.messages.find_one({"receiver":current_user, "_id": msg_id})
        message["_id"] = str(msg_id)
        if message["isRead"] == False:
            db.messages.update_one({"_id": msg_id}, {"$set": {"isRead": True}})

        return jsonify(message=message, status=400)

    def delete(self, id):
        try:
            id = ObjectId(id)
            current_user = get_jwt_identity()
            db.messages.delete_one({"receiver":current_user,"_id": id})
        except:
            abort(404, message="Message {} doesn't exist".format(id))

        return jsonify(message='Message deleted', status=204)



# MessagesList
# shows a list of all messages, and lets you POST to add new messages
def findReceiver(receiver):
    test = db.users.find_one({"email": receiver})
    if test:
        return jsonify(message="Receiver Exist", status=409)
    abort(404, message="Receiver {} doesn't exist".format(receiver))

class MessagesList(Resource):
    @jwt_required()
    def get(self):
        start = int(1)
        limit = int(50)
        current_user = get_jwt_identity()
        if len(request.args) > 0:
            start = int(request.args['start'])
            limit = int(request.args['limit'])
        messages = db.messages.find({"receiver":current_user}).skip(start).limit(limit)

        res = []
        for msg in messages:
            msg["_id"] = str(msg["_id"])
            res.append(msg)

        return jsonify(start=start,limit=limit,result=res)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        today = datetime.today()
        sender = current_user
        receiver = request.json["receiver"]
        findReceiver(receiver)
        message = request.json["message"]
        subject = request.json["subject"]
        creationDate = today.strftime('%Y-%m-%d')
        isRead = False
        new_message = dict(
            sender=sender,
            receiver=receiver,
            message=message,
            subject=subject,
            creationDate=creationDate,
            isRead = isRead
        )
        id = db.messages.insert_one(new_message)
        new_message["_id"] = str(id.inserted_id)
        return new_message


# UnreadMessages
# shows a list of all the unreaden messages

class UnreadMesseages(Resource):
    @jwt_required()
    def get(self):
        start = int(1)
        limit = int(50)
        current_user = get_jwt_identity()
        if len(request.args) > 0:
            start = int(request.args['start'])
            limit = int(request.args['limit'])
        unread_messages = db.messages.find({"receiver":current_user,"isRead": False}).skip(start).limit(limit)
        res = []
        for msg in unread_messages:
            msg["_id"] = str(msg["_id"])
            res.append(msg)

        return jsonify(start=start,limit=limit,result=res)

