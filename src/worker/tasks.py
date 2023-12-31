import time
import logging
import requests

from db import client as mongo_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('background_tasks')


# TODO: source from env
API_HOST = 'https://application-kfofpusgoa-uc.a.run.app'


def publish_scheduled_posts(caller: str = 'N/A') -> None:
    """
    1. query posts
        - publish_at_ts <= current_ts
        - is_published == False
    2. update each post `is_published` field
        - is_published = True

    :param caller: name of the entity who called the function
    """

    logger.info(f'"{caller}" invoked "publish_scheduled_posts" task')

    time.sleep(5)

    database = mongo_client.get_database('blog')
    collection = database.get_collection('post')

    posts_to_be_published = collection.find({
        'is_published': False,
        'publish_at_ts': {'$lte': time.time()}
    })

    for post in posts_to_be_published:
        post_id = post.get('_id')

        try:
            response = requests.put(
                url=f'{API_HOST}/api/posts/{post_id}',
                json={
                    'title': 'My first post title',
                    'content': 'Lorem Ipsum is simply dummy text',
                    'publish_at_ts': 0,
                    'is_published': True
                }
            )
            response.raise_for_status()
            logger.info(f'post w/ id "{str(post_id)}" is published')
        except Exception:
            logger.error('post update API failed')

    logger.info('"publish_scheduled_posts" task finished execution')
