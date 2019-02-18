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
        this._onReceiveEndTurnResponse = this._onReceiveEndTurnResponse.bind(this);
        this._onEndTurnHandler = this._onEndTurnHandler.bind(this);

        this.state = {
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
        };
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
        const playerScore = this._getPlayerHeader(PazaakGame.PLAYER);
        const opponentScore = this._getPlayerHeader(PazaakGame.OPPONENT);

        return (
            <div className="row">
                {playerScore}
                {opponentScore}
            </div>
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
        return (
            <div className="row horizontal-row full-width">
                <IconButton
                    label="End Turn"
                    bsStyle="success"
                    faClassName="fas fa-play"
                    disabled={this.state.disableActionButtons}
                    onClick={this._onClickEndTurn}
                />

                <IconButton
                    label="Stand"
                    bsStyle="warning"
                    faClassName="fas fa-hand-paper"
                    disabled={this.state.disableActionButtons}
                />

                <IconButton
                    label="Start Over"
                    bsStyle="danger"
                    faClassName="fas fa-redo"
                    disabled={this.state.disableActionButtons}
                />
            </div>
        );
    }

    _oppositePlayer(player) {
        let result;
        switch (player) {
            case PazaakGame.PLAYER:
                result = PazaakGame.OPPONENT;
                break;
            case PazaakGame.OPPONENT:
                result = PazaakGame.PLAYER;
                break;
            default:
                console.error('invalid argument passed to _oppositePlayer');
        }
        return result;
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
        };

        RequestService.post(url, payload)
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

        // TODO if status is something other than GAME_ON

        const playerToUpdate = payload.turn.justWent.value;
        const playerUpNext = payload.turn.upNext.value;
        const didPlayerJustGo = playerToUpdate === PazaakGame.PLAYER;
        const isStanding = payload.isStanding;

        // response.move is 0 when the player is standing (PazaakCard.empty())
        if (isStanding && !payload.move) {
            // hacky way to not update the player's side if they're standing
            payload.move = null;
        }

        const updatedState = this._getEndTurnUpdatedState(payload, playerToUpdate);

        // if it's the opponent's turn, get their next move.
        // otherwise, it's the player's turn, so wait for user input
        const shouldSwitchTurn = isStanding || didPlayerJustGo;
        if (shouldSwitchTurn) {
            // in this conditional:
            //   * otherPlayer is always PLAYER
            //   * didPlayerJustGo is always false
            this._getNextMove(playerUpNext);
        }

        this.setState({
            ...updatedState,
            turn: playerUpNext,
            disableActionButtons: shouldSwitchTurn,
        });
    }

    _getEndTurnUpdatedState(payload, player) {
        const cardPlaced = payload.move;
        let state = {};

        switch (player) {
            case PazaakGame.PLAYER:
                state = {
                    player: {
                        score: this.state.player.score + cardPlaced.modifier,
                        placed: [...this.state.player.placed, cardPlaced.parity],
                    },
                };
                break;
            case PazaakGame.OPPONENT:
                state = {
                    opponent: {
                        score: this.state.opponent.score + cardPlaced.modifier,
                        placed: [...this.state.opponent.placed, cardPlaced.parity],
                    },
                };
                break;
            default:
                console.error('invalid player argument passed to _updateSideFor');
        }

        return state;
    }
}

PazaakGame.propTypes = {};
export default PazaakGame;