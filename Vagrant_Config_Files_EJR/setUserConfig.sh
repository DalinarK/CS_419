#!/usr/bin/env bash
# set user profiles
python /vagrant/setupConfigs.py

if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi
