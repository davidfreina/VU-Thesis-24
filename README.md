# VU MSc CS - Master Thesis

Track: IWT
Student: David Freina
Supervisor: Matthijs Jansen
Group: @Large Research

## First steps

- Setup local ssh config:
    ````
    Host node1
        HostName node1
        User dfreina
        IdentityFile ~/.ssh/vu
        ProxyJump al01.anac.cs.vu.nl
        LocalForward 6443 192.168.210.2:6443

    Host al01.anac.cs.vu.nl
        HostName al01.anac.cs.vu.nl
        User dfreina
        IdentityFile ~/.ssh/vu
    ````
    (Port forwarding just as an example, any port can be used)
<!-- - Setup kubectl
    - Using scripts/get_kube_cfg.sh and scripts/install_kubectl.sh -->

## Setup local K8s cluster

- [Installing kubeadm, kubelet and kubectl](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl)
- Configure containerd
    - ``containerd config default | sudo tee /etc/containerd/config.toml ``
    - ``sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml``
- Setup cluster: ``kubeadm init --cri-socket unix:///run/containerd/containerd.sock --pod-network-cidr=10.244.0.0/16``
- Setup kubectl
    - ``mkdir -p $HOME/.kube``
    - ``sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config``
    - ``sudo chown $(id -u):$(id -g) $HOME/.kube/config``
- [Allow pod scheduling on control node](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#control-plane-node-isolation)
    - ``kubectl taint nodes --all node-role.kubernetes.io/control-plane-``
    <!-- - ``kubectl label nodes --all node.kubernetes.io/exclude-from-external-load-balancers-`` -->
- Apply Flannel for networking
    - ``kubectl apply -f kube-flannel.yml``
- Apply kube-prometheus for monitoring
    - ``kubectl apply --server-side -f manifests/setup/``
    - ``kubectl apply -f manifests/``
- Apply kepler
    - ``make build-manifest OPTS="BM_DEPLOY PROMETHEUS_DEPLOY"``
    - ``kubectl apply -f _output/generated-manifest/deployment.yaml``
- Import Kepler Grafana dashboard
    - [Dashboard JSON](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/grafana-dashboards/Kepler-Exporter.json)

<!-- ## Kepler deployment

- Setup [kube-prometheus](https://sustainable-computing.io/installation/kepler/#deploy-the-prometheus-operator)
    - Check if Grafana is running:
        - kubectl -n monitoring port-forward svc/grafana 3000
        - Username & Password: ````admin:admin````
- Install [Helm](https://helm.sh/docs/intro/quickstart/) -->

## Image export/import

- ``docker save -o davidfreina-sleep.tar davidfreina/sleep``
- ``sudo ctr -a /run/containerd/containerd.sock --namespace k8s.io  image import --base-name davidfreina/sleep davidfreina-sleep.tar``