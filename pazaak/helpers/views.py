from . import accounts
from pazaak.enums import AuthenticationContextType
from pazaak import data_access, helpers
from pazaak.utilities.functions import contains_all_keys
from pazaak.server.utilities import ERROR_KEY


def get_login_context(payload: {str: str}) -> {str: str}:
    context = {}

    if contains_all_keys(payload, 'emailAddress', 'password'):
        email_address = payload['emailAddress']
        password = payload['password']
        user = data_access.users.get_by_email(email_address)
        if accounts.are_user_credentials_valid(user, password):
            accounts.authenticate_user(email_address, AuthenticationContextType.LOGIN)
            context['emailAddress'] = email_address
            context['firstName'] = user.first_name
            context['lastName'] = user.last_name
        else:
            context[ERROR_KEY] = 'Invalid credentials. Please try again.'
    else:
        context[ERROR_KEY] = 'missing emailAddress or password from payload'

    return context


def create_account(user_data: {str: str}) -> {str: str}:
    context = {}

    if contains_all_keys(user_data, 'emailAddress', 'password'):
        email_address = user_data['emailAddress']
        password = user_data['password']
        first_name = user_data.get('firstName')
        last_name = user_data.get('lastName')

        if email_address and password:
            helpers.accounts.create_user(email_address, password, first_name=first_name, last_name=last_name)
            context['emailAddress'] = email_address
        else:
            context[ERROR_KEY] = 'blank emailAddress or password'
    else:
        context[ERROR_KEY] = 'missing emailAddress or password from payload'

    return context


if __name__ == '__main__':
    pass