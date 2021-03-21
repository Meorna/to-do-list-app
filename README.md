# to-do-list-app

##  Build dockers
```
docker-compose build
```

### Launch dockers
```
docker-compose up
```

### Swagger
```
http://0.0.0.0:5001/docs/

Example swagger token : Bearer: jwt-token
```

### Web site
```
http://0.0.0.0:8080/

Example login : 
    Username : romane
    Password : romane 
```

### Functionality
```
Back
    - POST /account 
    - POST /login 
    - GET /lists/{id_list}
    - DELETE /lists/{id_list}
    - PATCH /lists/{id_list}
    - PUT /lists 
    - GET /lists
    - GET /lists/todos/{id_list}/{id_todo}
    - DELETE /lists/todos/{id_list}/{id_todo} 
    - PATCH /lists/todos/{id_list}/{id_todo} 
    - PUT /lists/todos/{id_list}
    - GET /lists/todos/{id_list}
    - Swagger 
Front
    - /signup Route 
    - /login Route 
    - /home Route when auth (need jwt-token)
    - /tasks/{list_id} when auth (need jwt-token)
    - password hash
    - Add list (plus)
    - View list (eye)
    - Edit name list (pen)
    - Trash list (trash)
    - Validate or invalidate edit task (V or X)
    - View task (eye)
    - Edit name (pen)
    - Trash task (trash)
Docker:
    - Dockerfile front
    - .dockerignore node-modules
    - Dockerfile back
    - docker-compose
```