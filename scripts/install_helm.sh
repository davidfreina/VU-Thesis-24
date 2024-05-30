#!/bin/sh
LATEST_VERSION=$(curl --silent -qI https://github.com/helm/helm/releases/latest | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
curl -LO "https://get.helm.sh/helm-$LATEST_VERSION-linux-amd64.tar.gz"
tar xf ./helm-$LATEST_VERSION-linux-amd64.tar.gz
mv ./linux-amd64/helm $HOME/.local/bin/
chmod +x $HOME/.local/bin/helm
rm -r ./helm-$LATEST_VERSION-linux-amd64.tar.gz ./linux-amd64/
