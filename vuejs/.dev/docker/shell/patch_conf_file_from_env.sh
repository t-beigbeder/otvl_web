if [ ! -f $1.ori ] ; then
  cp -p $1 $1.ori
fi
sed -i -e "s=@WEB_PORT@=${WEB_PORT}=" $1
sed -i -e "s=@WEB_SERVER@=${WEB_SERVER}=" $1
sed -i -e "s=@API_PORT@=${API_PORT}=" $1
sed -i -e "s=@SERVER_NAME@=${SERVER_NAME}=" $1
sed -i -e "s=@APP_PORT@=${APP_PORT}=" $1
sed -i -e "s=default_api_server_url=https://${SERVER_NAME}:${APP_PORT}/api=" $1
sed -i -e "s=default_web_server_url=https://${SERVER_NAME}:${APP_PORT}=" $1
