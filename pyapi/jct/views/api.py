from flask import Blueprint, request, url_for, flash, redirect, make_response, abort
import re

from jct.services.algorithm import AlgorithmService
from jct.models.funder import FunderDAO

blueprint = Blueprint('api', __name__)

ISSN_RX = r"^[0-9]{4}-[0-9]{3}[0-9Xx]$"

@blueprint.route('/', methods=['GET'])
def index():
    return make_response("cOAlition S Journal Checker Tool. Service provided by Cottage Labs LLP. Contact us@cottagelabs.com", 200)

@blueprint.route('/calculate', methods=['GET'])
def calculate():
    issn = request.values.get("issn")
    ror = request.values.get("ror")
    funder_id = request.values.get("funder")

    if issn is None:
        abort(400, "ISSN parameter must be supplied in the `issn` url parameter")

    if funder_id is None:
        abort(400, "Funder parameter must be supplied in the `funder` url parameter")

    if re.match(ISSN_RX, issn) is None:
        abort(400, "Supplied ISSN is malformed")

    funder = FunderDAO.get(funder_id)
    if funder is None:
        abort(400, "Supplied funder id is not valid.  Please use a funder ID from https://journalcheckertool.org/funder-ids/")

    svc = AlgorithmService()
    compliance = svc.calculate(issn, funder, ror)

    resp = make_response(compliance.to_json(), 200)
    resp.mimetype = 'application/json'
    return resp

@blueprint.route('/ta', methods=['GET'])
def ta():
    return make_response(200)

@blueprint.route('/ta_search', methods=['GET'])
def ta_search():
    return make_response(200)

@blueprint.route("/tj/<issn>", methods=["GET"])
def tj(issn):
    """
    Get the journal title for the given ISSN
    :param issn: the ISSN of the journal
    :return: a JSON response with the journal title
    """
    return make_response(200)

@blueprint.route("/journal", methods=["GET"])
def journal():
    """
    Get the journal information for the given ISSN
    :return: a JSON response with the journal information
    """
    return make_response(200)

@blueprint.route("/institution/<institution_id>", methods=["GET"])
def institution(institution_id):
    """
    Get the institution information for the given institution ID
    :param institution_id: the ID of the institution
    :return: a JSON response with the institution information
    """
    return make_response(200)

@blueprint.route("/funder", methods=["GET"])
@blueprint.route("/funder/<funder_id>", methods=["GET"])
@blueprint.route("/funder_config", methods=["GET"])
@blueprint.route("/funder_config/<funder_id>", methods=["GET"])
def funder(funder_id=None):
    """
    Get the funder information for the given funder ID
    :param funder_id: the ID of the funder
    :return: a JSON response with the funder information
    """
    return make_response(200)

@blueprint.route("/funder_language", methods=["GET"])
@blueprint.route("/funder_language/<funder_id>", methods=["GET"])
@blueprint.route("/funder_language/<funder_id>/<lang>", methods=["GET"])
def funder_language(funder_id=None, lang=None):
    """
    Get the funder language information for the given funder ID and language
    :param funder_id: the ID of the funder
    :param lang: the language code
    :return: a JSON response with the funder language information
    """
    return make_response(200)