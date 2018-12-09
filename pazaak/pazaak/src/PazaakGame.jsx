import React from 'react';
import { get } from 'lodash';
import Score from './Score';
import TableSide from './TableSide';
import IconButton from './common/IconButton';
import RequestService from './requests';

import './PazaakGame.css';
import './common.css';


class PazaakGame extends React.Component {
    static PLAYER = 'player';
    static OPPONENT = 'opponent';

    constructor(props) {
        super(props);
        this.state = this._setUpState();

        this._onClickEndTurn = this._onClickEndTurn.bind(this);
        this._onReceiveEndTurnResponse = this._onReceiveEndTurnResponse.bind(this);
    }

    componentDidMount() {
        const url = '/pazaak/api/new-game/';
        RequestService.get(url)
            .then(data => this.setState({ ...data }));
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

    _setUpState() {
        return {
            player: {
                score: 0,
                isStanding: false,
            },
            opponent: {
                score: 0,
                isStanding: false,
            },
            turn: PazaakGame.PLAYER,
        };
    }

    _getScore(player) {
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
                console.error('invalid argument passed to PazaakGame._getScore');
        }

        return (
            <Score
                score={score}
                isPlayer={isPlayer}
                hasCurrentTurn={hasCurrentTurn}
            />
        );
    }

    _getScoreRow() {
        const playerScore = this._getScore(PazaakGame.PLAYER);
        const opponentScore = this._getScore(PazaakGame.OPPONENT);

        return (
            <div className="row">
                {playerScore}
                {opponentScore}
            </div>
        );
    }

    _getTable() {
        const playerHand = get(this.state, 'player.hand');

        return (
            <div className="row">
                <TableSide
                    isPlayer={true}
                    placedCards={[]}
                    handCards={playerHand}
                />
                <TableSide
                    isPlayer={false}
                    placedCards={[]}
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
                    onClick={this._onClickEndTurn}
                />

                <IconButton
                    label="Stand"
                    bsStyle="warning"
                    faClassName="fas fa-hand-paper"
                />

                <IconButton
                    label="Start Over"
                    bsStyle="danger"
                    faClassName="fas fa-redo"
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

    _onClickEndTurn() {
        const url = '/pazaak/api/end-turn';
        const payload = {
            action: 'end-turn-player',
            turn: PazaakGame.PLAYER,
            winner: '',
        };

        RequestService.post(url, payload)
            .then(this._onReceiveEndTurnResponse);
    }

    _onReceiveEndTurnResponse(payload) {
        const winner = payload.winner;
        const status = payload.status;

        if (status === 'game-over') {
            // TODO gameOver(winner);
            return;
        }

        let playerToUpdate = payload.turn;
        let otherPlayer = this._oppositePlayer(playerToUpdate);
        const didPlayerJustGo = playerToUpdate === PazaakGame.PLAYER;
        const isStanding = payload.is_standing;

        // response.move is 0 when the player is standing (PazaakCard.empty())
        if (isStanding && !payload.move) {
            // hacky way to not update the player's side if they're standing
            payload.move = null;
        }

        // TODO updateSideFor(playerToUpdate, payload)

        if (winner) {
            // TODO signalGameOver(winner)
        }

        // if it's the opponent's turn, get their next move.
        // otherwise, it's the player's turn, so wait for user input
        if (isStanding || !didPlayerJustGo) {
            // in this conditional:
            //   * otherPlayer is always PLAYER
            //   * playerJustWent is always false

            this.setState({ turn: playerToUpdate });
            // getMove(playerToUpdate, (response) => onEndTurn(response, otherPlayer));
        }
    }
}

PazaakGame.propTypes = {};
export default PazaakGame;