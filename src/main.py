from fastapi import FastAPI
from models import PostResponse, CreatePostRequest
from db import client as mongo_client
from pymongo.collection import Collection
from bson import ObjectId
from fastapi.exceptions import HTTPException


app = FastAPI()
database = {}


@app.get('/api/posts')
async def get_posts() -> list[PostResponse]:
    return database.get('posts', list())


@app.post('/api/posts')
async def create_post(create_post_request: CreatePostRequest) -> PostResponse:
    # NOTE: same as 2 lines below: collection = mongo_client['blog']['post']
    database = mongo_client.get_database('blog')
    collection: Collection = database.get_collection('post')
    result = collection.insert_one(document=create_post_request.model_dump())
    return PostResponse(
        id=str(result.inserted_id),  # ObjectId -> str
        # --- 1
        # title=create_post_request.title,
        # content=create_post_request.content
        # --- 2
        # **{
        #     'title': create_post_request.title,
        #     'content': create_post_request.content
        # }
        # --- 3
        **create_post_request.model_dump()
    )


@app.get('/api/posts/{post_id}')
async def get_post(post_id: str) -> PostResponse | None:
    database = mongo_client.get_database('blog')
    collection: Collection = database.get_collection('post')
    document: dict | None = collection.find_one({'_id': ObjectId(post_id)})

    if document is None:  #NOTE: if not document:
        raise HTTPException(status_code=404)

    return PostResponse(id=str(document.pop('_id')), **document)


@app.delete('/api/posts/{post_id}')
async def delete_post(post_id: int) -> bool:
    posts = database.get('posts', list())
    post_to_delete = None

    for post in posts:
        if post.id == post_id:
            post_to_delete = post
            break

    if post_to_delete is not None:
        posts.remove(post_to_delete)
        return True

    return False


@app.put('/api/posts/{post_id}')
async def update_post(post_id: int, update_post_request: CreatePostRequest) -> PostResponse:
    posts = database.get('posts', list())
    post_to_update_index: int = 0

    for index in range(len(posts)):
        post = posts[index]

        if post.id == post_id:
            post_to_update_index = index
            break

    posts[post_to_update_index] = PostResponse(
        id=post_id,
        title=update_post_request.title,
        content=update_post_request.content
    )

    return posts[post_to_update_index]
