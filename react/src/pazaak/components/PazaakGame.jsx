import React, { Component } from 'react';
import { get } from 'lodash';

import PlayerHeader from './PlayerHeader';
import TableSide from './TableSide';
import ActionIcon from './ActionIcon';
import IconButton from '../../common/components/IconButton';
import RequestService from '../../common/js/requests';

import { Action, GameStatus, Player, Theme } from '../js/enums';

import '../styles/common.css';
import '../styles/colors.css';
import '../styles/PazaakGame.css';


class PazaakGame extends Component {

    constructor(props) {
        super(props);

        this._onClickEndTurn = this._onClickEndTurn.bind(this);
        this._onClickStand = this._onClickStand.bind(this);
        this._onClickHandCard = this._onClickHandCard.bind(this);
        this._onReceiveEndTurnResponse = this._onReceiveEndTurnResponse.bind(this);
        this._onEndTurnHandler = this._onEndTurnHandler.bind(this);
        this._onClickStartOver = this._onClickStartOver.bind(this);
        this._newGame = this._newGame.bind(this);
        this._onHoverHandCardVisibilitySetting = this._onHoverHandCardVisibilitySetting.bind(this);
        this._onLeaveHandCardVisibilitySetting = this._onLeaveHandCardVisibilitySetting.bind(this);
        this._toggleOpponentHandCardVisibility = this._toggleOpponentHandCardVisibility.bind(this);
        this._onHoverThemeControl = this._onHoverThemeControl.bind(this);
        this._onLeaveThemeControl = this._onLeaveThemeControl.bind(this);
        this._toggleShowRecordData = this._toggleShowRecordData.bind(this);

        this.state = this._getInitialState();
        this._requestService = new RequestService('http://localhost:8000');

        const newGameURL = '/pazaak/api/new-game';
        this._requestService
            .get(newGameURL)
            .then(this._newGame);
    }

    render() {
        const scoreRow = this._getScoreRow();
        const table = this._getTable();
        const actionButtons = this._getActionButtons();
        const controls = this._getControls();

        return (
            <div className="PazaakGame">
                {scoreRow}
                {table}
                {actionButtons}
                {controls}
            </div>
        );
    }

    _getPlayerHeader(player) {
        const hasCurrentTurn = this.state.turn === player;
        let score = 0;
        let isPlayer = false;
        let isWinner = false;
        let recordData;

        switch (player) {
            case Player.PLAYER:
                score = this.state.player.score;
                isPlayer = true;
                isWinner = this.state.gameOver.id === GameStatus.PLAYER_WINS;
                recordData = this.state.player.record;
                break;
            case Player.OPPONENT:
                score = this.state.opponent.score;
                isWinner = this.state.gameOver.id === GameStatus.OPPONENT_WINS;
                recordData = this.state.opponent.record;
                break;
            default:
                console.error('invalid argument passed to PazaakGame._getPlayerHeader');
        }

        recordData.isDisplayed = this.state.isRecordDisplayed;
        const gameOverData = {
            value: this.state.gameOver.value,
            id: this.state.gameOver.id,
            isWinner: isWinner,
        };

        return (
            <PlayerHeader
                text={score}
                isPlayer={isPlayer}
                hasCurrentTurn={hasCurrentTurn}
                gameOverData={gameOverData}
                recordData={recordData}
            />
        );
    }

    _getScoreRow() {
        const gameOverBanner = this._getGameOverBanner();
        const playerScore = this._getPlayerHeader(Player.PLAYER);
        const opponentScore = this._getPlayerHeader(Player.OPPONENT);

        return (
            <div className="GameHeader">
                <div className="row info-header">
                    {gameOverBanner}
                </div>
                <div className="row text-align-left">
                    {playerScore}
                    {opponentScore}
                </div>
            </div>
        );
    }

    _getGameOverBanner() {
        return this.state.gameOver.value && (
            <h1 className="color-white">
                {this.state.gameOver.message}
            </h1>
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
                    onClickHandCard={this._onClickHandCard}
                />

                <TableSide
                    isPlayer={false}
                    placedCards={opponentPlaced}
                    handCards={opponentHand}
                    showHandCards={this.state.opponentHandCardVisibility.showOpponentHandCards}
                />
            </div>
        );
    }

