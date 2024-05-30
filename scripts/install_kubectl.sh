#!/bin/sh
STABLE_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
curl --create-dirs --output-dir $HOME/.local/bin -LO "https://dl.k8s.io/release/$STABLE_VERSION/bin/linux/amd64/kubectl"
chmod +x $HOME/.local/bin/kubectl
