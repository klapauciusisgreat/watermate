import time
from machine import Pin
import urequests as requests
import ujson
import urandom
import network
import gc

ALIVE_PING_INTERVAL = 360 # send empty packet every that many seconds
                          # otherwise only send when water is flowing
REQUEST_URL = '192.168.1.2:7777/waterworld' # server to save log to

sta_if=network.WLAN(network.STA_IF)
pin = Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
count = 0
frequency = 0

def total():
    global frequency
    global count
    frequency = count
    count = 0
    
# this Interrupt handler just increases the count of puses seen
def counterfn(x):
    global count
    count+=1



def sendUpdate(total):
    nonce = urandom.getrandbits(5)
    post_data = ujson.dumps({ 'Pulses': total, 'Random': nonce, 'Checksum': total ^ nonce })
    try:
	requests.post(REQUEST_URL, headers = {
            'content-type': 'application/json'}, data = post_data)
        print('sent: %d' % total)
    except:
	print("could not connect?")


def runme():
    global total
    global frequency
    pin.irq(counterfn, Pin.IRQ_FALLING)
    count = 0
    while True:
        # if not connected, we don't even try to accumulate pulses and
        # send them off, do it later instead
        if sta_if.isconnected():
            total()
	    if frequency != 0:
              sendUpdate(frequency)
              # Note: for now, if sending fails (e.g. network
              # issues or server down), our packet are dropped
              # on the floor.  TODO: keep them bottled up and
              # resend when online again
            if count % ALIVE_PING_INTERVAL == 0:
              sendUpdate(0)
              gc.collect()
	# note: when I wrote this, I naively thought I send an update every second.
	# In reality, the http requests take time, and when they are completed, *then*
	# I wait 1 second. This means that requests are spaced out in somewhat 
	# irregular intervals. If this were to become a problem we'd have to do something 
	# more complicated.
	time.sleep(1)


runme()
