from flask import Flask, jsonify, request
app= Flask(__name__)
from flask_cors import CORS
cors = CORS(app)

import os
from dotenv import load_dotenv
load_dotenv()


#https://rgwadmin.readthedocs.io/en/latest/rgwadmin/user-guide.html

from rgwadmin import RGWAdmin
rgw = RGWAdmin(
    access_key=os.environ['CEPH_ACCESS_KEY'],
    secret_key=os.environ['CEPH_SECRET_KEY'],
    server=os.environ['CEPH_SERVER'],
    secure=False,
    verify=False)
	
@app.route("/endpoint", methods=["GET"])
def getEndpoint():
    return jsonify(os.environ['CEPH_SERVER'])

@app.route("/user", methods=["POST"])
def setUser():
    if request.method=='POST':
        posted_data = request.get_json()
        print(posted_data)
        resp = rgw.create_user(
            uid=posted_data['uid'],
            display_name=posted_data['display_name'],
            email=posted_data['email'],
            user_caps=posted_data['user_caps'],
            max_buckets=posted_data['max_buckets'])
        return jsonify(resp)
    
@app.route("/user/<uid>", methods=["GET"])
def getUser(uid):
    return jsonify(rgw.get_user(uid, stats=True))

@app.route("/user", methods=["GET"])
def getUsers():
    return jsonify(rgw.get_users())

@app.route("/user/<uid>", methods=["DELETE"])
def deleteUser(uid):
    if request.method=='DELETE':
        rgw.remove_user(uid, purge_data=True)
        resp = jsonify(success=True)
        return resp
    
@app.route("/user/<uid>/key", methods=["GET"])
def generateKeyForUser(uid):
    rgw.create_key(
            uid,
            key_type='s3',
            generate_key=True)
    return jsonify(rgw.get_user(uid, stats=True))

#TODO: Debug
@app.route("/buckets", methods=["GET"])
def getUserBuckets():
    return jsonify(rgw.get_buckets())

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)
