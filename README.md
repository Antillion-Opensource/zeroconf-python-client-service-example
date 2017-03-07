# zeroconf Python service & client example

Demonstrates how to build a simple service that will be discovered via a Python script using zeroconf.

The service is a very simple API that responds with a tiny block of JSON. It's configured to run with the name simpleapi (defined in `simpleapi.service`).

The main client will query the network for any services and discover implementations of the service (based on it's name). Based on the discovered services it will make a request to each to obtain the simple JSON block.

## Getting started

Start the docker image(s):

    sudo docker run --net=host -it --rm antillion-os/zeroconf-example-service
    
Install the required Python dependencies:

    pip install -r client/requirements.txt

Discover the available services using the following command (you may receive a firewall notification as it will also be listening on the socket):

    python client/find_and_call.py
  
Assuming all goes well, you should see something like the following:
 

    Waiting 10s for services to become available (Ctrl+C to cancel search early)
    
    Service developmentbox simpleapi._http._tcp.local. of type _http._tcp.local. state changed: ServiceStateChange.Added
    Discovered a service: {u'path': '/api/v1', u'port': 8000, u'address': '11.0.0.11'}
    
    Querying 1 services found
    Service @ 11.0.0.11 responded with 200:{"Hello": "World!"} 



## Troubleshooting

### In the service

If you see:

    Mar  7 14:44:20 b0b7383106e2 avahi-daemon[70]: sendmsg() to 0:0:ff02:: failed: Invalid argument

Avahi is failing to broadcast to mDNS; make sure you started the container with `--net=host`.

### On the client

If you can't see your service come up, try `client/browser.py` which will show all services it can find.

Pass the `--debug` flag if you wish to see the mDNS network traffic; be warned: it's noisy.

