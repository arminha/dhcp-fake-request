# coding=utf-8
from setuptools import setup

setup(
    name='dhcp-fake-request',
    version='0.0.1',
    packages=[],
    url='https://github.com/arminha/dhcp-fake-request',
    license='GPLv2',
    author='Armin Häberling',
    author_email='armin.aha@gmail.com',
    description='A command line tool for sending DHCP request packets',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['pydhcplib'],
    scripts=['send_dhcp_request.py']
)
