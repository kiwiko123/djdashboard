import React, { Component } from 'react';
import RequestService from '../../common/js/requests';
import { NEW_GAME_URL } from '../js/urls';


export default class ScrabblePlayPage extends Component {

    constructor(props) {
        super(props);

        this._onNewGame = this._onNewGame.bind(this);

        this._requestService = new RequestService('http://localhost:8000');

        this._requestService
            .get(NEW_GAME_URL)
            .then(this._onNewGame)
    }

    render() {
        return (
            <div className="ScrabbleGame">
                <span>test</span>
            </div>
        );
    }

    _onNewGame(response) {
        console.log(response.message);
    }
}