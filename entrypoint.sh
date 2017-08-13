#!/bin/sh

while :
do
  certbot $@

  # convert symlink to regular file
  cd /etc/letsencrypt
  for file in $(find -type l)
  do
    cp -f $(readlink -f $file) $file
  done
  cd $OLDPWD

  sleep 30d
done
