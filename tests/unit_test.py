# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
import urllib


class TestClass:

    @pytest.fixture
    def s3authclient_no_bucket(self):
        """ S3 client object instanciated without a bucket name.
        """
        from s3signedauth import s3signedauth
        s3auth = s3signedauth.S3SignedURL(AWS_KEY='ok', AWS_SECRET_KEY='pouet')
        return s3auth

    @pytest.fixture
    def s3authclient_with_bucket(self):
        """ S3 client object instanciated with a bucket name.
        """
        from s3signedauth import s3signedauth
        s3auth = s3signedauth.S3SignedURL(AWS_KEY='ok', AWS_SECRET_KEY='pouet',
                                          BUCKET_NAME='panier')
        return s3auth

    @pytest.fixture
    def timestamp(self):
        """ A fixed timestamp as a datetime instance.
        """
        timestamp = datetime.strptime('Mon, 1 Oct 2014 00:42:00 GMT',
                                      '%a, %d %b %Y %H:%M:%S GMT')
        return timestamp

    def test_instanciate_client_without_bucket(self):
        """ Testting ``S3SignedURL`` instantiation.

            1. Class must exist and be callable.
            2. Must raise Exception when instanciated without any argument.
            3. Must raise Exception when instanciated with only the AWS_KEY.
            4. Must raise Exception when instanciated with only
               the AWS_SECRET_KEY.
            5. Must have self.has_bucket_name set to True when
               BUCKET_NAME is set.
            6. Must have self.has_bucket_name set to False when BUCKET_NAME
               is not set.
        """
        from s3signedauth import s3signedauth
        # 1. Method must exist and be callable.
        assert callable(s3signedauth.S3SignedURL) is True
        # 2. Must raise Exception when instanciated without any argument
        with pytest.raises(Exception) as excinfo:
            s3signedauth.S3SignedURL()
        # 3. Must raise Exception when instanciated with only the AWS_KEY
        with pytest.raises(Exception) as excinfo:
            s3signedauth.S3SignedURL(AWS_KEY='ok')
        # 4. Must raise Exception when instanciated with only the
        #    AWS_SECRET_KEY
        with pytest.raises(Exception) as excinfo:
            s3signedauth.S3SignedURL(AWS_SECRET_KEY='ok')
        # 5. Must have self.has_bucket_name set to True when BUCKET_NAME is set
        s3auth = s3signedauth.S3SignedURL(AWS_KEY='ok', AWS_SECRET_KEY='pouet',
                                          BUCKET_NAME='panier')
        assert s3auth.has_bucket_name is True
        # 6. Must have self.has_bucket_name set to False when BUCKET_NAME
        #    is not set
        s3auth = s3signedauth.S3SignedURL(AWS_KEY='ok', AWS_SECRET_KEY='pouet')
        assert s3auth.has_bucket_name is False

    def test_sign_get_file(self, s3authclient_no_bucket, timestamp):
        """ Testing ``sign_get_file`` when no bucket set on the object.

             1. Method must exist and be callable.
             2. Must return a predictable signature when providing timestamp.
             3. Must work with unicode characters in filename
             4. Must work with space characters in filename
             5. Must work with unicode and space characters in filename
             6. Must return valid Authorization HTTP header when output
                is set to ``http_header``.
             7. Must return valid query string when output is set to
                ``query_string``.
             8. Must raise Exception when bucke_name must be provided.
             9. Must raise Exception when filename does NOT start with a "/".
            10. Must return a 10 characters length base64 string.
            11. Must return a predictable signature when providing timestamp
                and ``mime_type``.
        """
        # 1. Method must exist and be callable.
        assert callable(s3authclient_no_bucket.sign_get_file) is True
        # 2. Must return a predictable signature when providing timestamp.
        raw_sign = s3authclient_no_bucket.sign_get_file('/photo.png',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'v11wbdzl77Qg5Kzh1R57PHCrpgw='
        # 3. Must work with unicode filename
        raw_sign = s3authclient_no_bucket.sign_get_file('/photo✔ 汉字😓.png',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'CE3eJk3Szd+8bU5jgw28HK/dQKI='
        # 4. Must work with space characters in filename
        raw_sign = s3authclient_no_bucket.sign_get_file('  / p h o t o .p n g',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'V3IMsnAHv8WABjWKqEhzeaQ5v4k='
        # 5. Must work with unicode and space characters in filename
        raw_sign = s3authclient_no_bucket.sign_get_file(' /空格后表情：😍.png',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'gM3+CFm3kBt9tJB6rs1/Wj5ixDA='
        # 6. Must return valid Authorization HTTP header when output
        #    is set to ``http_header``.
        http_sign = s3authclient_no_bucket.sign_get_file('/表情：😍. p n g',
                                                         bucket_name='panier',
                                                         output='http_header',
                                                         timestamp=timestamp)
        assert http_sign == 'AWS ok:qNicSQL4EGlubevSqW235pvKYhA='
        # assert http_sign == 'AWS ok:qNicS...SqW235pvKYhA='
        # 7. Must return valid query string when output is set to
        #    ``query_string``.
        qs_sign = s3authclient_no_bucket.sign_get_file(' / 格：😍. p n g',
                                                       bucket_name='panier',
                                                       output='query_string',
                                                       timestamp=timestamp)
        assert qs_sign == 'CPe/ftegBEtPtEA0IYyft1YaVh0%3D'
        # 8. Must raise Exception when bucke_name must be provided
        with pytest.raises(Exception) as excinfo:
            s3authclient_no_bucket.sign_get_file('/filename.png',
                                                 timestamp=timestamp)
        # 9. Must raise Exception when filename does NOT start with a "/".
        with pytest.raises(Exception) as excinfo:
            s3authclient_no_bucket.sign_get_file('filename.png',
                                                 bucket_name='panier',
                                                 timestamp=timestamp)
        # 10. Must return a 10 characters length base64 string
        raw_sign = s3authclient_no_bucket.sign_get_file('/filename.png',
                                                        bucket_name='panier')
        # 10.1 String type
        assert isinstance(raw_sign, str)
        # 10.2 28 char length
        assert len(raw_sign) == 28
        # 10.3 Base64 encoded string
        try:
            raw_sign.decode('base64')
        except Exception, ex:
            pytest.fail(ex.message)
        # 11. Must return a predictable signature when providing timestamp and
        #     ``mime_type``.
        raw_sign = s3authclient_no_bucket.sign_get_file('/photo.png',
                                                        bucket_name='panier',
                                                        mime_type='image/png',
                                                        timestamp=timestamp)
        assert raw_sign == 'IjHixrqsyxKE9NuO6Xeo/RwOslo='

    def test_sign_put_file(self, s3authclient_no_bucket, timestamp):
        """ Testing ``sign_put_file`` when no bucket set on the object.

             1. Method must exist and be callable.
             2. Must return a predictable signature when providing timestamp.
             3. Must work with unicode characters in filename
             4. Must work with space characters in filename
             5. Must work with unicode and space characters in filename
             6. Must return valid Authorization HTTP header when output
                is set to ``http_header``.
             7. Must return valid query string when output is set to
                ``query_string``.
             8. Must raise Exception when bucke_name must be provided
             9. Must raise Exception when filename does NOT start with a "/".
            10. Must return a 10 characters length base64 string
            11. Must return a predictable signature when providing timestamp
                and ``mime_type``.
        """
        # 1. Method must exist and be callable.
        assert callable(s3authclient_no_bucket.sign_put_file) is True
        # 2. Must return a predictable signature when providing timestamp.
        raw_sign = s3authclient_no_bucket.sign_put_file('/photo.png',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'wyK6PAKNZGGaqyUqW8ORgob5x28='
        # 3. Must work with unicode filename
        raw_sign = s3authclient_no_bucket.sign_put_file('/photo✔ 汉字😓.png',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == '2e+h8PzeAwCa03mawHAkKTlQJ1c='
        # 4. Must work with space characters in filename
        raw_sign = s3authclient_no_bucket.sign_put_file('  / p h o t o .p n g',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'Mp+NojvxLnp4FSVgUamVZcKeDQA='
        # 5. Must work with unicode and space characters in filename
        raw_sign = s3authclient_no_bucket.sign_put_file(' /空格后表情：😍.png',
                                                        bucket_name='panier',
                                                        timestamp=timestamp)
        assert raw_sign == 'W7r4U7zGgqHC1AtlDODVjQHOQVE='
        # 6. Must return valid Authorization HTTP header when output
        #    is set to ``http_header``.
        http_sign = s3authclient_no_bucket.sign_put_file('/表情：😍. p n g',
                                                         bucket_name='panier',
                                                         output='http_header',
                                                         timestamp=timestamp)
        assert http_sign == 'AWS ok:nMcL0MCgX9TE1A7BOhMZxxOAAQ0='
        # assert http_sign == 'AWS ok:qNicS...SqW235pvKYhA='
        # 7. Must return valid query string when output is set to
        #    ``query_string``.
        qs_sign = s3authclient_no_bucket.sign_put_file(' / 格：😍. p n g',
                                                       bucket_name='panier',
                                                       output='query_string',
                                                       timestamp=timestamp)
        assert qs_sign == 'ExjrHbGPfXhvO/8OeN9zJ46PPU8%3D'
        # 8. Must raise Exception when bucke_name must be provided
        with pytest.raises(Exception) as excinfo:
            s3authclient_no_bucket.sign_put_file('/filename.png',
                                                 timestamp=timestamp)
        # 9. Must raise Exception when filename does NOT start with a "/".
        with pytest.raises(Exception) as excinfo:
            s3authclient_no_bucket.sign_put_file('filename.png',
                                                 bucket_name='panier',
                                                 timestamp=timestamp)
        # 10. Must return a 10 characters length base64 string
        raw_sign = s3authclient_no_bucket.sign_put_file('/filename.png',
                                                        bucket_name='panier')
        # 10.1 String type
        assert isinstance(raw_sign, str)
        # 10.2 28 char length
        assert len(raw_sign) == 28
        # 10.3 Base64 encoded string
        try:
            raw_sign.decode('base64')
        except Exception, ex:
            pytest.fail(ex.message)
        # 11. Must return a predictable signature when providing timestamp and
        #     ``mime_type``.
        raw_sign = s3authclient_no_bucket.sign_put_file('/photo.png',
                                                        bucket_name='panier',
                                                        mime_type='image/png',
                                                        timestamp=timestamp)
        assert raw_sign == '0yjbdwyGjoPDeBTAXzbYhycWhYo='

    def test_sign_delete_file(self, s3authclient_with_bucket, timestamp):
        """ Testing ``sign_delete_file`` when a bucket is already set
            on the object.

             1. Method must exist and be callable.
             2. Must return a predictable signature when providing timestamp.
             3. Must work with unicode characters in filename
             4. Must work with space characters in filename
             5. Must work with unicode and space characters in filename
             6. Must return valid Authorization HTTP header when output
                is set to ``http_header``.
             7. Must return valid query string when output is set to
                ``query_string``.
             8. Must raise Exception when bucke_name must be provided
             9. Must raise Exception when filename does NOT start with a "/".
            10. Must return a 10 characters length base64 string
            11. Must return a predictable signature when providing timestamp
                and ``mime_type``.
        """
        # 1. Method must exist and be callable.
        assert callable(s3authclient_with_bucket.sign_delete_file) is True
        # 2. Must return a predictable signature when providing timestamp.
        raw_s = s3authclient_with_bucket.sign_delete_file('/photo.png',
                                                          timestamp=timestamp)
        assert raw_s == '3dQnzROmetvO8J9jjS77p78ZrOY='
        # 3. Must work with unicode filename
        raw_s = s3authclient_with_bucket.sign_delete_file('/photo✔ 汉字😓.png',
                                                          timestamp=timestamp)
        assert raw_s == 'lrM49l12lhLwx515fQLon9lhnuo='
        # 4. Must work with space characters in filename
        raw_s = s3authclient_with_bucket.sign_delete_file('/p h o t o .p n g',
                                                          timestamp=timestamp)
        assert raw_s == 'nxMKCOSNDryMtTboO+pMVuor8vo='
        # 5. Must work with unicode and space characters in filename
        raw_s = s3authclient_with_bucket.sign_delete_file(' /空格后表情：😍.png',
                                                          timestamp=timestamp)
        assert raw_s == 'qNwSf8qtHc4y+s3WLbqbpz9zqiw='
        # 6. Must return valid Authorization HTTP header when output
        #    is set to ``http_header``.
        s = s3authclient_with_bucket.sign_delete_file('/表情：😍. p n g',
                                                      output='http_header',
                                                      timestamp=timestamp)
        assert s == 'AWS ok:ixgppTBHo5ZXhoumSSkVP2tzt80='
        # assert http_sign == 'AWS ok:qNicS...SqW235pvKYhA='
        # 7. Must return valid query string when output is set to
        #    ``query_string``.
        qs_s = s3authclient_with_bucket.sign_delete_file(' / 格：😍. p n g',
                                                         output='query_string',
                                                         timestamp=timestamp)
        assert qs_s == '%2Bgazphg/7eEbs09R30rSVnE1fCQ%3D'
        # 8. Must raise Exception when bucke_name must is provided
        with pytest.raises(Exception) as excinfo:
            s3authclient_with_bucket.sign_delete_file('/filename.png',
                                                      bucket_name='panier',
                                                      timestamp=timestamp)
        # 9. Must raise Exception when filename does NOT start with a "/".
        with pytest.raises(Exception) as excinfo:
            s3authclient_with_bucket.sign_delete_file('filename.png',
                                                      bucket_name='panier',
                                                      timestamp=timestamp)
        # 10. Must return a 10 characters length base64 string
        raw_s = s3authclient_with_bucket.sign_delete_file('/filename.png')
        # 10.1 String type
        assert isinstance(raw_s, str)
        # 10.2 28 char length
        assert len(raw_s) == 28
        # 10.3 Base64 encoded string
        try:
            raw_s.decode('base64')
        except Exception, ex:
            pytest.fail(ex.message)
        # 11. Must return a predictable signature when providing timestamp and
        #     ``mime_type``.
        s = s3authclient_with_bucket.sign_delete_file('/photo.txt',
                                                      mime_type='text/plain',
                                                      timestamp=timestamp)
        assert s == 'IrG7NQE9IivbGBH0OM7f9ETYUqU='

    def test_sign_list_dir(self, s3authclient_with_bucket, timestamp):
        """ Testing ``sign_list_dir`` when a bucket is already set
            on the object.

             1. Method must exist and be callable.
             2. Must return a predictable signature when providing timestamp.
             3. Must work with unicode characters in filename
             4. Must work with space characters in filename
             5. Must work with unicode and space characters in filename
             6. Must return valid Authorization HTTP header when output
                is set to ``http_header``.
             7. Must return valid query string when output is set to
                ``query_string``.
             8. Must raise Exception when bucke_name must be provided
             9. Must raise Exception when filename does NOT start with a "/".
            10. Must return a 10 characters length base64 string
            11. Must return a predictable signature when providing timestamp
                and ``mime_type``.
        """
        # 1. Method must exist and be callable.
        assert callable(s3authclient_with_bucket.sign_list_dir) is True
        # 2. Must return a predictable signature when providing timestamp.
        raw_s = s3authclient_with_bucket.sign_list_dir('/photo.png',
                                                       timestamp=timestamp)
        assert raw_s == 'v11wbdzl77Qg5Kzh1R57PHCrpgw='
        # 3. Must work with unicode filename
        raw_s = s3authclient_with_bucket.sign_list_dir('/photo✔ 汉字😓.png',
                                                       timestamp=timestamp)
        assert raw_s == 'CE3eJk3Szd+8bU5jgw28HK/dQKI='
        # 4. Must work with space characters in filename
        raw_s = s3authclient_with_bucket.sign_list_dir('/p h o t o .p n g',
                                                       timestamp=timestamp)
        assert raw_s == 'Hj1GbFeFuAwFUQNS00oJ4dlxGfI='
        # 5. Must work with unicode and space characters in filename
        raw_s = s3authclient_with_bucket.sign_list_dir(' /空格后表情：😍.png',
                                                       timestamp=timestamp)
        assert raw_s == 'gM3+CFm3kBt9tJB6rs1/Wj5ixDA='
        # 6. Must return valid Authorization HTTP header when output
        #    is set to ``http_header``.
        s = s3authclient_with_bucket.sign_list_dir('/表情：😍. p n g',
                                                   output='http_header',
                                                   timestamp=timestamp)
        assert s == 'AWS ok:qNicSQL4EGlubevSqW235pvKYhA='
        # assert http_sign == 'AWS ok:qNicS...SqW235pvKYhA='
        # 7. Must return valid query string when output is set to
        #    ``query_string``.
        qs_s = s3authclient_with_bucket.sign_list_dir(' / 格：😍. p n g',
                                                      output='query_string',
                                                      timestamp=timestamp)
        assert qs_s == 'CPe/ftegBEtPtEA0IYyft1YaVh0%3D'
        # 8. Must raise Exception when bucke_name must is provided
        with pytest.raises(Exception) as excinfo:
            s3authclient_with_bucket.sign_list_dir('/filename.png',
                                                   bucket_name='panier',
                                                   timestamp=timestamp)
        # 9. Must raise Exception when filename does NOT start with a "/".
        with pytest.raises(Exception) as excinfo:
            s3authclient_with_bucket.sign_list_dir('filename.png',
                                                   bucket_name='panier',
                                                   timestamp=timestamp)
        # 10. Must return a 10 characters length base64 string
        raw_s = s3authclient_with_bucket.sign_list_dir('/filename.png')
        # 10.1 String type
        assert isinstance(raw_s, str)
        # 10.2 28 char length
        assert len(raw_s) == 28
        # 10.3 Base64 encoded string
        try:
            raw_s.decode('base64')
        except Exception, ex:
            pytest.fail(ex.message)
        # 11. Must return a predictable signature when providing timestamp and
        #     ``mime_type``.
        s = s3authclient_with_bucket.sign_list_dir('/photo.txt',
                                                   mime_type='text/plain',
                                                   timestamp=timestamp)
        assert s == 'BujRe2aXK26szkEPXuyIWNP0D9o='
