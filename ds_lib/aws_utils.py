##############################################################################################################
# Name        : aws_utils
# Description : Makes dealing with AWS S3 and EC2 easier
# Version     : 0.0.0
# Created On  : 2020-01-02
# Modified On : 2020-01-02
# Author      : Hamid R. Darabi, Ph.D.
##############################################################################################################

import os
import boto3

class AWSUtil:
    def __init__(self, key, secret, **kwargs):
        self.key = key
        self.secret = secret
        self.sess = boto3.session.Session(key, secret)
        self.s3_client = self.sess.client('s3')
        self.ec2_client = self.sess.client('ec2')

    def get_tag(self, bucket, file_key_path, tag_name):
        tags = self.s3_client.get_object_tagging(Bucket=bucket, Key=file_key_path)['TagSet']
        for tag in tags:
            if tag['Key'] == tag_name:
                return tag['Value']
        return None

    def set_tag(self, bucket, file_key_path, tag_name, tag_value):
        tags = self.s3_client.get_object_tagging(Bucket=bucket, Key=file_key_path)['TagSet']
        new_tags = []
        for tag in tags:
            if tag['Key'] == tag_name:
                tag['Value'] = tag_value
            new_tags.append(tag)
        self.s3_client.put_object_tagging(Bucket=bucket, Key=file_key_path, Tagging={'TagSet': new_tags})
