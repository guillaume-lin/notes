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
#
# k8s for haecbi-admin
# 2 replicate
#
apiVersion: apps/v1
kind: Deployment
metadata:
  name: haecbi-admin-deployment
spec:
  selector:
    matchLabels:
      app: haecbi-admin
  replicas: 2
  template:
    metadata:
      labels:
        app: haecbi-admin
    spec:
      containers:
      - name: haecbi-admin
        image: 172.22.19.230:5001/haecbi-admin:prod-1.0
        imagePullPolicy: Always   # 总是使用镜像中心最新的镜像
        envFrom:
        - configMapRef:
            name: prod-configmap
        ports:
        - containerPort: 8080

4. 创建statefulset 使eureka进程具有唯一的域名
#
# k8s for haecbi-eureka
# should be statefulset
# and have a fix name
#
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: haecbi-eureka-statefulset
spec:
  serviceName: haecbi-eureka
  selector:
    matchLabels:
      app: haecbi-eureka
  replicas: 1
  template:
    metadata:
      labels:
        app: haecbi-eureka
    spec:
      containers:
      - name: haecbi-eureka
        image: 172.22.19.230:5001/haecbi-eureka:prod-1.0
        imagePullPolicy: Always   # 总是使用镜像中心最新的镜像
        envFrom:
        - configMapRef:
            name: prod-configmap
        ports:
        - containerPort: 8080
        
#
# 创建eureka的headless服务
#

apiVersion: v1
kind: Service       # 对象类型为Service
metadata:
  name: haecbi-eureka
  labels:
    app: haecbi-eureka
spec:
  ports:
    - name: haecbi-eureka     # Pod间通信的端口名称
      port: 8080        # Pod间通信的端口号
  selector:
    app: haecbi-eureka        # 选择标签为app:nginx的Pod
  clusterIP: None     # 必须设置为None，表示Headless Service

5. 创建configmap使各个pod从configmap读取配置

6. 安装ingress-nginx-controller
用helm v3安装
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx

6. 创建ingress-nginx
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
      kubernetes.io/ingress.class: nginx
      # 配置正则 去掉斜杠后的第一个路径
      nginx.ingress.kubernetes.io/use-regex: "true"  
      nginx.ingress.kubernetes.io/enable-cors: "true"
      nginx.ingress.kubernetes.io/rewrite-target: /$2  # 匹配只有跳到后续路径
  name: haecbi-gateway-ingress
  namespace: default
spec:
  #ingressClassName: node-edge
  rules:
    - host: be-test.hengan.shop
      http:
        paths:
          - path: /gateway(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: haecbi-gateway-service
                port: 
                  number: 8071
          - path: /eureka(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: haecbi-eureka
                port:
                  number: 8080

