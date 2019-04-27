import React, { Component } from 'react';
import TextInput from '../components/TextInput';
import IconButton from '../components/IconButton'
import RequestService from '../js/requests';
import { BASE_SERVER_URL, CREATE_ACCOUNT_URL } from '../constants/urls';
import '../styles/colors.css';


export default class CreateAccountPage extends Component {

    constructor(props) {
        super(props);

        this._onEmailAddressEntered = this._onEmailAddressEntered.bind(this);
        this._onPasswordEntered = this._onPasswordEntered.bind(this);
        this._onSubmitForm = this._onSubmitForm.bind(this);
        this._validateResponse = this._validateResponse.bind(this);

        this._requestService = new RequestService(BASE_SERVER_URL);
        this._emailAddressTextInput = '';
        this._passwordTextInput = '';

        this.state = { errorMessage: null };
    }

    render() {
        return (
            <div>
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
                    variant="primary"
                    fontAwesomeClassName="fas fa-user-plus"
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onSubmitForm}
                >
                    Create
                </IconButton>
            </div>
        )
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

        this._requestService.post(CREATE_ACCOUNT_URL, payload)
            .then(this._validateResponse);
    }

    _validateResponse(payload) {
        if (payload.errorMessage) {
            this.setState({ errorMessage: payload.errorMessage });
        } else {

        }
    }
}