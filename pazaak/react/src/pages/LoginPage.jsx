import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';
import TextInput from '../components/TextInput';
import IconButton from '../components/IconButton'
import RequestService from '../js/RequestService';
import StorageHelper from '../js/StorageHelper';

import { BASE_SERVER_URL, LOGIN_URL } from '../constants/urls';
import { CURRENT_USER_DATA_KEY, STORAGE_MODE_SESSION } from '../constants/storage';

import '../styles/common.css';
import '../styles/colors.css';
import '../styles/LoginPage.css';


export default class LoginPage extends PureComponent {

    constructor(props) {
        super(props);

        this._onEmailAddressEntered = this._onEmailAddressEntered.bind(this);
        this._onPasswordEntered = this._onPasswordEntered.bind(this);
        this._onSubmitForm = this._onSubmitForm.bind(this);
        this._validateResponse = this._validateResponse.bind(this);

        this._requestService = new RequestService(BASE_SERVER_URL);

        this.state = {
            emailAddressTextInput: '',
            passwordTextInput: '',
        };
    }

    render() {
        const noAccountText = 'Don\'t have an account yet? ';
        const errorMessageElement = this._getErrorMessageElement();
        const submitButtonDisabled = !(this.state.emailAddressTextInput && this.state.passwordTextInput);

        return (
            <div className="LoginPage">
                {errorMessageElement}
                <TextInput
                    label="Email Address"
                    labelClassName="color-white"
                    maskInput={false}
                    onTextEntered={this._onEmailAddressEntered}
                    inputValidator={this._textInputValidator}
                />
                <TextInput
                    label="Password"
                    labelClassName="color-white"
                    maskInput={true}
                    onTextEntered={this._onPasswordEntered}
                    inputValidator={this._textInputValidator}
                />
                <IconButton
                    className="submit-button"
                    variant="success"
                    fontAwesomeClassName="fas fa-sign-in-alt"
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onSubmitForm}
                    disabled={submitButtonDisabled}
                >
                    Go
                </IconButton>
                <span className="color-gray-light display-block">
                    {noAccountText}
                    <Link to="/create-account">
                        Make one!
                    </Link>
                </span>
            </div>
        )
    }

    _getErrorMessageElement() {
        return this.state.errorMessage && (
            <span className="color-red">
                {this.state.errorMessage}
            </span>
        );
    }

    _onEmailAddressEntered(text) {
        this.setState({ emailAddressTextInput: text });
    }

    _onPasswordEntered(text) {
        this.setState({ passwordTextInput: text });
    }

    _onSubmitForm() {
        const payload = {
            emailAddress: this.state.emailAddressTextInput,
            password: this.state.passwordTextInput,
            firstName: this._firstNameInput,
        };

        this.setState({ passwordTextInput: '' });
        this._requestService.post(LOGIN_URL, payload)
            .then(this._validateResponse);
    }

    _textInputValidator(text) {
        return text && text.length > 0;
    }

    _validateResponse(payload) {
        if (payload.errorMessage) {
            this.setState({ errorMessage: payload.errorMessage });
        } else {
            // if successfully authenticated, redirect to the "play" page
            const userData = {
                emailAddress: payload.emailAddress,
                firstName: payload.firstName,
                lastName: payload.lastName,
            };
            this._setUserInSession(userData);
            this.props.history.push('/play');
        }
    }

    _setUserInSession(userData) {
        StorageHelper.setItem(STORAGE_MODE_SESSION, CURRENT_USER_DATA_KEY, userData);
    }
}