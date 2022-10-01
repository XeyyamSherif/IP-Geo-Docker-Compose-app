# IP-Geo-FastApi-app

unittestləri etməyə çatdıra bilmədim, amma pytest təcrübəm var,vaxt azlığından basic app yaratmağa çalışdım, istəsəz modəllər ve funksionallıqlar(password hashing, error handling və s.) barədə istənilən əlavələri də edə bilərəm. 

### Proqramın çalışdırılması:
 - resository-ni komputerinizə yükləyin
 - repositorynin olduğu file üçün terminalda "docker-compose up" commandını daxil edin 



### Bu postman collectionda bütün url nümunələri var:
##### https://go.postman.co/workspace/Team-Workspace~b7928d26-f491-411d-800c-995ccbf0ebdd/collection/13456460-89d9f768-9839-4bae-8001-02f902e7d08b


### swaggear ui:
##### http://127.0.0.1:8000/docs



### tokenlərin istifadəsi

User login etdikdən sonra 2 token verir: refresh token və access token
access token useri logged in protected etmek üçün edin, refresh tokeni acces tokeni yeniləmək üçün


http://127.0.0.1:8000/sign_up   -  POST method ilə  json formatında  "id, first_name, password" gəndərin. 'first_name' logində username kimi işlədin<br />
http://127.0.0.1:8000/login     -  login üçün 'username və password'  json formatında göndərin  (response de acces token və refresh token olacaq)<br />
http://127.0.0.1:8000/user      -  url i ilə birlikdə header olaraq "Bearer acces token" request edin, bu url-i login etmiş userin datasıı yoxlamaq üçün
istifade edin <br />
http://127.0.0.1:8000/logut     -  üçün də eyni requesti edin <br />
http://127.0.0.1:8000/refresh   -  urllə birlikdə "Bearer refresh token request edin" <br />
http://127.0.0.1:8000/task      -  response olaraq task id gelecek <br />
http://127.0.0.1:8000/status    -  celery task id ni  <br />
```
{
    "id": "task id"
}
```

kimi gonderin

