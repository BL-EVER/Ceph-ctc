import os
from dotenv import load_dotenv
load_dotenv()
access_key=os.environ['CEPH_ACCESS_KEY']
secret_key=os.environ['CEPH_SECRET_KEY']
server=os.environ['CEPH_SERVER']

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

#acl = s3.get_bucket_acl(Bucket='public')
#response = s3.put_bucket_acl(Bucket='public', GrantFullControl='id=testuser@kemea.gr,id=nano')


#re = s3.get_bucket_acl(Bucket='public')
#print(re)

metadata = rgw.get_metadata(metadata_type='bucket', key='kemea')
bucket_id = metadata['data']['bucket']['bucket_id']

rgw.link_bucket(
    bucket='kemea',
    bucket_id=bucket_id,
    uid='testuser@kemea.gr',
)
