import React from 'react';
import { get } from 'lodash';

import PlayerHeader from './PlayerHeader';
import TableSide from './TableSide';
import IconButton from './IconButton';
import RequestService from '../js/requests';

import '../styles/common.css';
import '../styles/PazaakGame.css';


class PazaakGame extends React.Component {
    static PLAYER = 'player';
    static OPPONENT = 'opponent';

    constructor(props) {
        super(props);

        this._onClickEndTurn = this._onClickEndTurn.bind(this);
        this._onClickStand = this._onClickStand.bind(this);
        this._onReceiveEndTurnResponse = this._onReceiveEndTurnResponse.bind(this);
        this._onEndTurnHandler = this._onEndTurnHandler.bind(this);
        this._onStartOver = this._onStartOver.bind(this);
        this._newGame = this._newGame.bind(this);

        this.state = this._getInitialState();
        this._requestService = new RequestService('http://localhost:8000');
    }

    render() {
        const scoreRow = this._getScoreRow();
        const table = this._getTable();
        const actionButtons = this._getActionButtons();

        return (
            <div className="PazaakGame">
                {scoreRow}
                {table}
                {actionButtons}
            </div>
        );
    }

    _getPlayerHeader(player) {
        const hasCurrentTurn = this.state.turn === player;
        let score = 0;
        let isPlayer = false;

        switch (player) {
            case PazaakGame.PLAYER:
                score = this.state.player.score;
                isPlayer = true;
                break;
            case PazaakGame.OPPONENT:
                score = this.state.opponent.score;
                break;
            default:
                console.error('invalid argument passed to PazaakGame._getPlayerHeader');
        }

        return (
            <PlayerHeader
                text={score}
                isPlayer={isPlayer}
                hasCurrentTurn={hasCurrentTurn}
            />
        );
    }

    _getScoreRow() {
        const gameOverBanner = this._getGameOverBanner();
        const playerScore = this._getPlayerHeader(PazaakGame.PLAYER);
        const opponentScore = this._getPlayerHeader(PazaakGame.OPPONENT);

        return (
            <div className="row">
                {gameOverBanner}
                {playerScore}
                {opponentScore}
            </div>
        );
    }

    _getGameOverBanner() {
        return this.state.gameOver.value && (
            <span>
                {this.state.gameOver.message}
            </span>
        );
    }

    _getTable() {
        const playerPlaced = get(this.state, 'player.placed');
        const opponentPlaced = get(this.state, 'opponent.placed');
        const playerHand = get(this.state, 'player.hand');
        const opponentHand = get(this.state, 'opponent.hand');

        return (
            <div className="row">
                <TableSide
                    isPlayer={true}
                    placedCards={playerPlaced}
                    handCards={playerHand}
                    showHandCards={true}
                />
                <TableSide
                    isPlayer={false}
                    placedCards={opponentPlaced}
                    handCards={opponentHand}
                    showHandCards={false}
                />
            </div>
        );
    }

