#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install vim
sudo apt-get install openssl ca-certificates
sudo apt-get install msmtp
sudo apt-get install fetchmail
sudo apt-get install procmail
sudo apt-get install mutt
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi