#### Setup and run 


``` sh
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py runserver

```
 
#### Example  postman

``` sh
GET http://127.0.0.1:8000/api/test?part=2&name=/home/oleg/Pictures/12.png
part -  количество разбиений 
name - путь до картинки

Ответ
{
    "Gamogen": "NOT"
}
```
 