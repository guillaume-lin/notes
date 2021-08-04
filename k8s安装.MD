使用kubeadm来安装

* 先设置centos上的yum源
cat <<EOF > kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

sudo mv kubernetes.repo /etc/yum.repos.d/

设置完后用yum 安装
yum install kubeadm

* 拉取gcr.io上的镜像(所有的节点上都要有这些镜像）
到hub.docker.com上搜索下gcr.io的镜像，下载到本地

images=(  
kube-apiserver:v1.18.3
kube-controller-manager:v1.18.3
kube-scheduler:v1.18.3
kube-proxy:v1.18.3
pause:3.2
etcd:3.4.3-0
coredns:1.6.7
)

for imageName in ${images[@]} ; do
    docker pull aiotceo/$imageName
    docker tag aiotceo/$imageName k8s.gcr.io/$imageName
    docker rmi aiotceo/$imageName
done

* 初始化,用flannel作为网络
kubeadm init --pod-network-cidr=10.244.0.0/16  # 后面的参数，确保podCIDR设置
按照如下说明操作
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.22.19.242:6443 --token n4v7ta.3yjnn3ahv4691igz \
    --discovery-token-ca-cert-hash sha256:7878ed0cda3e894d96a21a0a29c13aa8bb8fd3e2323cb2d62bf0799bae0f277f
* 部署flannel网络
作为普通用户
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
* 查看状态
 kubectl get pods -n kube-system
 
* 按需安装其他组件
    
    
以下用来新增节点
# master 查看节点检查token是否有效
kubeadm token list
# 生成新的token和命令。然后在node重新执行
kubeadm token create --print-join-command



* 安装dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.1/aio/deploy/head.yaml
* 通过代理访问dashboard
kubectl port-forward --address="172.22.19.242" -n kubernetes-dashboard service/kubernetes-dashboard 8080:443
打开浏览器访问 https://172.22.19.242/ 即可访问到dashboard

* 登录dashboard
通过下方创建一个用户
https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
登录即可