    _getActionButtons() {
        const disableActionButtons = this.state.disableActionButtons || this.state.gameOver.value;

        return (
            <div className="row horizontal-row full-width">
                <IconButton
                    className="rounded-corners-small button-action"
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
                    className="rounded-corners-small button-action"
                    variant="warning"
                    fontAwesomeClassName="fas fa-arrow-up"
                    disableOnClick={true}
                    disabled={disableActionButtons}
                    onClick={this._onClickStand}
                >
                    Stand
                </IconButton>

                <IconButton
                    className="rounded-corners-small button-action"
                    variant="danger"
                    fontAwesomeClassName="fas fa-redo"
                    disableOnClick={true}
                    showSpinnerOnClick={true}
                    onClick={this._onClickStartOver}
                >
                    Start Over
                </IconButton>
            </div>
        );
    }

    _getControls() {
        return (
            <div className="controls row horizontal-row stick-right">
                <ActionIcon
                    className="color-white margin-right-small"
                    fontAwesomeClassName={this.state.opponentHandCardVisibility.icon}
                    onHover={this._onHoverHandCardVisibilitySetting}
                    onLeave={this._onLeaveHandCardVisibilitySetting}
                    onClick={this._toggleOpponentHandCardVisibility}
                />

                <ActionIcon
                    className="color-white margin-right-small"
                    fontAwesomeClassName="fas fa-list fa-2x"
                    onClick={this._toggleShowRecordData}
                />

                <ActionIcon
                    className="color-white"
                    fontAwesomeClassName={this.state.theme.icon}
                    disabled={true} // temporary
                    onClick={() => {}}
                    onHover={this._onHoverThemeControl}
                    onLeave={this._onLeaveThemeControl}
                />
            </div>
        );
    }

    /**
     * POSTs to the end-turn API endpoint.
     *
     * @param player one of {Player.PLAYER, Player.OPPONENT}.
     * @private
     */
    _getNextMove(player) {
        const url = '/pazaak/api/end-turn';
        const action = player === Player.PLAYER ? Action.END_TURN_PLAYER : Action.END_TURN_OPPONENT;
        const payload = {
            action: action,
            turn: player,
            // gameId: this.state.gameId,
        };

        this._requestService.post(url, payload)
            .then(this._onEndTurnHandler);
    }

    /**
     * Helper method that binds to the "End Turn" button.
     * @private
     */
    _onClickEndTurn() {
        this.setState({ disableActionButtons: true });
        this._getNextMove(Player.PLAYER)
    }

    _onEndTurnHandler(payload) {
        let timeoutMs = 0;

        if (this.state.turn === Player.PLAYER) {
            if (this.state.player.isStanding) {
                timeoutMs = 500;
            }
        } else {
            timeoutMs = 750;
        }

        if (timeoutMs > 0) {
            setTimeout(() => this._onReceiveEndTurnResponse(payload), timeoutMs);
        } else {
            this._onReceiveEndTurnResponse(payload);
        }
    }

    _onReceiveEndTurnResponse(payload) {
        // shape: {name: string, value: number}
        const status = payload.status;
        const gameOver = this._handleWinner(status);

        const playerToUpdate = payload.turn.justWent.value;
        const playerUpNext = payload.turn.upNext.value;
        const isPlayerStanding = (playerToUpdate === Player.PLAYER && payload.isStanding) || this.state.player.isStanding;
        const shouldWaitForUserInput = playerUpNext === Player.PLAYER && !isPlayerStanding;

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
            placed: payload.placed,
            hand: payload.hand,
            isStanding: payload.isStanding,
            record: payload.record,
        };
        let state = {};

        switch (player) {
            case Player.PLAYER:
                state = { player: playerData };
                break;
            case Player.OPPONENT:
                state = { opponent: playerData };
                break;
            default:
                console.error('invalid player argument passed to _getEndTurnUpdatedState');
        }

