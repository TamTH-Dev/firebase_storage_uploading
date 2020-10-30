import cv2
from flask import request, jsonify
from app import app
from .images_extracting import process_video
from redis import Redis
from rq import Queue, Retry


q = Queue(connection=Redis(host='0.0.0.0', port=6380))


@app.route('/upload-video', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        if request.files['video']:
            video = request.files['video']
            # Push process into queue
            job = q.enqueue(process_video, video.filename,
                            video.read(), retry=Retry(max=5))  # Retry 5 times until removed from queue

    return jsonify({'message': 'Video is uploaded successfully!'})
