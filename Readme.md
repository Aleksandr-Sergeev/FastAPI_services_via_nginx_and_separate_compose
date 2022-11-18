## Two FastAPI services running under Nginx
Repo got 3 separate docker-composes:
1. nginx as reverse proxy: http://127.0.0.1:8080/
2. movie_service: http://127.0.0.1:8080/api/v1/movies/ . Check endpoints in movie_service/app/api/movies.py 
or via openapi: http://127.0.0.1:8080/api/v1/movies/docs
3. cast_service: http://127.0.0.1:8080/api/v1/casts/ . Check endpoints in cast_service/app/api/casts.py
or via openapi: http://127.0.0.1:8080/api/v1/casts/docs

All three parts connected via Docker movies_network. Services use separate DBs and private networks. 
For further details check docker-compose files and nginx.conf. Use postman as playground.

## Setup
1. Run in terminal: docker network create movies_network
2. Either run 3 docker-compose files in services directories or modify and run script "start_containers.ps1"

### Movie_service
It got 4 methods: CRUD (look at movie-service/app/api/movies.py)

On create and update it checks if cast_id is present in cast_service DB.

Todo with adding cast via movie-service:
1. Add interface to pass cast name to create movie instance
1. Add interface to pass cast name to update movie instance
2. If name is passed, check if cast is present in cast_service DB via httpx
3. If not - add cast and return cast_id from cast_service
4. After adding movie with a cast, send RabbitMQ request to update number of movies for the cast

Todo with reducing number of movies for cast when movie deleted:
1. After deleting movie, send RabbitMQ request to update number of movies for the cast

### Cast_service
It got 2 methods: Read and Create (look at cast_service/app/api/casts.py)

Todo with managing cast via movie-service:
1. Add model {cast_id, movies_num} for cast_service
2. Add cast if cast is not present in DB
3. Receive RabbitMQ request to decrease number of movies for cast if movie deleted
3. Receive RabbitMQ request to increase number of movies for cast if movie added