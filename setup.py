# coding=utf-8
"""
Smart console tool to find file duplicates
"""
from setuptools import setup


version = __import__('find_duplicates').__VERSION__

setup(
    name='find-duplicates',
    version=version,
    url='http://github.com/iamtio/find-duplicates/',
    license='BSD',
    author='Igor Tsarev',
    author_email='iam@tio.so',
    description='Smart console tool to find file duplicates',
    long_description=__doc__,
    packages=[],
    scripts=['find_duplicates.py'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    entry_points={'console_scripts': [
        'find_duplicates = find_duplicates:main',
    ]}
)
