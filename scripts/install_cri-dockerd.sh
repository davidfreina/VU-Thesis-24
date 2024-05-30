#!/bin/sh
LATEST_VERSION=$(curl --silent -qI https://github.com/Mirantis/cri-dockerd/releases/latest | awk -F '/' '/^location/ {print  substr($NF, 2, length($NF)-2)}')
echo $LATEST_VERSION
curl -LO "https://github.com/Mirantis/cri-dockerd/releases/download/v$LATEST_VERSION/cri-dockerd-$LATEST_VERSION.amd64.tgz"
tar xf ./cri-dockerd-$LATEST_VERSION.amd64.tgz
mv ./cri-dockerd/cri-dockerd $HOME/.local/bin/
chmod +x $HOME/.local/bin/cri-dockerd
rm -r cri-dockerd-$LATEST_VERSION.amd64.tgz
