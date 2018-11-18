// ==================================================================
// REGION Game Logic
// ==================================================================

PLAYER = "player";
OPPONENT = "opponent";
_WINNER = "";

function _oppositePlayer(player) {
    let result;
    switch (player) {
        case PLAYER:
            result = OPPONENT;
            break;
        case OPPONENT:
            result = PLAYER;
            break;
        default:
            result = undefined;
    }
    return result;
}

function signalGameOver(player) {
    _WINNER = player;
}

// ==================================================================
// ENDREGION
// ==================================================================

// ==================================================================
// REGION Helpers
// ==================================================================

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// ==================================================================
// ENDREGION
// ==================================================================

// ==================================================================
// REGION Game Logic - Cosmetic
// ==================================================================

function _switchTurnGeneric(from, to) {
    const fromId = `#icon-turn-${from}`;
    const toId = `#icon-turn-${to}`;
    $(fromId).removeClass("far fa-times-circle");
    $(fromId).addClass("fas fa-play-circle");
    $(toId).removeClass("fas fa-play-circle");
    $(toId).addClass("far fa-times-circle");
}

async function _flashTurnIcon(turn) {
    const turnIconId = `#icon-turn-${turn}`;
    const delayMs = 0.15 * 1000;
    const repititions = 5;

    for (let i = 0; i < repititions; ++i) {
        await sleep(delayMs).then(() => $(turnIconId).toggleClass("fas far"));
    }

    $(turnIconId).removeClass("far");
    $(turnIconId).addClass("fas");
}

/**
 * Updates the turn icon ("PLAY" or "X") to the player specified by `turn`.
 *
 * @param turn one of {`PLAYER`, `OPPONENT`}.
 * @param withFlash boolean which will momentarily flash the turn icon if true; immediate switch if false.
 */
async function switchTurnIconTo(turn, withFlash = true) {
    switch (turn) {
        case PLAYER:
            _switchTurnGeneric(PLAYER, OPPONENT);
            break;
        case OPPONENT:
            _switchTurnGeneric(OPPONENT, PLAYER);
            break;
        default:
            console.error(`_switchTurnIconTo received invalid turn "${turn}"`);
            return;
    }

    if (withFlash) {
        await _flashTurnIcon(turn);
    }
}

function removeAllClassesFrom(elementId) {
    const classNames = $(elementId).attr("class").split(/\s+/);
    classNames.forEach((cls) => $(elementId).removeClass(cls));
}

/**
 * Updates the score, by replacing it with the score from the JSON response.
 *
 * @param scoreId the string of the score ID to update.
 *          e.g., "#score-player"
 * @param cardValue int or string; the score/value of the just-placed card.
 */
function _updateScore(scoreId, cardValue) {
    scoreId = `${scoreId} span`;
    let score = $(scoreId).text().trim();
    if (score) {
        score = Number(score);
    }
    $(scoreId).text(score + cardValue);
}

/**
 * Updates the Pazaak cards placed by a player.
 * In other words, adds new Pazaak cards to the screen, based on the JSON response.
 *
 * @param playerOrOpponent a string of either "player" or "opponent", used to identify the appropriate HTML ID.
 * @param card a string of the card parity and value, taken directly from the JSON response.
 *          e.g., jsonResponse["player"]["move"] -> "+4"
 * @param placedLength an integer of the number of cards (including `card`) that have been placed.
 *          Also taken directly from the JSON response; e.g., jsonResponse["player"]["size"]
 */
function _addPlacedCard(playerOrOpponent, card, placedLength) {
    const placedDivID = `#placed-cards-${playerOrOpponent}`;
    const cardID = `card-placed-${playerOrOpponent}-${placedLength}`;
    const divHtml = `<div id=${cardID} class="horizontal-row pazaak-card"><p>${card}</p></div>`;
    $(placedDivID).append(divHtml);
}

/**
 * Finds the necessary game information (card placed, score) from `response`.
 * Adds the newly placed card and updates the score for `playerOrOpponent`.
 *
 * @param playerOrOpponent one of {`PLAYER`, `OPPONENT`}.
 * @param response the JSON response received from the server
 */
function updateSideFor(playerOrOpponent, response) {
    const cardPlaced = response.move;
    const placedLength = response.size;

    if (cardPlaced) {
        _updateScore(`#score-${playerOrOpponent}`, cardPlaced);
        _addPlacedCard(playerOrOpponent, cardPlaced, placedLength);
    }
}

