from flask_restplus import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
import os
import logging
import face_recognition
import numpy as np
import json
from configurations import Configurations


api = Namespace('face_comparer', description='Matches the similairty between two faces')

file_upload = reqparse.RequestParser()
file_upload.add_argument('first_image',
                         type=FileStorage,
                         location='files',
                         required=True,
                         help='Image file 1')

file_upload.add_argument('second_image',
                         type=FileStorage,
                         location='files',
                         required=True,
                         help='Image file 2')


face_comparision_reponse = api.model('Face Comparision Response', {
    'similarity': fields.Float(description='The similarity between the faces in the two images. '
                                           '1 represents exactly similar and 0 represents not similar at all.')
})


@api.route('/compare_faces')
class FaceComparer(Resource):
    @api.doc('compares faces')
    @api.expect(file_upload)
    @api.marshal_with(face_comparision_reponse, code=200)
    def post(self):
        """SComparing similairty of faces in two different images."""
        logging.info('Received post message.')

        args = file_upload.parse_args()
        # print(args)

        if 'image' not in args['first_image'].content_type:
            logging.error('First file is not an image')
            return api.abort(400, 'Expecting only image files. First File is not an image.')
        if 'image' not in args['second_image'].content_type:
            logging.error('Second file is not an image')
            return api.abort(400, 'Expecting only image files. Second file is not an image.')

        filename1 = os.path.join(Configurations().image_upload_folder, args['first_image'].filename)
        filename2 = os.path.join(Configurations().image_upload_folder, args['second_image'].filename)

        logging.info('Saving image files.')
        args['first_image'].save(filename1)
        logging.info('Saved {}'.format(filename1))
        args['second_image'].save(filename2)
        logging.info('Saved {}'.format(filename2))

        logging.info('Loading image files.')
        first_image = face_recognition.load_image_file(filename1)
        logging.info('Loaded first image.')
        second_image = face_recognition.load_image_file(filename2)
        logging.info('Loaded second image.')

        # dets = detector(first_image, 1)
        logging.info('Finding Facial encodings')
        first_image_encoding = face_recognition.face_encodings(first_image)
        second_image_encoding = face_recognition.face_encodings(second_image)

        if len(first_image_encoding) == 0:
            logging.error('Unable to detect face in the first image')
            api.abort(500, 'Unable to detect face in the first image')

        if len(second_image_encoding) == 0:
            logging.error('Unable to detect face in the second image')
            api.abort(500, 'Unable to detect face in the second image')
        # comparision_result = face_recognition.compare_faces([first_image_encoding], second_image_encoding)
        logging.info('Finding distance between faces.')
        face_distance = np.linalg.norm(first_image_encoding[0] - second_image_encoding[0])
        logging.info('Face distance found as {}'.format(face_distance))

        return {'similarity': 1-face_distance}, 201

