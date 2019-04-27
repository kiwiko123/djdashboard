import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import TextInput from '../components/TextInput';
import IconButton from '../components/IconButton'
import {BASE_SERVER_URL, LOGIN_URL} from '../constants/urls';
import RequestService from '../js/requests';
import '../styles/common.css';
import '../styles/colors.css';
import '../styles/LoginPage.css';


export default class LoginPage extends Component {

    constructor(props) {
        super(props);

        this._onEmailAddressEntered = this._onEmailAddressEntered.bind(this);
        this._onPasswordEntered = this._onPasswordEntered.bind(this);
        this._onSubmitForm = this._onSubmitForm.bind(this);
        this._validateResponse = this._validateResponse.bind(this);

        this._requestService = new RequestService(BASE_SERVER_URL);
        this._emailAddressTextInput = '';
        this._passwordTextInput = '';

        this.state = {
            submitButtonDisabled: false,
        };
    }

    render() {
        const noAccountText = 'Don\'t have an account yet? ';
        const errorMessageElement = this._getErrorMessageElement();

        return (
            <div className="LoginPage">
                {errorMessageElement}
                <TextInput
                    label="Email Address"
                    labelClassName="color-white"
                    maskInput={false}
                    onTextEntered={this._onEmailAddressEntered}
                />
                <TextInput
                    label="Password"
                    labelClassName="color-white"
                    maskInput={true}
                    onTextEntered={this._onPasswordEntered}
                />
                <IconButton
                    className="submit-button"
                    variant="success"
                    fontAwesomeClassName="fas fa-sign-in-alt"
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onSubmitForm}
                    disabled={this.state.submitButtonDisabled}
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

    _onEmailAddressEntered(event) {
        this._emailAddressTextInput = event.target.value;
    }

    _onPasswordEntered(event) {
        this._passwordTextInput = event.target.value;
    }

    _onSubmitForm() {
        const payload = {
            emailAddress: this._emailAddressTextInput,
            password: this._passwordTextInput,
        };

        this._requestService.post(LOGIN_URL, payload)
            .then(this._validateResponse);
    }

    _validateResponse(payload) {
        if (payload.errorMessage) {
            this.setState({
                errorMessage: payload.errorMessage,
                submitButtonDisabled: false,
            });
        } else {
            // if successfully authenticated, redirect to the "play" page
            this.props.history.push('/play');
        }
    }
}