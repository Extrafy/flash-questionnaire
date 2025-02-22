tg=$1
docker build -t flashq/frontend:"$tg" .
docker push flashq/frontend:"$tg"