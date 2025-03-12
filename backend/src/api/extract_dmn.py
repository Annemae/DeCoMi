import os
from flask import request
from flask_restful import Resource

SAVE_FOLDER = os.path.abspath('api\\saved_files')

# Extracts a DMN model from a provided file. # TODO - Add error handling.
class ExtractDMN(Resource):
    def post(self):
        file = request.files['file']

        # Saves provided file.
        if file.filename.endswith('.java'):
            file.save(f'{SAVE_FOLDER}\\{file.filename}')
        
        # Deletes file after extracting DMN model.
        os.remove(f'{SAVE_FOLDER}\\{file.filename}')