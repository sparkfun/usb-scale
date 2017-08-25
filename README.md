# Reading a usb hid scale with your browser

these instructions are for the **dymo m25 postal scale** on **windows 7** but with a little hacking other scales and operating systems should be usable.

readscale.cgi is a modified version of the code found here (used with permission): http://steventsnyder.com/reading-a-dymo-usb-scale-using-python/

## How To

vendor and products ids for the m25 should be 0922 and 8004 respectively. if your scale is different, update readscale.cgi with its values. you'll also need to know them for the install procedure below.

on the computer that needs to read from the scale:

- install [python](http://www.python.org/getit/)
- install [pyusb](https://github.com/walac/pyusb) (python.exe setup.py install)
- install [libusb-win32](http://sourceforge.net/apps/trac/libusb-win32/wiki)

now we roll up a driver that python can read:

- plug the scale in and turn it on
- run LIBUSBDIR/bin/ARCH/install-filter-win.exe (choose your scale device)
- run LIBUSBDIR/bin/inf-wizard.exe (choose your scale device and "install now" at the end)
- restart the scale

run `python.exe readscale.cgi`

you should see something like `here_is_the_weight({ ounces: 0, pounds: 0})`

now to serve up that value:

- run a cgi-enabled web server (i chose [mongoose](https://code.google.com/p/mongoose/))
- browse or make an ajax call to readscale.cgi; see _example.html_

## Notes

- in my example (and probably most real world instances) jsonp is used to circumvent same-origin-policy, but if the computer with the scale is also the web server then you shouldn't have to
- i chose the mongoose web server because i was working with encrypted content and needed ssl, but if you don't you could use the built in python http.server
