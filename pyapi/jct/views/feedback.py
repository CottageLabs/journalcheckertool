from flask import Blueprint, request, url_for, flash, redirect, make_response

blueprint = Blueprint('feedback', __name__)

@blueprint.route('/', methods=['GET', "POST"])
def feedback():
    pass