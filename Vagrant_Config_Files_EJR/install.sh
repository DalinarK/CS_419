#!/bin/bash

#
# SIMPLIFIED ADVISING SCHEDULING
#
# Vagrant installation script (for testing)
#

# Make sure .msmtprc exists and set permissions
touch /home/vagrant/.msmtprc
chmod 600 /home/vagrant/.msmtprc

# Make sure .fetchmailrc exists and set permissions
touch /home/vagrant/.msmtprc
chmod 600 /home/vagrant/.fetchmailrc

# Create vagrant user's Mail directory
mkdir /home/vagrant/Mail

# Update APT package database
sudo apt-get update

# Install supplementary packages for implementation and testing
sudo apt-get -y install vim
sudo apt-get -y install openssl ca-certificates
sudo apt-get -y install msmtp
sudo apt-get -y install fetchmail
sudo apt-get -y install procmail
sudo apt-get -y install mutt
sudo apt-get -y install sqlite3

# Create our Python modules directory and copy modules to it
sudo mkdir -p /usr/local/lib/python2.7/dist-packages/appt
sudo chmod g+w /usr/local/lib/python2.7/dist-packages/appt
sudo cp /vagrant/PythonFiles/appt_email.py /usr/local/lib/python2.7/dist-packages/appt
sudo cp /vagrant/UIFiles/appt_ui_func.py /usr/local/lib/python2.7/dist-packages/appt
sudo touch "/usr/local/lib/python2.7/dist-packages/appt/__init__.py"

# Create our Python executables directory and copy executables to it
sudo mkdir -p /opt/appt
sudo cp /vagrant/UIFiles/appt_ui.py /opt/appt
sudo cp /vagrant/parse.py /opt/appt
sudo cp /vagrant/email /opt/appt
sudo chmod +x /opt/appt/appt_ui.py

# Create the vagrant user's .appt configuration file and
# database directory. Set file permissions to restrict reading
# and writing.
mkdir /home/vagrant/.appt
chmod 700 /home/vagrant/.appt
cp /vagrant/credentials.py /home/vagrant/.appt
chmod 600 /home/vagrant/.appt/credentials.py
sudo touch "/home/vagrant/.appt/__init__.py"

# Create db for testing
cd /home/vagrant/.appt
python /vagrant/tableCreate_withdates.py

# Change ownership for all files under vagrant's .appt directory
cd ..
sudo chown --recursive vagrant:vagrant /home/vagrant/.appt

# Add vagrant user to the staff group.
sudo usermod -a -G staff vagrant

# Add alias to appt_ui in /etc/profile, don't echo to console
echo "alias appt_ui=/opt/appt/appt_ui.py" | tee --append /etc/profile > /dev/null