    _getActionButtons() {
        const disableActionButtons = this.state.disableActionButtons || this.state.gameOver.value;
        return (
            <div className="row horizontal-row full-width">
                <IconButton
                    variant="success"
                    fontAwesomeClassName="fas fa-play"
                    disabled={disableActionButtons}
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onClickEndTurn}
                >
                    End Turn
                </IconButton>

                <IconButton
                    variant="warning"
                    fontAwesomeClassName="fas fa-arrow-up"
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    disabled={disableActionButtons}
                    onClick={this._onClickStand}
                >
                    Stand
                </IconButton>

                <IconButton
                    variant="danger"
                    fontAwesomeClassName="fas fa-redo"
                    // disabled={this.state.isNewGame}
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onStartOver}
                >
                    Start Over
                </IconButton>
            </div>
        );
    }

    /**
     * POSTs to the end-turn API endpoint.
     *
     * @param player one of {PazaakGame.PLAYER, PazaakGame.OPPONENT}.
     * @private
     */
    _getNextMove(player) {
        const url = '/pazaak/api/end-turn';
        const payload = {
            action: `end-turn-${player}`,
            turn: player,
            gameId: this.state.gameId,
        };

        this._requestService.post(url, payload)
            .then(this._onEndTurnHandler);
    }

    /**
     * Helper method that binds to the "End Turn" button.
     * @private
     */
    _onClickEndTurn() {
        this._getNextMove(PazaakGame.PLAYER)
    }

    _onEndTurnHandler(payload) {
        setTimeout(() => this._onReceiveEndTurnResponse(payload), 1 * 750);
    }

    _onReceiveEndTurnResponse(payload) {
        // shape: {name: string, value: number}
        const status = payload.status;
        const gameOver = this._handleWinner(status);

        // TODO if status is something other than GAME_ON

        const playerToUpdate = payload.turn.justWent.value;
        const playerUpNext = payload.turn.upNext.value;
        const isPlayerStanding = (playerToUpdate === PazaakGame.PLAYER && payload.isStanding) || this.state.player.isStanding;

        // // response.move is 0 when the player is standing (PazaakCard.empty())
        // if (isStanding && !payload.move) {
        //     // hacky way to not update the player's side if they're standing
        //     payload.move = null;
        // }

        const shouldWaitForUserInput = playerUpNext === PazaakGame.PLAYER && !isPlayerStanding;

        const updatedState = this._getEndTurnUpdatedState(payload, playerToUpdate);
        this.setState({
            ...updatedState,
            turn: playerUpNext,
            disableActionButtons: !shouldWaitForUserInput,
            isNewGame: false,
        });

        if (!shouldWaitForUserInput && !gameOver) {
            this._getNextMove(playerUpNext);
        }
    }

    _getEndTurnUpdatedState(payload, player) {
        const playerData = {
            score: payload.score,
            placed: payload.placed.map(card => card.parity),
            isStanding: payload.isStanding,
        };
        let state = {};

        switch (player) {
            case PazaakGame.PLAYER:
                state = { player: playerData };
                break;
            case PazaakGame.OPPONENT:
                state = { opponent: playerData };
                break;
            default:
                console.error('invalid player argument passed to _getEndTurnUpdatedState');
        }

        return state;
    }

    _getInitialState() {
        return {
            player: {
                score: 0,
                isStanding: false,
                placed: [],
                hand: [],
            },
            opponent: {
                score: 0,
                isStanding: false,
                placed: [],
                hand: [],
            },
            turn: PazaakGame.PLAYER,
            disableActionButtons: false,
            isNewGame: true,
            gameOver: {
                value: false,
            },
        };
    }

    _onStartOver() {
        const url = '/pazaak/api/new-game';
        this._requestService.get(url)
            .then(this._newGame);
    }

    _newGame() {
        const state = this._getInitialState();
        this.setState(state);
    }

    _onClickStand() {
        this._onStand(PazaakGame.PLAYER);
    }

    _onStand(player) {
        const url = '/pazaak/api/stand';
        const payload = { action: `stand-${player}` };
        this._requestService.post(url, payload)
            .then(this._onReceiveEndTurnResponse);
    }

    _handleWinner(status) {
        let gameOver = true;
        let message;
        switch (status.value) {
            case 0:
                // player wins
                message = 'Player Wins!';
                break;
            case 1:
                // opponent wins
                message = 'Opponent Wins!';
                break;
            case 2:
                // tie
                message = 'Tie!';
                break;
            case 3:
                // continue
                gameOver = false;
                break;
            case 4:
                // player forfeit
                break;
            default:
                console.error(`unexpected GameStatus enum value "${status.value}" received`);
        }

        this.setState({
            gameOver: {
                value: gameOver,
                message: message,
            },
        });

        return gameOver;
    }
}

PazaakGame.propTypes = {};
export default PazaakGame;