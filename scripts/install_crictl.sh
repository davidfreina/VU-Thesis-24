#!/bin/sh
LATEST_VERSION=$(curl --silent -qI https://github.com/kubernetes-sigs/cri-tools/releases/latest | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
curl -LO "https://github.com/kubernetes-sigs/cri-tools/releases/download/$LATEST_VERSION/crictl-$LATEST_VERSION-linux-amd64.tar.gz"
tar xf ./crictl-$LATEST_VERSION-linux-amd64.tar.gz
mv ./crictl $HOME/.local/bin/
chmod +x $HOME/.local/bin/crictl
rm -r crictl-$LATEST_VERSION-linux-amd64.tar.gz
