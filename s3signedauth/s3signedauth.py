import urllib
import sha
import hmac
import base64
from datetime import datetime


class S3SignedURL():

    def __init__(self, AWS_KEY=None, AWS_SECRET_KEY=None, BUCKET_NAME=None):
        if not AWS_KEY or not AWS_SECRET_KEY:
            raise Exception('You must provide your AWS key and secret key.')
        else:
            self.AWS_KEY = AWS_KEY
            self.AWS_SECRET_KEY = AWS_SECRET_KEY
        # Getting the bucket name if any
        if BUCKET_NAME:
            if BUCKET_NAME.startswith('/') or BUCKET_NAME.endswith('/'):
                raise Exception('BUCKET_NAME must neither start nor end with the \
                                 character "/".')
            else:
                self.has_bucket_name = True
                self.BUCKET_NAME = BUCKET_NAME
        else:
            self.has_bucket_name = False

    def _forge_signature(self, method, filepath, timestamp='', output=None,
                         mime_type=''):
        # TODO: Need to type check timestamp for datetime object
        if not timestamp:
            timestamp = datetime.now()
        timestamp_str = datetime.strftime(timestamp,
                                          '%a, %d %b %Y %H:%M:%S GMT')
        sanitized_filepath = urllib.quote(filepath)
        date_header_value = 'x-amz-date:' + timestamp_str
        s3_req_string = "{0}\n\n{1}\n\n{2}\n{3}".format(method, mime_type,
                                                        date_header_value,
                                                        sanitized_filepath)
        h = hmac.new(self.AWS_SECRET_KEY, s3_req_string, sha)
        signature = base64.encodestring(h.digest()).strip()
        if not output:
            return signature
        elif output == 'http_header':
            http_auth_header = "AWS {0}:{1}".format(self.AWS_KEY, signature)
            return http_auth_header
        elif output == 'query_string':
            return urllib.quote(signature)

    def _sign_operation(self, method, filename, options):
        if not filename:
            raise Exception('No filename provided')
        elif not filename.strip().startswith('/'):
            raise Exception('The filename must starts with the character "/".')
        # Get the bucket name
        bucket_name = options.get('bucket_name')
        if self.has_bucket_name and bucket_name:
            raise Exception('Bucket name already set when instantiating \
                             the class (%s).' % self.BUCKET_NAME)
        elif not self.has_bucket_name and not bucket_name:
            raise Exception('Bucket name neither set when instantiating \
                             the class or calling this method.')
        elif not bucket_name:
            bucket_name = self.BUCKET_NAME
        # Forge signature
        filepath = "/{0}{1}".format(bucket_name.strip(), filename.strip())
        forged_sig = self._forge_signature(method, filepath,
                                           timestamp=options.get('timestamp'),
                                           output=options.get('output'),
                                           mime_type=options.get('mime_type'))
        return forged_sig

    def sign_get_file(self, filename, **kwargs):
        return self._sign_operation('GET', filename, kwargs)

    def sign_put_file(self, filename, **kwargs):
        return self._sign_operation('PUT', filename, kwargs)

    def sign_delete_file(self, filename, **kwargs):
        return self._sign_operation('DELETE', filename, kwargs)

    def sign_list_dir(self, directory, **kwargs):
        return self._sign_operation('GET', directory, kwargs)
