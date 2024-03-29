server {
    listen      80;
    server_name jct.cottagelabs.com api.jct.cottagelabs.com;

    location ^~ /.well-known/acme-challenge/ {
        default_type "text/plain";
        root /var/www/letsencrypt;
    }
    location = /.well-known/acme-challenge/ {
        return 404;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
  listen 443 ssl;
  server_name jct.cottagelabs.com;
  root /home/cloo/dev/journalcheckertool/ui/public;

  ssl_certificate /etc/letsencrypt/live/jct.cottagelabs.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/jct.cottagelabs.com/privkey.pem;

  add_header Pragma public;
  add_header Cache-Control "public";
  add_header Access-Control-Allow-Origin *;

  location = /static/jct_plugin.js {
    return 301 /js/jct_plugin.js;
  }
  location = /static/css/plugin.css {
    return 301 /css/plugin.css;
  }
}

upstream noddy_jct_dev {
    server localhost:3002;
}

server {
    listen          443 ssl;
    server_name     api.jct.cottagelabs.com;

    ssl_certificate /etc/letsencrypt/live/api.jct.cottagelabs.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.jct.cottagelabs.com/privkey.pem;

    location / {
        proxy_pass http://noddy_jct_dev/api/service/jct/;
        add_header Access-Control-Allow-Methods 'GET, PUT, POST, DELETE, OPTIONS';
        add_header Access-Control-Allow-Headers 'X-apikey,X-id,DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
