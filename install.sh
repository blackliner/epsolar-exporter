#!/bin/bash

set -euxo pipefail

sudo python3 -m pip install .

sudo cp epsolar_exporter.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable epsolar_exporter.service
sudo systemctl restart epsolar_exporter.service
