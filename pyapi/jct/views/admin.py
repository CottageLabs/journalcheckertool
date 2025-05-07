from flask import Blueprint, request, url_for, flash, redirect, make_response

blueprint = Blueprint('admin', __name__)

@blueprint.route('/unknown', methods=['GET'])
@blueprint.route('/unknown/<start>/<end>', methods=['GET'])
def unknown(start=None, end=None):
    """
    Get the unknown journals between start and end
    :param start: the start date
    :param end: the end date
    :return: a JSON response with the unknown journals
    """
    return make_response(200)

@blueprint.route("/compliance", methods=["GET"])
def compliance():
    """
    Get the compliance information for the given ISSN
    :return: a JSON response with the compliance information
    """
    return make_response(200)

@blueprint.route("/test", methods=["GET"])
def test():
    """
    Test the API
    :return: a JSON response with the test information
    """
    return make_response(200)

