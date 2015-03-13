import setuptools
from s3signedauth.version import Version


setuptools.setup(name='s3-signed-auth',
                 version=Version('0.0.1').number,
                 description='Sign and authenticate AWS S3 HTTP requests',
                 long_description=open('README.rst').read().strip(),
                 author='Julien Buty',
                 author_email='julien.buty@gmail.com',
                 url='http://github.com/nepsilon/s3-signed-auth',
                 py_modules=['s3-signed-auth'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='s3 aws http rest authenticate',
                 classifiers=['Development Status :: 4 - Beta',
                              'License :: OSI Approved :: MIT License',
                              'Topic :: Internet :: WWW/HTTP',
                              'Programming Language :: Python',
                              'Environment :: Web Environment'])