function gameOver(winner) {
    enableActionButtons(false);

    let message;
    let tie = false;
    switch (winner) {
        case PLAYER:
            message = "Player wins!";
            break;
        case OPPONENT:
            message = "Opponent wins!";
            break;
        default:
            message = "It's a tie!";
            tie = true;
    }

    if (tie) {
        [PLAYER, OPPONENT].forEach((turn) => {
            const turnIconId = `#icon-turn-${turn}`;
            removeAllClassesFrom(turnIconId);
            $(turnIconId).addClass("fas fa-handshake fa-3x");
        });
    } else {
        const loser = _oppositePlayer(winner);
        const winnerIconId = `#icon-turn-${winner}`;
        const loserIconId = `#icon-turn-${loser}`;

        removeAllClassesFrom(winnerIconId);
        removeAllClassesFrom(loserIconId);

        $(winnerIconId).addClass("fas fa-trophy fa-3x");
        $(loserIconId).addClass("fas fa-times fa-3x");
    }

    $("#banner-winner-text").text(message);
}

// ==================================================================
// ENDREGION
// ==================================================================

// ==================================================================
// REGION Button Actions
// ==================================================================

/**
 * Refreshes the page.
 */
function _onClickRestartButton() {
    location.href = $("#btn-restart").data("url");;
}

/**
 * Disables the "End Turn" and "Stand" buttons.
 * Updates the turn icon to the opponent side.
 */
function _onClickActionButton() {
    enableActionButtons(false);
    switchTurnIconTo(OPPONENT);
}

/**
 * Toggles the "End Turn" and "Stand" buttons.
 *
 * @param enable boolean; true enables the buttons, and false disables.
 */
function enableActionButtons(enable) {
    $("#btn-end-turn").prop("disabled", !enable);
    $("#btn-stand").prop("disabled", !enable);
}

// ==================================================================
// ENDREGION
// ==================================================================

// ==================================================================
// REGION Element Binding - Logic
// ==================================================================

function bindActionButton(buttonID, requestType, preceder, action, success) {
    $(buttonID).click((e) => {
        if (preceder) {
            preceder();
        }

        $.ajax({
            type: requestType,
            data: {
                "action": action,
                turn: PLAYER,
                winner: _WINNER
            },
            "success": (response) => _successWrapper(response, success)
        });
    });
}

function bindHand(preceder, success) {
    $("#hand-player > .pazaak-card").each((index, element) => {
        _bindCardInHand(element.id, index, preceder, success)
    });
}

function _bindCardInHand(cardId, cardIndex, preceder, success) {
    $(`#${cardId}`).click((e) => {
        if (preceder) {
            preceder();
        }

        $.ajax({
            type: "POST",
            data: {
                action: "hand-player",
                turn: PLAYER,
                card_index: cardIndex
            },
            success: (response) => _successWrapper(response, success)
        });
    });
}

// ==================================================================
// ENDREGION
// ==================================================================

// ==================================================================
// REGION Request/Response - Logic
// ==================================================================

function getMove(playerOrOpponent, success) {
    $.ajax({
        type: "POST",
        data: {
            action: `end-turn-${playerOrOpponent}`,
            turn: playerOrOpponent,
            winner: _WINNER
        },
        "success": (response) => _successWrapper(response, success)
    });
}

function _successWrapper(response, proceder) {
    if (response.error) {
        console.error(`error: "${response.error}"`);
        //TODO render error
    } else {
        proceder(response);
    }
}

//TODO handle standing
function _endTurnHandler(response) {
    const winner = response.winner;
    const status = response.status;

    if (status === "game-over") {
        gameOver(winner);
        return;
    }

    let playerToUpdate = response.turn;
    let otherPlayer = _oppositePlayer(playerToUpdate);
    let playerJustWent = playerToUpdate === PLAYER;   // player meaning the user
    const isStanding = response.is_standing;

    // response.move is 0 when the player is standing (PazaakCard.empty())
    if (isStanding && !response.move) {
        // hacky way to not update the player's side if they're standing
        response.move = null;
    }

    updateSideFor(playerToUpdate, response);

    if (winner) {
        signalGameOver(winner);
    }

    // if it's the opponent's turn, get their next move.
    // otherwise, it's the player's turn, so wait for user input
    if (isStanding || !playerJustWent) {
        // in this conditional:
        //   * otherPlayer is always PLAYER
        //   * playerJustWent is always false

        switchTurnIconTo(otherPlayer);
        getMove(playerToUpdate, (response) => onEndTurn(response, otherPlayer));
    }

    enableActionButtons(!isStanding && playerJustWent);
}

function onEndTurn(response, whoEndedTurn) {
    setTimeout(() => _endTurnHandler(response, whoEndedTurn), 1 * 1000);
}

// ==================================================================
// ENDREGION
// ==================================================================