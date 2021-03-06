from __future__ import unicode_literals
import base64
from datetime import datetime
from hashlib import sha1
import hmac
import json
import os
import re
import six
import time
import urllib
from uuid import uuid4

import boto
from flask import current_app as app
from flask import Markup
from werkzeug import secure_filename

from .extensions import db

def s3_signer(request):
        AWS_ACCESS_KEY = app.config['AWS_ACCESS_KEY_ID']
        AWS_SECRET_KEY =  app.config['AWS_SECRET_ACCESS_KEY']
        S3_BUCKET =  app.config['S3_BUCKET_NAME']

        object_name = request.args.get('s3_object_name')
        mime_type = request.args.get('s3_object_type')

        expires = int(time.time()+20)
        amz_headers = 'x-amz-acl:public-read'

        put_request = 'PUT\n\n%s\n%d\n%s\n/%s/%s' % (
                mime_type, expires, amz_headers, S3_BUCKET, object_name)

        signature = base64.encodestring(
                hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        signature = urllib.quote_plus(signature.strip())

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

        return json.dumps({
            'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' \
                % (url, AWS_ACCESS_KEY, expires, signature),
            'url': url
            })


def s3_upload(source_file,acl='public-read'):
    ''' From: https://github.com/doobeh/Flask-S3-Uploader/blob/master/tools.py

        Uploads WTForm File Object to Amazon S3

        Expects following app.config attributes to be set:
            AWS_ACCESS_KEY_ID       :   S3 API Key
            AWS_SECRET_ACCESS_KEY   :   S3 Secret Key
            S3_BUCKET_NAME          :   What bucket to upload to
            S3_UPLOAD_DIRECTORY     :   Which S3 Directory.

        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.
    '''
    source_filename = secure_filename(source_file.data.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex + source_extension
    # Connect to S3 and upload file.
    conn = boto.connect_s3(
            app.config['AWS_ACCESS_KEY_ID'],
            app.config['AWS_SECRET_ACCESS_KEY'])
    b = conn.get_bucket(app.config['S3_BUCKET_NAME'])

    sml = b.new_key(
            '/'.join([app.config['S3_UPLOAD_DIRECTORY'],
                        destination_filename]))
    sml.set_contents_from_string(source_file.data.read())
    sml.set_acl(acl)

    return sml.generate_url(expires_in=300, query_auth=False)


def prettydate(d):
    diff = datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 14 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s/3600)

def slugify(value, substitutions=()):
    '''
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Took from Django sources.
    '''
    # TODO Maybe steal again from current Django 1.5dev
    value = Markup(value).striptags()
    # value must be unicode per se
    import unicodedata
    from unidecode import unidecode
    # unidecode returns str in Py2 and 3, so in Py2 we have to make
    # it unicode again
    value = unidecode(value)
    if isinstance(value, six.binary_type):
        value = value.decode('ascii')
    # still unicode
    value = unicodedata.normalize('NFKD', value).lower()
    for src, dst in substitutions:
        value = value.replace(src.lower(), dst.lower())
    value = re.sub('[^\w\s-]', '', value).strip()
    value = re.sub('[-\s]+', '-', value)
    # we want only ASCII chars
    value = value.encode('ascii', 'ignore')
    # but Pelican should generally use only unicode
    return value.decode('ascii')


def mongo_to_dict(obj):
    return_data = []

    if isinstance(obj, db.DynamicDocument):
        return_data.append(('id',str(obj.id)))
    if isinstance(obj, db.Document):
        return_data.append(('id',str(obj.id)))

    for field_name in obj._fields:

        if field_name in ('id',):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], db.DateTimeField):
            if data:
                return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.StringField):
            try:
                data = str(data)
            except:
                data = data
                pass
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], db.IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], db.ListField):
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name],
                db.EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))
        elif isinstance(obj._fields[field_name], db.DictField):
            return_data.append((field_name, data))

    return dict(return_data)
