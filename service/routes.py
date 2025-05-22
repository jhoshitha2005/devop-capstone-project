from flask import Flask, jsonify, request, abort
from service.models import Account
from http import HTTPStatus as status

app = Flask(__name__)

BASE_URL = "/accounts"

######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route(BASE_URL, methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will list all Accounts
    """
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]

    app.logger.info("Returning [%s] accounts", len(account_list))
    return jsonify(account_list), status.OK


######################################################################
# READ AN ACCOUNT
######################################################################
@app.route(f"{BASE_URL}/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """
    Reads an Account
    This endpoint will read an Account based on the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    return account.serialize(), status.OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route(f"{BASE_URL}/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Update an Account
    This endpoint will update an Account based on the posted data
    """
    app.logger.info("Request to update an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    account.deserialize(request.get_json())
    account.update()

    return account.serialize(), status.OK


######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route(f"{BASE_URL}/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Delete an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    account.delete()
    return "", status.NO_CONTENT


######################################################################
# METHOD NOT ALLOWED HANDLER for /accounts route (e.g. DELETE on /accounts)
######################################################################
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), status.METHOD_NOT_ALLOWED
