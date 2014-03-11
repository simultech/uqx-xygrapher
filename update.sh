if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi
clear

echo "Updating git"
git pull
echo "Restarting apache"
service httpd graceful
echo "Restarted"