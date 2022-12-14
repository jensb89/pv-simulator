## PV Simulator
Simulate the interaction between PV power values generated with a Solar Panel and a building consumption.
It assumes the following pv generator curve:
![pv generator curve](pv_curve.png)

### Prerequisits
* Rabbit MQ server running (https://www.rabbitmq.com/download.html)

### Installation
* Create a python virtualenv
* Install all dependencies: `pip install -r requirements.txt` (main dependencies:numpy, matplotlib, pika)
* Start `python pv_generator.py` in one shell
* Start `python meter.py` in another shell

### Code style
Run:
* `python -m black <file>`
* `python -m flake8 <file>`

### Tests
Run `pytest`

### Possible Improvements
* More and advanced tests :)
* The pv generator curve is approximated by a normal distribution. That's not totally correct as the sides of a given pv generator curve decrease faster. One could model the curve by a parabola and two linear sections
* Don't open the file each time for a new datapoint for the fast sim and collect values for a day first: less file operations and improved simulation time
* Spawn multiple producers at the same time (maybe even as separate threads) or use direct exchanges
* Improved logging 

Future ideas:
* Flask application for liveview web application