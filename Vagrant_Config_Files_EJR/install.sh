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
sudo mkdir -p /usr/local/lib/python2.7/dist-packages/appt
sudo chmod g+w /usr/local/lib/python2.7/dist-packages/appt
sudo cp /vagrant/PythonFiles/appt_email.py /usr/local/lib/python2.7/dist-packages/appt
sudo cp /vagrant/UIFiles/appt_ui_func.py /usr/local/lib/python2.7/dist-packages/appt
sudo touch "/usr/local/lib/python2.7/dist-packages/appt/__init__.py"
sudo mkdir -p /opt/appt
sudo cp /vagrant/UIFiles/appt_ui.py /opt/appt
sudo cp /vagrant/parse.py /opt/appt
sudo cp /vagrant/email /opt/appt
sudo chmod +x /opt/appt/appt_ui.py
mkdir /home/vagrant/.appt
chmod 700 /home/vagrant/.appt
cp /vagrant/credentials.py /home/vagrant/.appt
chmod 600 /home/vagrant/.appt/credentials.py
sudo touch "/home/vagrant/.appt/__init__.py"
cd /home/vagrant/.appt
# Create db with usable date strings
python /vagrant/tableCreate_withdates.py
cd ..
sudo chown --recursive vagrant:vagrant /home/vagrant/.appt
sudo usermod -a -G staff vagrant
# Add alias to appt_ui in /etc/profile, don't echo to console
echo "alias appt_ui=/opt/appt/appt_ui.py" | tee --append /etc/profile > /dev/null
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi
