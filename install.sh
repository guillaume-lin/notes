#/bin/bash

if [ $# -lt 3 ];then
    echo "usage: $0 <server> <path> <backendUrl>"
    exit 1
fi
server=$1
dpath=$2
backendUrl=$3
cat > .env.production <<EOF
NODE_ENV = 'production'
VUE_APP_BACKEND_URL = "${backendUrl}"
EOF

npm run build
if [ $? -ne 0 ]; then
    echo "build failed."
    exit 1
fi
rsync  --delete -rvc dist/  root@$server:$dpath
if [ $? -ne 0 ]; then
    echo "rsync failed."
    exit 2
fi
ssh root@$server "chmod a+rx -R ${dpath}"
if [ $? -ne 0 ]; then
    echo "chmod failed."
    exit 3
fi
echo "deploy successfully."
