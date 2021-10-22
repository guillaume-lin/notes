1. 创建私有镜像仓库

客户端配置不安全的注册中心
/etc/docker/daemon.json
{
        "insecure-registries":["172.22.19.230:5001"]
}
重启docker守护进程

2. 创建spring镜像，使用Dockerfile
==begin here==
FROM tomcat:8.5.72-jdk8-corretto
MAINTAINER  linjingxian@hengan.com
COPY target/haecbi-admin.war /usr/local/tomcat/webapps/ROOT.war
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
==end here==
docker build -t 172.22.19.230:5001/haecbi-admin:prod-1.0 .

3. 创建deployment 部署各个服务

4. 创建statefulset 使eureka进程具有唯一的域名

5. 创建configmap使各个pod从configmap读取配置

6. 安装ingress-nginx-controller
用helm v3安装
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx

6. 创建ingress-nginx
