from flask import Flask, jsonify, request
app= Flask(__name__)
from flask_cors import CORS
cors = CORS(app)

import os
from dotenv import load_dotenv
load_dotenv()
access_key=os.environ['CEPH_ACCESS_KEY']
secret_key=os.environ['CEPH_SECRET_KEY']
server=os.environ['CEPH_SERVER']


#https://rgwadmin.readthedocs.io/en/latest/rgwadmin/user-guide.html


PREFIX = ""

from rgwadmin import RGWAdmin
rgw = RGWAdmin(
    access_key=access_key,
    secret_key=secret_key,
    server=server,
    secure=False,
    verify=False)

import boto3
s3 = boto3.client('s3',
    endpoint_url="http://"+server,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

#For sree to locate ceph api
@app.route(PREFIX + "/endpoint", methods=["GET"])##
def getEndpoint():
    return jsonify(os.environ['CEPH_SERVER'])

@app.route(PREFIX + "/user", methods=["POST"])##
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
    
@app.route(PREFIX + "/user/<uid>", methods=["GET"])##
def getUser(uid):
    return jsonify(rgw.get_user(uid, stats=True))

@app.route(PREFIX + "/user", methods=["GET"])
def getUsers():
    return jsonify(rgw.get_users())

@app.route(PREFIX + "/user/<uid>", methods=["DELETE"])
def deleteUser(uid):
    if request.method=='DELETE':
        rgw.remove_user(uid, purge_data=True)
        resp = jsonify(success=True)
        return resp
    
@app.route(PREFIX + "/user/<uid>/key", methods=["GET"])
def generateKeyForUser(uid):
    rgw.create_key(
            uid,
            key_type='s3',
            generate_key=True)
    return jsonify(rgw.get_user(uid, stats=True))

@app.route(PREFIX + "/bucket/<bid>", methods=["GET"])##
def getBucket(bid):
    return jsonify(rgw.get_bucket(bucket=bid))

@app.route(PREFIX + "/buckets", methods=["GET"])##
def getUserBuckets():
    return jsonify(rgw.get_buckets())
	
def linkBucketToUser(bid, uid):
    metadata = rgw.get_metadata(metadata_type='bucket', key=bid)
    bucket_id = metadata['data']['bucket']['bucket_id']
    resp = rgw.link_bucket(
        bucket=bid,
        bucket_id=bucket_id,
        uid=uid,
    )
    
def userAccessBucket(bid,uid):
    acl = s3.get_bucket_acl(Bucket=bid)
    allGrants = acl["Grants"]+[{'Grantee': {'ID': uid, 'Type': 'CanonicalUser'}, 'Permission': 'FULL_CONTROL'}]
    response = s3.put_bucket_acl(AccessControlPolicy={'Grants': allGrants,'Owner': acl["Owner"]},Bucket=bid)

    
@app.route(PREFIX + "/bucket/<bid>", methods=["DELETE"])
def deleteBucket(bid):
    if request.method=='DELETE':
        linkBucketToUser(bid, 'nano')
        objects = s3.list_objects_v2(Bucket=bid)
        
        for obj in objects.get('Contents', []):
            s3.delete_object(Bucket=bid, Key=obj['Key'])
        response = s3.delete_bucket(Bucket=bid)
        
        resp = jsonify(success=True)
        return resp

def createBucket(bid):
    response = s3.create_bucket(Bucket=bid)
    cors_configuration = {
    'CORSRules': [{
        'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE'],
        'AllowedOrigins': ['*'],
        'AllowedHeaders': ['*', 'Authorization'],
        'ExposeHeaders': ['ETag', 'x-amz-acl']
    }]}
    s3.put_bucket_cors(Bucket=bid, CORSConfiguration=cors_configuration)
    linkBucketToUser(bid, 'nano')

@app.route(PREFIX + "/assignBuckets", methods=["POST"])
def assignBuckets():
    if request.method=='POST':
        
        posted_data = request.get_json()
        uid=posted_data['uid']
        org=posted_data['org']
        org=org.lower()
        
        #General bucket creation
        all_buckets = rgw.get_buckets();
        if "public" not in all_buckets:
            createBucket("public")
        if org not in all_buckets:
            createBucket(org)

        #User buckets
        user_buckets = rgw.get_bucket(uid=uid);
        if "public" not in user_buckets:
            linkBucketToUser("public", uid)
        if org not in user_buckets:
            linkBucketToUser(org, uid)

        return jsonify(success=True)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=81)
