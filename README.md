# small-test
Small programing test from Open Web Technologies

## How to run:

Just install `pipenv`, go to the folder and run commands :
```bash
cd /path/to/small-test/
pipenv shell
cd code/
python api.py
```

## Example of REST API:

 * GET on http://localhost:8080/skill/research with
    ```json
    {
        "name":"java"
    }
    ```
    to get all skills with the "java" name

* GET on http://localhost:8080/user/research with
    ```json
    {
        "firstname":"Romain",
        "skills": [1]
    }
    ```
    to get all users with firstname "Romain" and skills with id 1.

* PUT on http://localhost:8080/user/create with
  ```json
  {
	"fullname": "Romain Mencattini",
	"user_id": 1,
	"email": "mrl@bluewin.ch",
	"address": "21c rue de graman",
	"firstname": "Romain",
	"lastname": "Mencattini",
	"mobile_phone":"07893",
	"skills": [1,2]
  }
  ```

* PUT on http://localhost:8080/skill/create with
  ```json
  {
	"name":"java",
    "level":"junior",
    "users":[1,2]
  }
  ```

* POST on http://localhost:8080/user/update with
    ```json
    {
        "user_id":1,
        "fullname":"Romain Mencattini",
        "email":"mrl@bluewin.ch",
        "mobile_phone": "0787498982",
        "firstname": "Romain",
        "skills": [1,2,3]
    }
    ```
    
* POST on http://localhost:8080/skill/update with
    ```json
    {
        "skill_id":1,
        "name":"python"
    }
    ```


* DELETE on http://localhost:8080/user/delete with
  ```json
  {
      "firstname":"Romain"
  }
  ```
  to delete **all** users with firstname matching.


* DELETE on http://localhost:8080/skill/delete with
  ```json
  {
      "users":[1,2]
  }
  ```
  to delete **all** skill which have users 1 and 2.



## TODO

* do autentification and authorisation
* document API on Swagger