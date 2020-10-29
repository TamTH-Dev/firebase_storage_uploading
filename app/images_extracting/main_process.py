import cv2
import os
import pyrebase

config = {
    'apiKey': 'AIzaSyBQLYTo-G-pdn-JZsyAiNKj-Z9n-JB-V0A',
    'authDomain': 'fir-storageuploading-6eaa6.firebaseapp.com',
    'databaseURL': 'https://fir-storageuploading-6eaa6.firebaseio.com',
    'projectId': 'fir-storageuploading-6eaa6',
    'storageBucket': 'fir-storageuploading-6eaa6.appspot.com',
    'messagingSenderId': '251436968164',
    'appId': '1:251436968164:web:cefc6c1cda08b19f26e4f1',
    'measurementId': 'G-THNW6XRKH3'
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def process_video(video_name, bytes_str):
    image_frames = cv2.VideoCapture(
        get_video_from_bytes_str(video_name, bytes_str))

    frames_total = int(image_frames.get(cv2.CAP_PROP_FRAME_COUNT))

    try:
        if not os.path.exists('./app/images_extracting/data'):
            os.makedirs('./app/images_extracting/data')
    except OSError:
        print('Error: Creating directory of data')

    current_frame = 0

    while(True):
        isSuccess, frame = image_frames.read()

        if isSuccess:
            if current_frame == frames_total - 1:
                imgPath = './app/images_extracting/data/frame' + \
                    str(current_frame) + '.png'
                cv2.imwrite(imgPath, frame)
                storage.child(
                    f'images/{get_video_name_without_extensions(video_name)}.png').put(imgPath)
            current_frame += 1
        else:
            break

    image_frames.release()
    cv2.destroyAllWindows()


def get_video_from_bytes_str(video_name, bytes_str):
    try:
        if not os.path.exists('./app/images_extracting/videos'):
            os.makedirs('./app/images_extracting/videos')
    except OSError:
        print('Error: Creating directory of data')

    try:
        output_file = f'./app/images_extracting/videos/{video_name}'
        if os.path.isfile(output_file):
            os.remove(output_file)

        out_file = open(output_file, "wb")
        out_file.write(bytes_str)
        out_file.close()
    except Exception as error:
        print(error)

    return output_file


def get_video_name_without_extensions(video_name):
    return video_name.split('.')[0]
