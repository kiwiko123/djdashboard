import React, { PureComponent } from 'react';
import TextInput from '../components/TextInput';
import IconButton from '../components/IconButton'
import RequestService from '../js/RequestService';
import { BASE_SERVER_URL, CREATE_ACCOUNT_URL } from '../constants/urls';
import '../styles/colors.css';


export default class CreateAccountPage extends PureComponent {

    constructor(props) {
        super(props);

        this._onEmailAddressEntered = this._onEmailAddressEntered.bind(this);
        this._onPasswordEntered = this._onPasswordEntered.bind(this);
        this._onFirstNameEntered = this._onFirstNameEntered.bind(this);
        this._onSubmitForm = this._onSubmitForm.bind(this);
        this._validateResponse = this._validateResponse.bind(this);

        this._requestService = new RequestService(BASE_SERVER_URL);

        this.state = {
            errorMessage: null,
            emailAddressInput: '',
            passwordInput: '',
        };
    }

    render() {
        const submitButtonDisabled = !(this.state.emailAddressInput && this.state.passwordInput);
        return (
            <div>
                <TextInput
                    label="Email Address"
                    labelClassName="color-white"
                    maskInput={false}
                    onTextEntered={this._onEmailAddressEntered}
                    inputValidator={this._textInputValidator}
                    placeholder="required"
                />
                <TextInput
                    label="Password"
                    labelClassName="color-white"
                    maskInput={true}
                    onTextEntered={this._onPasswordEntered}
                    inputValidator={this._textInputValidator}
                    placeholder="required"
                />
                <TextInput
                    label="First Name"
                    labelClassName="color-white"
                    onTextEntered={this._onFirstNameEntered}
                />
                <IconButton
                    variant="primary"
                    fontAwesomeClassName="fas fa-user-plus"
                    disabled={submitButtonDisabled}
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onSubmitForm}
                >
                    Create
                </IconButton>
            </div>
        )
    }

    _onEmailAddressEntered(text) {
        this.setState({ emailAddressInput: text });
    }

    _onPasswordEntered(text) {
        this.setState({ passwordInput: text });
    }

    _onFirstNameEntered(text) {
        this._firstNameInput = text;
    }

    _textInputValidator(text) {
        return text && text.length > 0;
    }

    _onSubmitForm() {
        const payload = {
            emailAddress: this.state.emailAddressInput,
            password: this.state.passwordInput,
            firstName: this._firstNameInput,
        };

        this.setState({ passwordTextInput: null });
        this._requestService.post(CREATE_ACCOUNT_URL, payload)
            .then(this._validateResponse);
    }

    _validateResponse(payload) {
        if (payload.errorMessage) {
            this.setState({ errorMessage: payload.errorMessage });
        } else {
            this.props.history.push('/play');
        }
    }
}