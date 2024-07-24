<h1>Urls</h1>

<h2>api/v1/users/</h2>
<h3>GET</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```

<b>output data: </b>

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "{User.id}",
            "username": "{User.username}",
            "email": "{User.email}",
            "language": {
                "id": 1,
                "code": "{Language.code}",
                "name": "{Language.name}"
            }
        }
    ]
}
```
<h2>api/v1/users/{User.id}/</h2>
<h3>GET</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```



<b>output data: </b>

```json
{
    "id": "{User.id}",
    "username": "{User.username}",
    "email": "{User.email}",
    "language": "{Language.id}"
}
```

<h3>PUT</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```

<b>input data: </b>

```json
{
  "email": "{User.email}",
  "other_fields": "other_fields"
}
```

<b>output data: </b>

```json
{
    "id": "{User.id}",
    "username": "{User.username}",
    "email": "{User.email}",
    "language": "{Language.id}"
}
```
<h3>DELETE</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```

<b>input data: </b>

```json
```

<b>output data: </b>

```json
```

<h2>api/v1/users/{User.id}/cars/</h2>
<h3>GET</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```



<b>output data: </b>

```json
{
    "id": "{User.id}",
    "username": "{User.username}",
    "email": "{User.email}",
    "language": "{Language.id}",
    "cars": [
        {
            "id": "{Car.id}",
            "creation_year": "{Car.creation_year}",
            "time_add": "{Car.time_add}",
            "name": "This car`s name is not supported in {User.username}`s language"
        },
        {
            "id": "{Car.id}",
            "creation_year": "{Car.creation_year}",
            "time_add": "{Car.time_add}",
            "name": "{Car.name}"
        }
    ]
}
```

<h2>api/v1/users/{User.id}/add_cars/</h2>
<h3>PUT</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```

<b>input data: </b>

```json
{
  "cars": [
    "{Car.id}", 
    "{Car.id}"
  ]
}
```

<b>output data: </b>

```json
{
  "status": "ok",
  "cars": [
    "{Car.id}", 
    "{Car.id}"
  ]
}

```
<h2>api/v1/users/register/</h2>

<h3>POST</h3>

<b>input data: </b>

```json
{
  "username": "{User.username}",
  "email": "{User.email}",
  "password": "{User.password}",
  "language": "{Language.id}"
}
```

<b>output data: </b>

```json
{
  "username": "{User.username}",
  "email": "{User.email}",
  "language": "{Language.id}"
}
```

<h2>api/v1/auth/token/login/</h2>

<h3>POST</h3>

<b>input data: </b>

```json
{
  "email": "{User.email}",
  "password": "{User.password}",
}
```

<b>output data: </b>

```json
{
  "access_token": "{Token.token}"
}
```

<h2>api/v1/auth/token/logout/</h2>

<h3>POST</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```

<b>input data: </b>

```json
```

<b>output data: </b>

```json
```

<h2>api/v1/cars/create/</h2>

<h3>POST</h3>

<b>headers: </b>
```json
{
  "Authorization": "Token {Token.token}"
}
```

<b>input data: </b>

```json
{
    "name": "{CaTranslatedName.name}",
    "car": {
        "creation_year": "{Car.creation_year}"
    },
    "language": "{Language.id}"
}
```


<b>output data: </b>

```json
{
    "name": "{CaTranslatedName.name}",
    "car": {
        "id": "{Car.id}",
        "creation_year": "{Car.creation_year}",
        "time_add": "{Car.time_add}"
    },
    "language": "{Language.id}"
}
```


<h1>Setup</h1>

```commandline
docker-compose up --build -d
```

```commandline
docker exec -it "{web contaiter name}" "python manage.py test"
```