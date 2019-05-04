import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { get } from 'lodash';
import HeaderControls from '../components/HeaderControls';
import StorageHelper from '../js/StorageHelper';
import RequestService from '../js/RequestService';
import { CURRENT_USER_DATA_KEY, STORAGE_MODE_SESSION } from '../constants/storage';
import { BASE_SERVER_URL, LOGOUT_URL } from '../constants/urls';

import '../styles/colors.css';
import '../styles/common.css';
import '../styles/AccountHeaderControls.css';


export default class AccountHeaderControls extends PureComponent {

    static propTypes = {
        history: PropTypes.object,
    };

    constructor(props) {
        super(props);

        this._onClickLogin = this._onClickLogin.bind(this);
        this._onClickLogOut = this._onClickLogOut.bind(this);
        this._onLogOut = this._onLogOut.bind(this);

        this._requestService = new RequestService(BASE_SERVER_URL);
        this.state = {
            currentUserData: StorageHelper.getItem(STORAGE_MODE_SESSION, CURRENT_USER_DATA_KEY),
        };
    }

    render() {
        const options = this._getControlOptions();
        return (
            <HeaderControls
                className="controls-header"
                controls={options}
            />
        );
    }

    _getControlOptions() {
        const { currentUserData } = this.state;
        const currentUserGreetingName = currentUserData && (currentUserData.firstName || currentUserData.emailAddress);
        const greetingOption = currentUserGreetingName && {
            text: `Hello, ${currentUserGreetingName}`,
            className: 'control-individual color-gray-light',
        };

        const logInOption = !currentUserData && {
            text: 'Log In',
            onClick: this._onClickLogin,
            className: 'control-individual color-white',
        };

        const logOutOption = currentUserData && {
            text: 'Log Out',
            onClick: this._onClickLogOut,
            className: 'control-individual color-white',
        };

        return [
            greetingOption,
            logInOption,
            logOutOption,
        ];
    }

    _onClickLogin() {
        this.props.history.push('/login');
    }

    _onClickLogOut() {
        const currentUserEmail = get(this.state.currentUserData, 'emailAddress');
        if (!currentUserEmail) {
            return;
        }

        const payload = { emailAddress: currentUserEmail };
        this._requestService
            .post(LOGOUT_URL, payload)
            .then(this._onLogOut);
    }

    _onLogOut() {
        this.setState({ currentUserData: null });
        StorageHelper.clear(STORAGE_MODE_SESSION);
    }
}