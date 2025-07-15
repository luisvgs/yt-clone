# Youtuble Clone

Instrucciones para correr:

1) Clona el repositorio con `git clone https://github.com/luisvgs/yt-clone.git`
2) Ingresar a la raiz del proyecto `cd yt-clone`
3) Correr los siguientes comandos: 
````
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
````

4) acceder a la url `http://localhost` en el navegador

Para correr los tests, ejecutar: `python manage.py test` 
