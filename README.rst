Sign AWS S3 HTTP Requests
=========================

S3 Signed Auth is a simple Python library to authenticate your HTTP requests to `AWS S3 <http://aws.amazon.com/s3/>`_ endpoints.

This `authentication mechanism <http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html>`_ can authorize your end users to perform operations (read/upload/delete/edit/list) directly on your S3 buckets.

The main advantage is to offload your servers from file transfer and as a result having a better scalable file handling strategy.


Installation
------------

To install S3 Signed Auth, simply:

.. code-block:: bash

  $ pip install s3-signed-auth


Getting Started
---------------

Example to authenticate a ``GET /filename.png`` request:

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')
  >>> signature = s3auth.sign_get_file('/filename.png')

The variable ``signature`` now holds the base64 encoded SHA1 checksum S3 will use to authenticate your request.

From there you can let your user request the file operation directly to S3, providing the signature either via HTTP header or query string.

If using the HTTP ``Authorization`` header, specify the ``http_header`` output type, to get a pre-formatted value:

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')
  >>> http_auth_value = s3auth.sign_get_file('filename.png', output='http_header')
  >>> print http_auth_value
  'AWS <AWS_KEY>:<signature>'
  >>> # Example using requests (http://docs.python-requests.org)
  >>> import requests
  >>> headers = {'Authorization': http_auth_value}
  >>> requests.get('https://bucket-name.s3.amazonaws.com/filename.png', headers=headers)

If using the query string version, specify the ``query_string`` output type, to get a pre-formatted value:

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> auth_query_string = s3auth.sign_get_file('filename.png', output='query_string',
  ...                                           bucket_name='pouet')
  >>> print auth_query_string
  '<uri-encoded-signature>'
  >>> # Example using requests (http://docs.python-requests.org)
  >>> import requests
  >>> payload = {'Signature': auth_query_string, 'AWSAccessKeyId': '<Your-AWS-KEY>',
  ...            'Expires': '<UNIX-epoch-timestamp>'}
  >>> requests.get('https://bucket-name.s3.amazonaws.com/filename.png', params=payload)


Timestamp requirement
~~~~~~~~~~~~~~~~~~~~~

A valid timestamp (using either the HTTP ``Date`` header or AWS ``x-amz-date`` custom header) is mandatory for authenticated requests. This timestamp must be within 15 minutes from the Amazon S3 system time when the request is received and can not be set in the future. Its purpose is to prevent an adversary to replay the requests past this 15 minutes period. It is also highly recommended to use HTTPS transport for your authenticated requests. See `Security <#security>`_ for more details.

When using query string, no special HTTP header are required. To provide the valid timestamp use instead the ``Expires`` query string, as in the example above. Its value must be specified as the number of seconds since the UNIX epoch.


API Reference
-------------


``class S3SignedURL()``
~~~~~~~~~~~~~~~~~~~~~~~

**Arguments:**

* ``AWS_KEY`` - mandatory.
* ``AWS_SECRET_KEY`` - mandatory.
* ``BUCKET_NAME`` - optional. If not provided when instantiating the class, the bucket name must be provided each time when calling its methods via the ``bucket_name`` keyword.

**Returns:**

An object providing methods to sign requests to S3 endpoints.

**Example:**

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')


``.sign_get_file()``
~~~~~~~~~~~~~~~~~~~~

**Arguments:**

* ``filename`` - mandatory. The complete path to the file on the S3 bucket, including the file extension if any, and excluding the bucket name. It must start with a ``/``.
* ``output`` - optional. To specify the output type preferred. When not provided output is the base64 encoded SHA1 checksum of the request. Other output types are:

  * ``http_header``: Returns the value to be used with the ``Authorization`` HTTP header.
  * ``query_string``: Returns the URI encoded value to be used as query string.
* ``date`` - optional. To specify the date to be used. The request must then be made maximum 15 minutes after. It must be a ``datetime`` instance. Default is the current datetime as given by `datetime.datetime.now()`.
* ``bucket_name`` - optional. To specify the bucket_name on which the we want to get the file. If not provided, the bucket name must have been provided when instantiating the S3SignedURL class.

**Returns:**

By default the method returns the raw base64 encoded SHA1 checksum. Output can be modified with the ``output`` keyword argument.

**Examples:**

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')
  >>> signature = s3auth.sign_get_file('/vacation 2006/Paris/0001.png')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> http_auth_value = s3auth.sign_get_file('/vacation 2006/Paris/0001.png',
  ...                                        bucket_name='pouet', output='http_header')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> import datetime
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> timestamp = datetime.datetime.now()
  >>> http_auth_value = s3auth.sign_get_file('/vacation 2006/Paris/0001.png',
  ...                                        bucket_name='pouet',
  ...                                        output='http_header', date=timestamp)


``.sign_put_file()``
~~~~~~~~~~~~~~~~~~~~

**Arguments:**

* ``filename`` - mandatory. The complete path to the file on the S3 bucket, including the file extension if any, and excluding the bucket name. It must start with a ``/``.
* ``mime_type`` - optional. The file MIME type.
* ``output`` - optional. To specify the output type preferred. When not provided output is the base64 encoded SHA1 checksum of the request. Other output types are:

  * ``http_header``: Returns the value to be used with the ``Authorization`` HTTP header.
  * ``query_string``: Returns the URI encoded value to be used as query string.
* ``date`` - optional. To specify the date to be used. The request must then be made maximum 15 minutes after. It must be a ``datetime`` instance. Default is the current datetime as given by `datetime.datetime.now()`.
* ``bucket_name`` - optional. To specify the bucket_name on which the we want to get the file. If not provided, the bucket name must have been provided when instantiating the S3SignedURL class.

