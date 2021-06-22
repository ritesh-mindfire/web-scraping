import os, sys
import boto3
import requests
import logging

from botocore.exceptions import ClientError
from pathlib import Path
from urllib.request import urlopen

from time import time
from queue import Queue
from threading import Thread

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.conf import settings

DEBUG = settings.DEBUG
AWS_KEY = settings.AWS_ACCESS_KEY_ID
AWS_SECRET = settings.AWS_SECRET_ACCESS_KEY 
AWS_REGION_NAME = settings.AWS_S3_REGION_NAME
AWS_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME


def s3_upload_file_link(link):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """

    # S3 object_name was not specified, use file_name
    file_name = os.path.basename(link)
    object_name = os.path.join('media', 'products', file_name)

    # Upload the file
    s3_client = boto3.client("s3", region_name=AWS_REGION_NAME,
                          aws_access_key_id=AWS_KEY,
                          aws_secret_access_key=AWS_SECRET)


    print('Upload start at %s' % object_name)
    try:
        res = requests.get(link, stream=True)
        s3_client.upload_fileobj(res.raw, AWS_BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        print('Upload failed %s: %s' % (object_name, e))
        return False
    print('Uploaded %s' % object_name)
    return True


def download_link(directory, link):
    download_path = os.path.join(directory, os.path.basename(link))
    print('Download start at %s' % download_path)
    with urlopen(link) as image, open(download_path, 'wb') as f:
        f.write(image.read())
    print('Downloaded %s' % link)


def setup_download_dir(dirname):
    download_dir = Path(dirname)
    if not download_dir.exists():
        download_dir.mkdir()
    print('Download directory %s' % download_dir)
    return download_dir


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            func, *args = self.queue.get()
            try:
                func(*args)
            finally:
                self.queue.task_done()


def main(download_dir, links):
    ts = time()

    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for _ in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    for link in links:
        print('Queueing {}'.format(link))
        if DEBUG:
            queue.put((download_link, download_dir, link))
        else:
            queue.put((s3_upload_file_link, link))
    # Causes the main thread to wait for the queue to finish processing all the tasks

    queue.join()
    print('Took %s' % (time() - ts))


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dirname = os.path.join(project_root, 'media')
    download_dir = setup_download_dir(dirname)

    links = [
        'https://images-eu.ssl-images-amazon.com/images/I/81l8KHc7%2BtL._AC_UL200_SR200,200_.jpg',
        # 'https://images-eu.ssl-images-amazon.com/images/I/81s6DUyQCZL._AC_UL200_SR200,200_.jpg',
        # 'https://images-eu.ssl-images-amazon.com/images/I/81NYuWzsJcS._AC_UL200_SR200,200_.jpg',
    ]
    main(download_dir, links)
