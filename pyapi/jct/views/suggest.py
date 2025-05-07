from flask import Blueprint, request, url_for, flash, redirect, make_response

blueprint = Blueprint('suggest', __name__)

@blueprint.route('/<type>', methods=['GET'])
@blueprint.route('/<type>/<query>', methods=['GET'])
def suggest(type, query=None):
    """
    Suggest a list of items based on the type and query
    :param type: the type of suggestion to make
    :param query: the query string to use for the suggestion
    :return: a JSON response with the suggestions
    """
    pass