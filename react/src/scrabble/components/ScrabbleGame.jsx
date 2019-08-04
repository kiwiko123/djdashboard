import React, { Component } from 'react';
import { get } from 'lodash';
import RequestService from '../../common/js/requests';
import { Player } from '../js/enums';
import { NEW_GAME_URL, PLAY_MOVE_URL } from '../js/urls';
import { renderPlayerTiles } from './util/gameUI';

import IconButton from '../../common/components/IconButton';
import ScrabbleBoard from './ScrabbleBoard';

import '../../common/styles/positioning.css';
import '../styles/ScrabbleGame.css';


const SERVER_URL = 'http://localhost:8000';


export default class ScrabbleGame extends Component {

    constructor(props) {
        super(props);

        this._onNewGame = this._onNewGame.bind(this);
        this._updateGameState = this._updateGameState.bind(this);
        this._onDropTileOnBoard = this._onDropTileOnBoard.bind(this);
        this._onPlayerSubmitMove = this._onPlayerSubmitMove.bind(this);

        this.state = {};
        this._requestService = new RequestService(SERVER_URL);
        this._onNewGame();
    }

    render() {
        const playerCharacters = get(this.state, 'player.characters', []);
        const playerCharacterElement = renderPlayerTiles(playerCharacters, false);

        return (
            <div className="ScrabbleGame">
                <div className="board parent-center">
                    <ScrabbleBoard
                        board={this.state.board}
                        dropTileHandler={this._onDropTileOnBoard}
                    />
                </div>
                <hr />
                <div className="player-characters parent-center">
                    {playerCharacterElement}
                </div>
                <div className="buttons parent-center">
                    <IconButton
                        variant="success"
                        fontAwesomeClassName="fas fa-play"
                        onClick={this._onPlayerSubmitMove}
                        disableOnClick={true}
                    >
                        Submit
                    </IconButton>
                    <IconButton
                        variant="secondary"
                        fontAwesomeClassName="fas fa-arrow-down"
                        onClick={() => {}}
                    >
                        Reset
                    </IconButton>
                    <IconButton
                        variant="warning"
                        fontAwesomeClassName="fas fa-forward"
                        onClick={() => {}}
                        disableOnClick={true}
                    >
                        Pass
                    </IconButton>
                    <IconButton
                        variant="danger"
                        fontAwesomeClassName="fas fa-redo"
                        onClick={this._onNewGame}
                    >
                        Start Over
                    </IconButton>
                </div>
            </div>
        );
    }

    _onNewGame() {
        this._requestService
            .get(NEW_GAME_URL)
            .then(this._updateGameState);
    }

    _updateGameState(response) {
        this.setState({
            player: response.player,
            opponent: response.opponent,
            board: response.board,
            submittedTiles: [],
        });

        this._requestService.setPersistentPayload({
            gameId: response.gameId,
        });
    }

    _onDropTileOnBoard(tileIndex, droppedRow, droppedColumn) {
        const submittedTiles = get(this.state, 'submittedTiles', []);
        submittedTiles.push({
            tileIndex,
            row: droppedRow,
            column: droppedColumn,
        });

        const tiles = get(this.state, 'player.characters', []);
        const board = get(this.state, 'board', []);
        board[droppedRow][droppedColumn] = tiles[tileIndex];
        tiles.splice(tileIndex, 1); // modifies in-place; also updates this.state.player.characters

        this.setState({
            submittedTiles,
            board,
        });
    }

    _onPlayerSubmitMove() {
        const payload = {
            player: Player.PLAYER,
            submittedTiles: this.state.submittedTiles,
        };

        this._requestService.post(PLAY_MOVE_URL, payload)
            .then(this._updateGameState);
    }
}