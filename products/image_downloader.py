import json
import logging
import os
from pathlib import Path
from urllib.request import urlopen, Request

from time import time
import logging
import os
from queue import Queue
from threading import Thread

logger = logging.getLogger(__name__)


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
            directory, link = self.queue.get()
            try:
                download_link(directory, link)
            finally:
                self.queue.task_done()


def main(download_dir, links):
    ts = time()

    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    for link in links:
        print('Queueing {}'.format(link))
        queue.put((download_dir, link))
    # Causes the main thread to wait for the queue to finish processing all the tasks

    queue.join()
    print('Took %s' % (time() - ts))


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dirname = os.path.join(project_root, 'media')
    download_dir = setup_download_dir(dirname)

    links = [
        'https://images-eu.ssl-images-amazon.com/images/I/81l8KHc7%2BtL._AC_UL200_SR200,200_.jpg',
        'https://images-eu.ssl-images-amazon.com/images/I/81s6DUyQCZL._AC_UL200_SR200,200_.jpg',
        'https://images-eu.ssl-images-amazon.com/images/I/81NYuWzsJcS._AC_UL200_SR200,200_.jpg',
    ]
    main(download_dir, links)
