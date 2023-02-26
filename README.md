# imagesAPI

### About images API
ImagesAPI is a RESTful API that allows users to upload and manage their images. The API offers three built-in account tiers: Basic, Premium, and Enterprise, each with varying features and benefits. In addition, admins can create arbitrary tiers with customizable thumbnail sizes and the presence of links to the originally uploaded file and the ability to generate expiring links.

### quick note about my choices
* I decided to resize images on go, because resizing images is not very computationally intensive. I also used PilImage.NEAREST - the quickest PIL resizing algorithm (drawback - returns worse quality images) - i'm assuming, that thumbnail will just be a preview for original image.
* in production I'd use some form of caching (either using caching service e.g Cloudflare, or use own caching backend), to cache most-accessed images (depends on client target)
* in production I'd store images at cloud object storage e.g Amazon S3 or self-hosted storage
* README was supposed to be short, but that was a perfect opportunity to practice creating docs
* my next task would be to replace the default Django TokenAuthentication with Django REST Knox, because according to DRF documentation, Django REST Knox offers a more secure implementation that allows generating multiple tokens per user, as well as token expiration.
# Running the Project

## Deployment information

### The imagesAPI project is currently deployed (for testing) and can be accessed at the following URL:
https://imagesapi.onrender.com/api/

#### test Enterprise user:
* email: test@test.com
* password: N52f#He!hf2&QG9DTe17ziQYg
### environment variables that need to be set for the project to work properly:

* `SECRET_KEY`: Django secret key
* `DEBUG`: Debug mode flag
* `DB_NAME`: Database name
* `DB_USER`: Database username
* `DB_PASSWORD`: Database password
* `DB_HOST`: Database host
* `DB_PORT`: Database port
* `ALLOWED_HOSTS`: List of allowed hosts

### to run the project cd into project directory and use:

```
docker-compose build
```

```
docker-compose run imagesapi python generate_fixtures.py
```

```
docker-compose up
```

### to run the tests cd into project directory and use:

```
docker-compose run imagesapi python -m coverage run --source='.' manage.py test && python -m coverage html
```

current code coverage: 100%, however tests need to be expanded into more cases, and some repetition of code should be considered whether they should be moved into functions or not.

<br /><br />
# API Endpoints

| Endpoint                                                                                      | Method | Description                               | Payload                                                 | Params                                          |
| --------------------------------------------------------------------------------------------- | ------ | ----------------------------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| [/api/images/](#GET-/api/images/)                                                             | GET    | List available images                     |                                                         | expiration_time:`int`                           |
| [/api/images/\<pk\>/generate_image_variants/](#GET-/api/images/<pk>/generate_image_variants/) | GET    | Get links to images with different sizes. |                                                         |                                                 |
| [/api/images/](#POST-/api/images/)                                                            | POST   | Create a new image.                       | {"name": `file name`, "file": `image file`}             |                                                 |
| [/api/images/](#PUT-/api/images/<pk>/)                                                        | PUT    | Update an existing image.                 | {"id": `id`, "name": `file name`, "file": `image file`} |                                                 |
| [/api/images/](#DELETE-/api/images/<pk>/)                                                     | DELETE | Delete an existing image.                 | {"id": `id`}                                            |                                                 |
| [/api/images/\<pk\>/](#GET-/api/images/<pk>)                                                  | GET    | Show an image file                        |                                                         | height:`int`, expires_at:`int`, signature:`str` |



<br />

## GET /api/images/

This endpoint allows you to list available images, and get urls to these images in available for user formats.

### Request

- Method:  `GET`
- Payload: None
- Params: None

### Response
| Status code | content-type     | response                                                                                |
| ----------- | ---------------- | --------------------------------------------------------------------------------------- |
| 200         | application/json | {"id":`id`, "name":`filename`, "url": `url for image generation`, "created_at": `time`} |
| 400         | application/json | {"code":"400","error":"Bad Request"}                                                    |
| 401         | application/json | {"code":"400","detail": "Authentication credentials were not provided."}                |


## GET /api/images/\<pk\>/generate_image_variants/

This endpoint allows you to retrieve links to image thumbnails, and original image / expiring binary image based on AccountTier.

### Request

- Method:  `GET`
- Payload: None
- Params: expiration_time[optional, int]

### Response
| Status code | content-type     | response                                                                                                                                                                                                                                                                                                                  |
| ----------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200         | application/json | {"thumbnail_urls": `Object with keys representing different image sizes eg.(size_200:url}) and values representing the corresponding thumbnail URL`.,<br> "original_image": `String representing the URL of the original image.`,<br> "expiring_binary_url": `String representing the URL of the expiring binary image.`} |
| 400         | application/json | {"code":"400","error":"Bad Request"}                                                                                                                                                                                                                                                                                      |
| 401         | application/json | {"code":"400","detail": "Authentication credentials were not provided."}                                                                                                                                                                                                                                                  |
| 404         | application/json | {"code":"404","detail":"Not found."}                                                                                                                                                                                                                                                                                      |


## POST /api/images/

This endpoint allows you to upload image.

### Request

- Method:  `POST`
- Payload: {"name": `filename`, "file": `image file`}
- Params: None

### Response
| Status code | content-type     | response                                                                                |
| ----------- | ---------------- | --------------------------------------------------------------------------------------- |
| 201         | application/json | {"id":`id`, "name":`filename`, "url": `url for image generation`, "created_at": `time`} |
| 400         | application/json | {"code":"400","error":"Bad Request"}                                                    |
| 401         | application/json | {"code":"401","detail": "Authentication credentials were not provided."}                |

## PUT /api/images/\<pk\>/

This endpoint allows you to update an image.

### Request

- Method:  `PUT`
- Payload: optional one of: {"name": `filename`, "file": `image file`}
- Params: None

### Response
| Status code | content-type     | response                                                                                |
| ----------- | ---------------- | --------------------------------------------------------------------------------------- |
| 201         | application/json | {"id":`id`, "name":`filename`, "url": `url for image generation`, "created_at": `time`} |
| 400         | application/json | {"code":"400","error":"Bad Request"}                                                    |
| 401         | application/json | {"code":"401","detail": "Authentication credentials were not provided."}                |
| 404         | application/json | {"code":"404","detail":"Not found."}                                                    |

## DELETE /api/images/\<pk\>/

This endpoint allows you to remove uploaded image.

### Request

- Method:  `DELETE`
- Payload: None
- Params: None

### Response
| Status code | content-type     | response                                                                 |
| ----------- | ---------------- | ------------------------------------------------------------------------ |
| 204         | application/json | {"code": "204", "detail": "No Content"}                                  |
| 400         | application/json | {"code":"400","error":"Bad Request"}                                     |
| 401         | application/json | {"code":"401","detail": "Authentication credentials were not provided."} |
| 404         | application/json | {"code":"404","detail":"Not found."}                                     |


## GET /api/images/\<pk\>/

This endpoint allows you to show formatted uploaded image.

### Request

- Method:  `GET`
- Payload: None
- Params: signature, height, expires_at

### Response
| Status code | content-type         | response                                                    |
| ----------- | -------------------- | ----------------------------------------------------------- |
| 200         | image/\<img-format\> | image file                                                  |
| 400         | application/json     | {"error":"Bad Request"}                                     |
| 401         | application/json     | {"detail": "Authentication credentials were not provided."} |
| 410         | application/json     | {"error":"Image expired."}                                  |

