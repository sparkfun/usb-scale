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

- Install [python 2.7](http://www.python.org/getit/)
- Update your path information so that you can use `pip` and `python` in the shell
  - Right Click on the Start icon
  - Select `System`
  - Select `Advanced system settings`
  - Click on `Environment Vriables...`
  - Select `Path` from the `System variables` list
  - Click `Edit...`
  - Verify or add entries for `C:\Python27\` and `C:\Python27\scripts\`
  - Click `OK` to exit from the menus 
  - If you are still having issues running `pip` you can also replace the `pip` commands below with 
  ```bash
  python -m pip install ...
  ```
  
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
  - We've had the best luck with the `libusbK` driver, but you may have to play around a little
  - Click ```Install Driver```
  - You should disconnect and reconnect the scale at this point

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
