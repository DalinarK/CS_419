#!/usr/bin/env bash
pwd
pwd
pwd
pwd
chmod 0600 ../../../home/vagrant/.msmtprc
chmod 600 ../../../home/vagrant/.fetchmailrc
mkdir ../../../../home/vagrant/Mail
sudo apt-get update
sudo apt-get install vim
echo Y | sudo apt-get install vim
sudo apt-get install openssl ca-certificates
echo Y | sudo apt-get install openssl ca-certificates
sudo apt-get install msmtp
echo Y | sudo apt-get install msmtp
sudo apt-get install fetchmail
echo Y | sudo apt-get install fetchmail
sudo apt-get install procmail
echo Y | sudo apt-get install procmail
sudo apt-get install mutt
echo Y | sudo apt-get install mutt
sudo apt-get install sqlite3
echo Y | sudo apt-get install sqlite3
python ../../../../vagrant/tableCreate.py
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi