sed -i -e "s=@WEB_PORT@=${WEB_PORT}=" $1
sed -i -e "s=@WEB_SERVER@=${WEB_SERVER}=" $1
sed -i -e "s=@API_PORT@=${API_PORT}=" $1
sed -i -e "s=@API_SERVER@=${API_SERVER}=" $1
sed -i -e "s=@RPX_PORT@=${RPX_PORT}=" $1
sed -i -e "s=@RPX_SERVER@=${RPX_SERVER}=" $1

sed -i -e "s=@SERVER_NAME@=${SERVER_NAME}=" $1
sed -i -e "s=@APP_PORT@=${APP_PORT}=" $1
