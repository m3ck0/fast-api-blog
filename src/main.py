from bson import ObjectId
from db import client as mongo_client
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from models import CreatePostRequest, PostResponse
from pymongo.collection import Collection
from rq import Queue
from worker.connection import client as redis_client
from worker.tasks import publish_scheduled_posts as publish_scheduled_posts_task

app = FastAPI()
queue = Queue(connection=redis_client)

database = {}


@app.get('/api/posts')
async def get_posts() -> list[PostResponse]:
    database = mongo_client.get_database('blog')
    collection: Collection = database.get_collection('post')

    # region - convert dict documents to PostResponses (using for in loop)
    # posts = list()

    # for document in collection.find({'is_published': True}):
    #     posts.append(PostResponse(id=document.pop('_id'), **document))
    # endregion

    # region - convert dict documents to PostResponses (using lambda)
    # posts = map(
    #     lambda d: PostResponse(id=d.pop('_id'), **d),
    #     collection.find({'is_published': True})
    # )
    # endregion

    # region - convert dict documents to PostResponses (using list comprehension)  # noqa: E501
    return [
        PostResponse(id=str(document.pop('_id')), **document)
        for document in collection.find({'is_published': True})
    ]
    # endregion


@app.post('/api/posts')
async def create_post(create_post_request: CreatePostRequest) -> PostResponse:
    database = mongo_client.get_database('blog')
    collection: Collection = database.get_collection('post')
    result = collection.insert_one(document=create_post_request.model_dump())
    return PostResponse(id=str(result.inserted_id), **create_post_request.model_dump())


@app.get('/api/posts/{post_id}')
async def get_post(post_id: str) -> PostResponse | None:
    database = mongo_client.get_database('blog')
    collection: Collection = database.get_collection('post')
    document: dict | None = collection.find_one({'_id': ObjectId(post_id)})

    if document is None:
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
async def update_post(post_id: str, update_post_request: CreatePostRequest):
    database = mongo_client.get_database('blog')
    collection: Collection = database.get_collection('post')

    collection.update_one(
        {'_id': ObjectId(post_id)},
        {'$set': {'is_published': update_post_request.is_published}}
    )

    return {}, 200


@app.post('/api/posts/publish')
async def publish_scheduled_posts():
    """
    create task which published publishable posts
    """

    queue.enqueue(f=publish_scheduled_posts_task, caller='FastAPI backend')
    return {}, 202
