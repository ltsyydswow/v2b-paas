#!/bin/bash

# 检查是否是root用户
if [[ $EUID -ne 0 ]]; then
    echo "请以root用户运行此脚本。"
    exit 1
fi

# 检测是否已安装nginx并安装
if ! command -v nginx &> /dev/null; then
    echo "未检测到已安装的nginx，即将进行安装..."
    apt update
    apt install -y nginx

    # 检查nginx是否安装成功
    if ! command -v nginx &> /dev/null; then
        echo "安装nginx失败，请检查网络或手动安装nginx后再试。"
        exit 1
    fi

    echo "nginx安装成功！"
fi

# 获取用户输入的域名
read -p "请输入您要绑定在VPS上的域名: " domain

# 检查域名是否已绑定在VPS上
ping_result=$(ping -c 1 "$domain" | grep "bytes from")

while [ -z "$ping_result" ]; do
    read -p "域名未绑定在VPS上，请重新输入您要绑定在VPS上的域名: " domain
    ping_result=$(ping -c 1 "$domain" | grep "bytes from")
done

# 获取用户输入的需要反向代理的网站
read -p "请输入需要反向代理的网站URL: " target_url

# 配置反向代理
config_file="/etc/nginx/sites-available/$domain"

echo "server {
    listen 80;
    server_name $domain;
    location / {
        proxy_pass $target_url;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}" > "$config_file"

ln -s "$config_file" "/etc/nginx/sites-enabled/"

# 检查配置文件是否正确
nginx -t

# 重启nginx
service nginx restart

echo "反向代理配置完成！"
