## Steps to Setup :

**Step 1**: *Clone the Project Repository*
git clone <repository_url>
cd <project_directory>

**Step 2**: *Create and Activate a Virtual Environment*
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`

**Step 3**: *Install Dependencies*
pip install -r requirements.txt

**Step 4**: *Apply Database Migrations*
python manage.py makemigrations
python manage.py migrate

**Step 5**: *Create a Superuser (Optional)*
python manage.py createsuperuser

**Step 6**: *Run the Development Server*
python manage.py runserver



## APIs Curl Commands

**1. Register User**
Endpoint: POST /register/

curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassword"}'

  
**2. List Movies**
Endpoint: GET /movies/

curl -X GET http://localhost:8000/api/movies/ \
-H "Authorization: Bearer <access_token>"


**3. List Collections**
Endpoint: GET /collection/

curl -X GET http://localhost:8000/api/collection/ \
-H "Authorization: Bearer <access_token>"


**4. Create Collection**
Endpoint: POST /collection/

curl -X POST http://localhost:8000/collection/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"title": "<Title  of  the  collection>",
"description": "<Description  of  the  collection>",
"movies": [
{
"title": "<title  of  the  movie>",
"description": "<description  of  the  movie>",
"genres": "<genres>",
"uuid": "<uuid>"
}
]
}'


**5. Update Collection**
Endpoint: PUT /collection/<collection_uuid>/

curl -X PUT http://localhost:8000/collection/<collection_uuid>/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{
"title": "<Optional  updated  title>",
"description": "<Optional  updated  description>",
"movies": <Optional  updated  movie  list>
}'


**6. Delete Collection*
Endpoint: DELETE /collection/<collection_uuid>/

curl -X DELETE http://localhost:8000/collection/<collection_uuid>/ \
-H "Authorization: Bearer <access_token>"
  

**7. Get Request Count**
Endpoint: GET /request-count/
  
curl -X GET http://localhost:8000/request-count/ \
-H "Authorization: Bearer <access_token>"


**8. Reset Request Count**
Endpoint: POST /request-count/reset/

curl -X POST http://localhost:8000/request-count/reset/ \
-H "Authorization: Bearer <access_token>"


## Postman API Collection:
To execute the API Import onefin.postman_collection.json in Postman.