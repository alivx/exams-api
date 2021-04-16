To Run app:

```
docker-compose build
docker-compose up
# Or
docker-compose up -d #To run it in the background
```


To Upload all Json under Files dir, run the shell below:
```
for f in files/*.json;  do
    filex="$PWD/${f}"
    curl --location --request POST 'http://127.0.0.1:8000/files/' \
    --header 'accept: application/json' \
    --header 'Content-Type: multipart/form-data' \
    --form file=@"${filex}"
done;
```

To put new item to the database:
```
curl --location -g --request PUT 'http://127.0.0.1:8000/items/{item_id}?question=What%20is%20is&options1=is%201&options2=is%202s&options3=iss%203&options4=iss%204&answer=is%202&material=Arabic' \
--header 'accept: application/json'
```