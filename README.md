# Reading a Usb HID Scale with your Browser

These instructions are for the **Dymo M25 postal scale** on **Windows 8**, 
**Windows 10**, or **Mac OS X** but with a little hacking other scales and 
operating systems should be usable.

readscale.cgi is a modified version of the code found here (used with 
permission): http://steventsnyder.com/reading-a-dymo-usb-scale-using-python/

The newest version serves the scale values via Websockets

## How To

Vendor and products ids for the m25 should be 0922 and 8004 respectively. If 
your scale is different, update readscale.py with its values. you'll also need 
to know them for the install procedure below.

### Installation
On the computer that needs to read from the scale:

- Install [python](http://www.python.org/getit/)
- Install gevent and gevent-websocket ```pip install gevent gevent-websocket```

For Windows installations:
- Install pyusb ```pip install pyusb```
- Install the proper driver so that Python can talk to the scale on 
Windows.  There are many ways to do this, but the recommeded method is with 
[**Zadig**](http://zadig.akeo.ie/)
  - Plug in the scale and turn it on
  - Open **Zadig**
  - Click ```Options > List All Devices```
  - Select ```M25 25 lb Digital Postal Scale```
  - Click ```Install Driver```

For Mac OSX installations:
- Install hidapi ```pip install hidapi```

### Creating Certificates and Keys
If you need to serve the scale values over **HTTPS** (which you probably 
should).  You will need a certificate and private key. 

Here is an example of creating keys and certs using **OpenSSL**
```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
```

### Testing the Scale Server
We should now be ready to test that the scale server is working correctly

Now to serve up that value:

- Start the server
```bash
python scaleServer.py -k <keyfile> -c <certfile>
```
- Open a browser and go to _https://localhost:8000/_
- Validate the the scale values will live update in the form 
provided!  Clicking `record` will lock in the values and close the websocket

### Using the Server in your Application

To use the server in your own web app, just make the appropriate changes to 
the code found within the `<script>` tags in `templates/index.html`
