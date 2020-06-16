This contains code for a small project to monitor and document the
water usage of my garden sprinkler system.

This can help understand where the cost goes, if there are unexpected
leaks etc.

There are a few projects like that on github already, but they seemed
either overkill or didn't really meet what I needed.


Hardware:

* I sat up a in-line hall flow meter such as 
  * https://www.amazon.com/dp/B07MY6LFPH
  * https://www.amazon.com/DIGITEN-Sensor-Switch-Flowmeter-Counter/dp/B00VKAT9VA
  * https://www.amazon.com/FASTROHY-Sensor-Copper-Effect-Flowmeter/dp/B07JZXBKJR
  * https://www.banggood.com/DN20-G34-Copper-Water-Flow-Sensor-Pulse-Output-1_75Mpa-245Lmin-Flowmeter-p-1266296.html
  * https://www.aliexpress.com/item/32247118868.html

These flow meters all seem the same model, rebranded, but I have not
compared them. While they are inexpensive, it was not trivial to
install them without leaking - I'm also not certain about their
long-term reliability yet.

My flowmeter says that it's frequency is 5.5 Hz * Q, where Q is the
flow in litres/minute.  That means one liter trnaslates into 330
pulses. I let the sprinkler run for a few minutes, checked our
official utility water meter before and after, and compared with the
number of pulses on the flow meter. As far as I can tell, the flow
meter is fairly accurate (less than 10% deviation).

* I also used an elderly esp8266 wemos D1 with micropython.  I just
connected GND and 5V to the flow meter and the data pin to D4
(GPIO2?).

* I run the main.py on the Wemos D1. Other than configuring the
  network, the only other thing to do here is to specify where to send
  the measured data to.

* Since I don't trust the D1 to stay up for extended periods of time,
  I periodically send the collected data to a separate server that
  keeps a more permanent log. The water_server.go file implements the
  server, you can start it with ```go run water_server.go```. I do
  this in a screen session on a raspberry pi for now.

* Finally, I included a small python script to plot the data. 


PUBLIC DOMAIN ----------------------------------------------------------------------

	I, the copyright holder of this work, hereby release it into
	the public domain. This applies worldwide.

	In case this is not legally possible, I grant any entity the
	right to use this work for any purpose, without any
	conditions, unless such conditions are required by law.