        return state;
    }

    _getInitialState() {
        // try to preserve settings if starting over
        const showOpponentHandCards = get(this.state, 'opponentHandCardVisibility.showOpponentHandCards', false);
        const currentTheme = get(this.state, 'theme.value', Theme.DARK);
        const isRecordDisplayed = get(this.state, 'isRecordDisplayed', false);

        return {
            player: {
                score: 0,
                isStanding: false,
                placed: [],
                hand: [],
                record: {
                    wins: 0,
                    losses: 0,
                    ties: 0,
                },
            },
            opponent: {
                score: 0,
                isStanding: false,
                placed: [],
                hand: [],
                record: {
                    wins: 0,
                    losses: 0,
                    ties: 0,
                },
            },
            turn: Player.PLAYER,
            disableActionButtons: false,
            isNewGame: true,
            gameOver: {
                value: false,
                id: GameStatus.GAME_ON,
            },
            opponentHandCardVisibility: {
                showOpponentHandCards: showOpponentHandCards,
                icon: this._getOpponentVisibilityIcon(showOpponentHandCards),
            },
            theme: {
                value: currentTheme,
                icon: this._getThemeControlIcon(currentTheme),
            },
            isRecordDisplayed,
        };
    }

    _onClickStartOver() {
        const url = '/pazaak/api/new-game';
        this._requestService.post(url)
            .then(this._newGame);
    }

    _newGame(payload) {
        const initialState = this._getInitialState();
        const gameId = payload.gameId;
        this._requestService.setPersistentPayload({ gameId });
        this.setState({
            ...initialState,
            ...payload,
        });
    }

    _onClickStand() {
        window.scrollTo(0, 0); // TODO -- better way of scrolling than using window?
        this.setState({ disableActionButtons: true });
        const url = '/pazaak/api/stand';
        const payload = { action: Action.STAND_PLAYER };
        this._requestService.post(url, payload)
            .then(this._onReceiveEndTurnResponse);
    }

    _onClickHandCard(index) {
        const url = '/pazaak/api/select-hand-card';
        const payload = {
            cardIndex: index,
            action: Action.HAND_PLAYER,
        };
        return this._requestService.post(url, payload)
            .then(this._onReceiveEndTurnResponse);
    }

    _handleWinner(status) {
        let gameOver = true;
        let message;
        switch (status.value) {
            case GameStatus.PLAYER_WINS:
                // player wins
                message = 'Player Wins!';
                break;
            case GameStatus.OPPONENT_WINS:
                // opponent wins
                message = 'Opponent Wins!';
                break;
            case GameStatus.TIE:
                // tie
                message = 'Tie!';
                break;
            case GameStatus.GAME_ON:
                // continue
                gameOver = false;
                break;
            case GameStatus.FORFEIT:
                // player forfeit
                break;
            default:
                console.error(`unexpected GameStatus enum value "${status.value}" received`);
        }

        this.setState({
            gameOver: {
                id: status.value,
                value: gameOver,
                message: message,
            },
        });

        return gameOver;
    }

    _getOpponentVisibilityIcon(shouldShow) {
        const enabledFaIcon = 'fa-eye';
        const disabledFaIcon = 'fa-eye-slash';
        const result = shouldShow ? enabledFaIcon : disabledFaIcon;

        return `fas ${result} fa-2x`;
    }

    _onHoverHandCardVisibilitySetting() {
        const opponentHandCardVisibility = this.state.opponentHandCardVisibility;
        const reversedIcon = this._getOpponentVisibilityIcon(!opponentHandCardVisibility.showOpponentHandCards);
        this.setState({
            opponentHandCardVisibility: {
                ...opponentHandCardVisibility,
                icon: reversedIcon,
            },
        });
    }

    _onLeaveHandCardVisibilitySetting() {
        const opponentHandCardVisibility = this.state.opponentHandCardVisibility;
        const icon = this._getOpponentVisibilityIcon(opponentHandCardVisibility.showOpponentHandCards);
        this.setState({
            opponentHandCardVisibility: {
                ...opponentHandCardVisibility,
                icon: icon,
            },
        });
    }

    _toggleOpponentHandCardVisibility() {
        const opponentHandCardVisibility = this.state.opponentHandCardVisibility;
        const isShowing = opponentHandCardVisibility.showOpponentHandCards;
        const icon = this._getOpponentVisibilityIcon(isShowing);
        this.setState({
            opponentHandCardVisibility: {
                ...opponentHandCardVisibility,
                showOpponentHandCards: !isShowing,
                icon: icon,
            },
        });
    }

    _getThemeControlIcon(currentTheme) {
        let result;
        switch (currentTheme) {
            case Theme.LIGHT:
                result = 'fa-sun';
                break;
            case Theme.DARK:
                result = 'fa-moon';
                break;
            default:
                // default
        }

        return `fas ${result} fa-2x`;
    }

    _getOppositeTheme(theme) {
        let result;
        switch (theme) {
            case Theme.LIGHT:
                result = Theme.DARK;
                break;
            case Theme.DARK:
                result = Theme.LIGHT;
                break;
            default:
                // error
        }

        return result;
    }

    _onHoverThemeControl() {
        const { theme } = this.state;
        const oppositeTheme = this._getOppositeTheme(this.state.theme.value);
        this.setState({
            theme: {
                ...theme,
                icon: this._getThemeControlIcon(oppositeTheme),
            },
        });
    }

    _onLeaveThemeControl() {
        const { theme } = this.state;
        this.setState({
            theme: {
                ...theme,
                icon: this._getThemeControlIcon(this.state.theme.value),
            },
        });
    }

    _toggleShowRecordData() {
        const isShowing = this.state.isRecordDisplayed;
        this.setState({ isRecordDisplayed: !isShowing });
    }
}

PazaakGame.propTypes = {};
export default PazaakGame;