#!/usr/bin/env python3

import re
import threading
from pprint import pprint
from time import sleep

from prometheus_client import Gauge, Summary, start_http_server

from epsolar_exporter.epsolar import ep_solar_client, ep_solar_connect, read_all

REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")

lock = threading.Lock()


def locked_read(register):
    with lock:
        value = ep_solar_client.read_input(register).value
        #  print(f"{register} = {value}")
        return value


gauges = []


def init():
    if ep_solar_connect():
        results = read_all()
        for register, result in results:

            def purify(s):
                return re.sub(r"""['%,/ \(\)]+""", "_", s)

            name = purify(str(result.register.name).lower().strip())
            documentation = result.register.name
            unit = purify(result.register.unit()[0].lower())
            pprint({name, documentation, unit})
            gauges.append((register, Gauge(name=name, documentation=documentation, unit=unit)))
            # gauges[-1].set_function(lambda: locked_read(register))


def update_values():
    for register, gauge in gauges:
        gauge.set(locked_read(register))


def run():
    init()

    # Start up the server to expose the metrics.
    start_http_server(8000)

    while True:
        if ep_solar_connect():
            update_values()
        sleep(1)


if __name__ == "__main__":
    run()
