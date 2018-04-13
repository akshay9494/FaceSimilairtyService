from flask_restplus import Api
from .face_similarity import api as ns1


api = Api(
    title='Match similarity of faces between two images',
    version='1.0'
    # All API metadatas
)

api.add_namespace(ns1)