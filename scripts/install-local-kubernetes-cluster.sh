#!/bin/sh
CNI_PLUGINS_VERSION=$(curl --silent -qI https://github.com/containernetworking/plugins/releases/latest | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
CRICTL_VERSION=$(curl --silent -qI https://github.com/kubernetes-sigs/cri-tools/releases/latest | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
KUBERNETES_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)

echo "Install CNI Plugins"

DEST="/opt/cni/bin"
sudo mkdir -p "$DEST"
curl -L "https://github.com/containernetworking/plugins/releases/download/${CNI_PLUGINS_VERSION}/cni-plugins-linux-amd64-${CNI_PLUGINS_VERSION}.tgz" | sudo tar -C "$DEST" -xz

echo "---"

echo "Install crictl"

curl -LO "https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-amd64.tar.gz"
tar xf ./crictl-$CRICTL_VERSION-linux-amd64.tar.gz
mv ./crictl $HOME/.local/bin/
chmod +x $HOME/.local/bin/crictl
rm -r crictl-$CRICTL_VERSION-linux-amd64.tar.gz

echo "---"

# Install kubernetes tools

curl --create-dirs --output-dir $HOME/.local/bin -LO "https://dl.k8s.io/release/$STABLE_VERSION/bin/linux/amd64/kubectl"
chmod +x $HOME/.local/bin/kubectl

curl --create-dirs --output-dir $HOME/.local/bin -L --remote-name-all https://dl.k8s.io/release/${KUBERNETES_VERSION}/bin/linux/amd64/{kubeadm,kubelet}
chmod +x $HOME/.local/bin/kubeadm
chmod +x $HOME/.local/bin/kubelet

DOWNLOAD_DIR="$HOME/.local/bin"
RELEASE_VERSION="v0.16.2"
mkdir -p $HOME/.local/share/systemd/user
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/krel/templates/latest/kubelet/kubelet.service" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | tee $HOME/.local/share/systemd/user/kubelet.service
mkdir -p $HOME/.local/share/systemd/user/kubelet.service.d
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/krel/templates/latest/kubeadm/10-kubeadm.conf" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | tee $HOME/.local/share/systemd/user/kubelet.service.d/10-kubeadm.conf


