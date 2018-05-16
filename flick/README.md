# Flick
A web application to control the Philips Hue smart lights in your home.

## Prerequisites
To get this site up and running, you'll need a few things:

* [Python 3.5+](https://www.python.org/downloads/)
  * Django  1.11+
    * `pip3 install django`
  * Pycrypto
    * `pip3 install pycrypto`

## Running the Site
Clone the repository from GitHub, then navigate to the base directory.
```bash
$ git clone https://github.com/kogw/djdashboard.git
$ cd djdashboard/
```

Start the server.
```bash
$ python3 manage.py runserver
```

Navigate to `localhost:8000/flick` in your web browser.

## Getting Started
To interact with the Philips Hue smart lights in your home, Flick needs two things:

* the IP address of your Philips Hue bridge
* a free Philips Hue developer account, to obtain an API username ([detailed here](https://www.developers.meethue.com/documentation/getting-started))

The first time you start the site, you will need to specify these two pieces of information. Flick will store these credentials locally so you don't have to reauthenticate every time.

### About Your Data
Your credentials are stored on-device only. 
They are encrypted with 256-bit AES encryption, using a randomly generated initialization vector and a normalized string of your device's MAC address as the key. 
Your key is not written or stored anywhere on-device - Flick programmatically reads your device's MAC address at (and only at) encryption/decryption time.

Note that you will need to re-input the two aforementioned credentials when running Flick on a new machine.