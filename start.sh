echo "Setting up container"

if [ -z $NETBOX_URL ] || [ -z $NETBOX_TOKEN ] || [ -z $API_USERNAME ] || [ -z $API_PASSWORD ]
then
    echo "You must specify NETBOX_URL & NETBOX_TOKEN & API_USERNAME & API_PASSWORD"
else
    echo "Setting up API Settings"
    sed -i 's#netbox_url=".*"#netbox_url="'$NETBOX_URL'"#' app.py
    sed -i 's#netbox_token=".*"#netbox_token="'$NETBOX_TOKEN'"#' app.py

    echo "Setting up API Auth"
    sed -i 's#".*":#"'$API_USERNAME'":#' app.py
    sed -i 's#(".*")#("'$API_PASSWORD'")#' app.py

    echo "Starting API"
    flask run
fi