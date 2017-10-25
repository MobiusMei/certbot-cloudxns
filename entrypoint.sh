#!/bin/sh

while :
do
  certbot $@

  # convert symlink to regular file
  cp -LpR /etc/letsencrypt/live/* live-regular
  for domain in live-regular/*; do
    cat "$domain/privkey.pem" "$domain/fullchain.pem" > "$domain/bundle.pem"
  done

  sleep 30d
done
