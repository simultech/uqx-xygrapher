clear

echo "Updating git"
git pull
echo "Restarting apache"
/etc/init.d/httpd restart