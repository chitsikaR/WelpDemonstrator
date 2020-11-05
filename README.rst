================
WelpDemonstrator
================


.. image:: https://img.shields.io/travis/chitsikaR/WelpDemonstrator.svg
        :target: https://travis-ci.com/chitsikaR/WelpDemonstrator

.. image:: https://readthedocs.org/projects/Welpdemonstrator/badge/?version=latest
        :target: https://WelpDemonstrator.readthedocs.io/en/latest/?badge=latest
        

.. image:: https://travis-ci.org/chitsikaR/WelpDemonstrator.png?branch=master
        :target: https://travis-ci.org/chitsikaR/WelpDemonstrator


This project contains the API to demonstrate use of our Welp API. Welp is intended to be used with wearable technology in the IoT space to send alert messages with one's current location.


* Free software: GNU General Public License v3
* Documentation: https://WelpDemonstrator.readthedocs.io.

Installation
-----------------

welpdemonstrator highly makes use of the **smtplib** library so before you begin, you need to have that package installed.

.. code-block:: bash

    $ sudo pip install smtplib
    $ sudo pip install python-firebase
    $ sudo pip install welpdemonstrator
    $ sudo apt install msmtp msmtp-mta
    $ sudo nano msmtprc
    
.. code-block::  bash
    
    # msmtp needs to be set up to send emails from your device first before attempting to run the demonstrator
    # run the following commands to install the required libraries
    # be sure to install any other dependencies if an error occurs

    # navigate to the msmtprc file on your Pi using the following:
    cd /etc/msmstprc

    # if the file does not exist, create one by running the following:
    cd /etc
    # once open in nano, add the mail host(s) of choice


    # Generics
defaults
auth           on
tls            on
# following is different from ssmtp:
tls_trust_file /etc/ssl/certs/ca-certificates.crt
# user specific log location, otherwise use /var/log/msmtp.log, however, 
# this will create an access violation if you are user pi, and have not changes the access rights
logfile        ~/.msmtp.log

# Gmail specifics
account        gmail
host           smtp.gmail.com
port           587

from           root@raspi-buster
user           # insert the email address you want to send emails from
password       # insert the password for the email account

# you may add hotmail etc

# Default chosen as gmail
account default : gmail

Features
--------

TODO
-------
* Docs must be generated.

Credits
-------
* To everyone who helped me develop this API and contributes to bug fixes

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
