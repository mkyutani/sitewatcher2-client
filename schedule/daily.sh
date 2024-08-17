#/bin/env sh
echo ========  $(date) ========
echo ---- ping
sudo docker run --net=sw2nw --rm sw2
echo ---- update resources
sudo docker run --net=sw2nw --rm sw2 d update all
echo ---- collect resources in channels
sudo docker run --net=sw2nw --rm sw2 c collect all
echo ---- share new resources to slack
sudo docker run --net=sw2nw --rm sw2 c share all slack