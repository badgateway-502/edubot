```shell
docker run -d --name edubotdb -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=nimda -e POSTGRES_DB=edubotdb -v edubotdbv:/var/lib/postgresql/data -p "5432:5432" postgres:alpine
```