**Returns:**

By default the method returns the raw base64 encoded SHA1 checksum. Output can be modified with the ``output`` keyword argument.

**Examples:**

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')
  >>> signature = s3auth.sign_put_file('/vacation 2006/Paris/0001.png',
  ...                                  mime_type='image/png')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> http_auth_value = s3auth.sign_put_file('/vacation 2006/Paris/0001.png',
  ...                                        bucket_name='pouet', output='http_header')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> import datetime
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> timestamp = datetime.datetime.now()
  >>> http_auth_value = s3auth.sign_put_file('/vacation 2006/Paris/0001.png',
  ...                                        bucket_name='pouet',
  ...                                        output='http_header', date=timestamp)

``.sign_delete_file()``
~~~~~~~~~~~~~~~~~~~~~~~

**Arguments:**

* ``filename`` - mandatory. The complete path to the file on the S3 bucket, including the file extension if any, and excluding the bucket name. It must start with a ``/``.
* ``output`` - optional. To specify the output type preferred. When not provided output is the base64 encoded SHA1 checksum of the request. Other output types are:

  * ``http_header``: Returns the value to be used with the ``Authorization`` HTTP header.
  * ``query_string``: Returns the URI encoded value to be used as query string.
* ``date`` - optional. To specify the date to be used. The request must then be made maximum 15 minutes after. It must be a ``datetime`` instance. Default is the current datetime as given by `datetime.datetime.now()`.
* ``bucket_name`` - optional. To specify the bucket_name on which the we want to get the file. If not provided, the bucket name must have been provided when instantiating the S3SignedURL class.

**Returns:**

By default the method returns the raw base64 encoded SHA1 checksum. Output can be modified with the ``output`` keyword argument.

**Examples:**

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')
  >>> signature = s3auth.sign_delete_file('/vacation 2006/Paris/0001.png')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> http_auth_value = s3auth.sign_delete_file('/vacation 2006/Paris/0001.png',
  ...                                           bucket_name='pouet', output='http_header')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> import datetime
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> timestamp = datetime.datetime.now()
  >>> http_auth_value = s3auth.sign_delete_file('/vacation 2006/Paris/0001.png',
  ...                                           bucket_name='pouet',
  ...                                           output='http_header', date=timestamp)

``.sign_list_dir()``
~~~~~~~~~~~~~~~~~~~~

**Arguments:**

* ``dirname`` - optional. The complete path to the directory on the S3 bucket, and excluding the bucket name. It must start with a ``/``. If not provided its default value is ``/``.
* ``output`` - optional. To specify the output type preferred. When not provided output is the base64 encoded SHA1 checksum of the request. Other output types are:

  * ``http_header``: Returns the value to be used with the ``Authorization`` HTTP header.
  * ``query_string``: Returns the URI encoded value to be used as query string.
* ``date`` - optional. To specify the date to be used. The request must then be made maximum 15 minutes after. It must be a ``datetime`` instance. Default is the current datetime as given by `datetime.datetime.now()`.
* ``bucket_name`` - optional. To specify the bucket_name on which the we want to get the file. If not provided, the bucket name must have been provided when instantiating the S3SignedURL class.

**Returns:**

By default the method returns the raw base64 encoded SHA1 checksum. Output can be modified with the ``output`` keyword argument.

**Examples:**

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy',
  ...                                   BUCKET_NAME='pouet')
  >>> signature = s3auth.sign_list_dir('/vacation 2006')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> http_auth_value = s3auth.sign_list_dir('/vacation 2006', bucket_name='pouet',
  ...                                        output='http_header')

.. code-block:: python

  >>> from s3signedauth import s3signedauth
  >>> import datetime
  >>> s3auth = s3signedauth.S3SignedURL(AWS_KEY='xxx', AWS_SECRET_KEY='yyy')
  >>> timestamp = datetime.datetime.now()
  >>> http_auth_value = s3auth.sign_list_dir('/vacation 2006', bucket_name='pouet',
  ...                                        output='http_header', date=timestamp)


Tests
-----

Testing is set up using `pytest <http://pytest.org/>`_ and coverage is handled with the `pytest-cov <https://pypi.python.org/pypi/pytest-cov>`_ plugin.
Unit tests are available in the ``/tests`` folder.

To test this library simply use:

.. code-block:: bash

  $ pip install -r dev-requirements.txt
  $ make test


Security
--------

Anybody knowing the request signature and URL can successfully perform the operation on the bucket.

In order to prevent this, it is crucial to both use a short interval after which the link will expire (see `Timestamp requirement <#timestamp-requirement>`_). As well as to use HTTPS when requesting the file operation.


See Also
--------

Official documentation about the authenticating mechanism from AWS S3:

* `Authenticating Requests (AWS Signature Version 4) <http://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html>`_

  * `Authenticating a Request in the Authorization Header <http://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-auth-using-authorization-header.html>`_
  * `Authenticating Requests by Using Query Parameters <http://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html>`_
  * `Examples: Signature Calculations <http://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-examples-using-sdks.html>`_
* `S3 FAQs <http://aws.amazon.com/s3/faqs>`_


TODO
----

* Support chunk upload (see `doc <http://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-streaming.html>`_)
* Support ACL (see `doc <http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGETacl.html>`_)
* Support file versioning (see `doc <http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html>`_)
* Support ``PUT Copy`` (see `doc <http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectCOPY.html>`_)
* Support ``HEAD`` request (see `doc <http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectHEAD.html>`_)


License
-------

The MIT License (MIT)

Copyright © 2015 Julien Buty <julien@nepsilon.net>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
