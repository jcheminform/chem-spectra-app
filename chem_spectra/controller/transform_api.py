from flask import (
    Flask, Blueprint, request, jsonify, send_file, abort,
)
from chem_spectra.controller.helper.file_container import FileContainer
from chem_spectra.controller.helper.settings import get_ip_white_list
from chem_spectra.controller.helper.share import (
    allowed_file, to_zip_response, extract_params
)

from chem_spectra.model.transformer import TransformerModel as TraModel


trans_api = Blueprint('transform_api', __name__)


@trans_api.before_app_request
def filter_remote_ip():
    trusted_servers = get_ip_white_list()
    # if request.remote_addr not in trusted_servers:
    #     abort(403)


@trans_api.route('/zip_jcamp_n_img', methods=['POST'])
def zip_jcamp_n_img():
    try:
        file = FileContainer(request.files['file'])
        params = extract_params(request)
        if file: # and allowed_file(file):
            tf_jcamp, tf_img = TraModel(file, params).convert2jcamp_img()
            memory = to_zip_response([tf_jcamp, tf_img])
            return send_file(
                memory,
                attachment_filename='spectrum.zip',
                as_attachment=True
            )
            abort(400)
    except:
        abort(500)


@trans_api.route('/zip_jcamp', methods=['POST'])
def zip_jcamp():
    try:
        file = FileContainer(request.files['file'])
        params = extract_params(request)
        if file: # and allowed_file(file):
            tf_jcamp = TraModel(file, params).convert2jcamp()
            memory = to_zip_response([tf_jcamp])
            return send_file(
                memory,
                attachment_filename='spectrum.zip',
                as_attachment=True
            )
        abort(400)
    except:
        abort(500)


@trans_api.route('/zip_image', methods=['POST'])
def zip_image():
    try:
        file = FileContainer(request.files['file'])
        params = extract_params(request)
        if file: # and allowed_file(file):
            tf_img = TraModel(file, params).convert2img()
            memory = to_zip_response([tf_img])
            return send_file(
                memory,
                attachment_filename='spectrum.zip',
                as_attachment=True
            )
        abort(400)
    except:
        abort(500)


@trans_api.route('/jcamp', methods=['POST'])
def jcamp():
    try:
        file = FileContainer(request.files['file'])
        params = extract_params(request)
        if file: # and allowed_file(file):
            tf_jcamp = TraModel(file, params).convert2jcamp()
            return send_file(
                tf_jcamp,
                attachment_filename='spectrum.jdx',
                as_attachment=True
            )
        abort(400)
    except:
        abort(500)


@trans_api.route('/image', methods=['POST'])
def image():
    try:
        file = FileContainer(request.files['file'])
        params = extract_params(request)
        if file: # and allowed_file(file):
            tf_img = TraModel(file, params).convert2img()
            return send_file(
                tf_img,
                attachment_filename='spectrum.png',
                as_attachment=True,
                mimetype='image/png'
            )
        abort(400)
    except:
        abort(500)
