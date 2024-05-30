#!/bin/sh
curl --create-dirs --output-dir $HOME/.local/bin -LO "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
mv $HOME/.local/bin/minikube-linux-amd64 $HOME/.local/bin/minikube
chmod +x $HOME/.local/bin/minikube
