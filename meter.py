from broker import Broker
from enum import Enum

import random
import datetime
import json
import time


# Enum defining the simulation type
class SimType(Enum):
    REALTIME = 1
    FAST = 2


# Class that defines the meter, used to simulate the readings of the electrical consumption of a building
class Meter(object):
    def __init__(self, sim_mode: SimType = SimType.FAST) -> None:
        """
        Constructor for the class.
        """
        self.sim_mode = sim_mode
        # we always start at 0s of the day for a fast sim
        if sim_mode == SimType.FAST:
            self.time = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        else:
            self.time = datetime.datetime.now()

        # Init the broker
        self.broker = Broker()

    def run(self, cadence=1, sleepTime=1 / 1000) -> None:
        """
        > The function runs in a loop, generating a new sample every `cadence` seconds, and sending it
        to the broker

        :param cadence: the time between samples, defaults to 1s (optional)
        :param sleepTime: the amount of time to sleep between sending a new sample, defaults to 1ms for the fast sim and is ignored for the realtime sim (optional)
        """

        while True:
            newTime = self.time + datetime.timedelta(seconds=cadence)
            if newTime.day != self.time.day:
                break

            newSample = self.generateNewSample()
            self.sendData(newTime, newSample)

            self.time = newTime
            if self.sim_mode == SimType.REALTIME:
                time.sleep(cadence)
            else:
                time.sleep(sleepTime)

    def generateNewSample(self) -> float:
        """
        This function generates a new meter value
        :return: A random number between 0 and 9000
        """
        return random.randint(0, 9000)

    def sendMessageToBroker(self, payload) -> None:
        """
        This function sends a message to the broker

        :param payload: The message to send to the broker
        """
        self.broker.send(payload)

    def sendData(self, date: datetime, value) -> None:
        """
        This function takes a date and a value, creates a JSON object with those two values, and sends it to the broker

        :param date: The date and time of the reading
        :type date: datetime
        :param value: the value to send to the broker
        """
        data = {"time": date.isoformat(), "meterValue": value}
        self.sendMessageToBroker(json.dumps(data))


if __name__ == "__main__":
    generator = Meter()
    # Generate new power value and send it to the broker
    generator.run(cadence=1, sleepTime=0.001)
