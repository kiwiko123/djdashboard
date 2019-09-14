import React, { Component } from 'react';
import {
    clone,
    get,
    isEmpty,
} from 'lodash';
import RequestService from '../../common/js/requests';
import { Player } from '../js/enums';
import {
    NEW_GAME_URL,
    VALIDATE_MOVE_URL,
    PLAY_MOVE_URL,
} from '../js/urls';
import {
    createTileInfo,
    getAvailableTiles,
    getFromSubmittedTiles,
} from './util/gameLogic';
import { renderPlayerTiles } from './util/gameUI';

import IconButton from '../../common/components/IconButton';
import ScrabbleBoard from './ScrabbleBoard';
import Cell from './Cell';

import '../../common/styles/positioning.css';
import '../styles/ScrabbleGame.css';


const SERVER_URL = 'http://localhost:8000';


function getDefaultState() {
    return {
        board: [],
        submittedTiles: [],
        canSubmit: false,
    };
}


export default class ScrabbleGame extends Component {

    constructor(props) {
        super(props);

        this._onNewGame = this._onNewGame.bind(this);
        this._updateGameState = this._updateGameState.bind(this);
        this._onDropTileOnBoard = this._onDropTileOnBoard.bind(this);
        this._onPlayerSubmitMove = this._onPlayerSubmitMove.bind(this);
        this._onRecallTiles = this._onRecallTiles.bind(this);
        this._onRecallTile = this._onRecallTile.bind(this);
        this._onValidateMove = this._onValidateMove.bind(this);
        this._transferTileFromBoardToPlayer = this._transferTileFromBoardToPlayer.bind(this);

        this.state = getDefaultState();
        this._requestService = new RequestService(SERVER_URL);
        this._onNewGame();
    }

    render() {
        const availableTiles = getAvailableTiles(this.state.playerTiles, this.state.submittedTiles);
        const playerTilesElement = renderPlayerTiles(availableTiles, false);
        const submitButtonVariant = this.state.canSubmit ? 'success' : 'dark';

        return (
            <Cell
                className="ScrabbleGame"
                onDrop={this._transferTileFromBoardToPlayer}
            >
                <div className="board parent-center">
                    <ScrabbleBoard
                        board={this.state.board}
                        submittedTiles={this.state.submittedTiles}
                        dropTileHandler={this._onDropTileOnBoard}
                        clickTileHandler={this._onRecallTile}
                    />
                </div>
                <hr />
                <div className="player-tiles parent-center">
                    {playerTilesElement}
                </div>
                <div className="buttons parent-center">
                    <IconButton
                        variant={submitButtonVariant}
                        fontAwesomeClassName="fas fa-play"
                        onClick={this._onPlayerSubmitMove}
                        disableOnClick={true}
                        disabled={!this.state.canSubmit}
                    >
                        Submit
                    </IconButton>
                    <IconButton
                        variant="light"
                        fontAwesomeClassName="fas fa-arrow-down"
                        onClick={this._onRecallTiles}
                        disabled={isEmpty(this.state.submittedTiles)}
                    >
                        Recall
                    </IconButton>
                    <IconButton
                        variant="warning"
                        fontAwesomeClassName="fas fa-forward"
                        onClick={() => {}}
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
            </Cell>
        );
    }

    _onNewGame() {
        this._requestService
            .get(NEW_GAME_URL)
            .then(this._updateGameState);

        this.setState({
            canSubmit: false,
        });
    }

    _updateGameState(response) {
        this.setState({
            player: response.player,
            opponent: response.opponent,
            playerTiles: createTileInfo(response.playerTiles),
            opponentTiles: createTileInfo(response.opponentTiles),
            board: response.board,
            submittedTiles: [],
        });

        this._requestService.setPersistentPayload({
            gameId: response.gameId,
        });
    }

    _onDropTileOnBoard(tileIndex, droppedRow, droppedColumn) {
        const submittedTile = {
            index: tileIndex,
            row: droppedRow,
            column: droppedColumn,
        };
        const submittedTiles = [
            ...get(this.state, 'submittedTiles', []),
            submittedTile,
        ];

        const tiles = get(this.state, 'playerTiles', [])
            .map(tile => tile.value);
        const board = [...get(this.state, 'board', [])];

        board[droppedRow][droppedColumn] = tiles[tileIndex];
        tiles.splice(tileIndex, 1);

        const payload = { submittedTiles };
        this._requestService.post(VALIDATE_MOVE_URL, payload)
            .then(this._onValidateMove);

        this.setState({
            submittedTiles,
            board,
        });
    }

    _onPlayerSubmitMove() {
        const payload = {
            player: Player.PLAYER,
            submittedTiles: get(this.state, 'submittedTiles', []),
        };

        this._requestService.post(PLAY_MOVE_URL, payload)
            .then(this._updateGameState);
    }

    _onRecallTiles() {
        const submittedTiles = get(this.state, 'submittedTiles', []);
        const board = [...this.state.board];
        submittedTiles.forEach((tile) => { board[tile.row][tile.column] = null; });

        this.setState({
            board,
            submittedTiles: [],
        });
    }

    _onValidateMove(response) {
        this.setState({ canSubmit: response.is_valid });
    }

    _transferTileFromBoardToPlayer(event) {
        console.log('test');
        event.preventDefault();
        const stringified = event.dataTransfer.getData('text/plain');
        const payload = JSON.parse(stringified);
        if (typeof payload !== 'object') {
            console.error(`Expected JSON-object containing row/column on transfer tile from board to player; received "${payload}"`);
        }
        const { row, column } = payload;
        this._onRecallTile(row, column);
    }

    _onRecallTile(row, column) {
        const clickedTile = getFromSubmittedTiles(row, column, this.state.submittedTiles);
        if (!clickedTile) {
            console.error(`Board at row "${row}", column "${column}" is empty`);
            return;
        }

        const board = clone(this.state.board);
        board[row][column] = null;

        this.setState({
            board,
            submittedTiles: this.state.submittedTiles.filter(tile => tile !== clickedTile),
        });
    }
}