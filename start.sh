echo "Setting up container"

if [ -z $NETBOX_URL ] || [ -z $NETBOX_TOKEN ]
then
    echo "You must specify NETBOX_URL & NETBOX_TOKEN"
else
    echo "Setting up API Settings"
    sed -i 's#netbox_url=".*"#netbox_url="'$NETBOX_URL'"#' app.py
    sed -i 's#netbox_token=".*"#netbox_token="'$NETBOX_TOKEN'"#' app.py

    echo "Starting app"
    flask run
fi