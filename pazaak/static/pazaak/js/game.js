// ==================================================================
// REGION Game Logic
// ==================================================================

g_PLAYER = "player";
g_OPPONENT = "opponent";

function _oppositePlayer(player) {
    let result;
    switch (player) {
        case g_PLAYER:
            result = g_OPPONENT;
            break;
        case g_OPPONENT:
            result = g_PLAYER;
            break;
        default:
            result = undefined;
    }
    return result;
}

function isGameOver(status) {
    return status === "game_over";
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
        await sleep(delayMs).then(() => {
            $(turnIconId).toggleClass("fas");
            $(turnIconId).toggleClass("far");
        });
    }

    $(turnIconId).removeClass("far");
    $(turnIconId).addClass("fas");
}

/**
 * Updates the turn icon ("PLAY" or "X") to the player specified by `turn`.
 *
 * @param turn one of {`g_PLAYER`, `g_OPPONENT`}.
 * @param withFlash boolean which will momentarily flash the turn icon if true; immediate switch if false.
 */
function _switchTurnIconTo(turn, withFlash = true) {
    switch (turn) {
        case g_PLAYER:
            _switchTurnGeneric(g_PLAYER, g_OPPONENT);
            break;
        case g_OPPONENT:
            _switchTurnGeneric(g_OPPONENT, g_PLAYER);
            break;
        default:
            console.error(`_switchTurnIconTo received invalid turn "${turn}"`);
            return;
    }

    if (withFlash) {
        _flashTurnIcon(turn);
    }
}

/**
 * Updates the score, by replacing it with the score from the JSON response.
 *
 * @param scoreId the string of the score ID to update.
 *          e.g., "#score-player"
 * @param cardScore int or string; the score/value of the just-placed card.
 */
function _updateScore(scoreId, cardScore) {
    $(scoreId).text(cardScore);
}

/**
 * Updates the Pazaak cards placed by a player.
 * In other words, adds new Pazaak cards to the screen, based on the JSON response.
 *
 * @param playerOrOpponent a string of either "player" or "opponent", used to identify the appropriate HTML ID.
 * @param card a string of the card parity and value, taken directly from the JSON response.
 *          e.g., jsonResponse["player"]["last_placed"] -> "+4"
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
 * Finds the necessary game information (card placed, score) from `jsonResponse`.
 * Adds the newly placed card and updates the score for `playerOrOpponent`.
 *
 * @param playerOrOpponent one of {`g_PLAYER`, `g_OPPONENT`}.
 * @param jsonResponse the response received from the server
 */
function updateSideFor(playerOrOpponent, jsonResponse) {
    const cardPlaced = jsonResponse["last_placed"];
    const placedLength = jsonResponse["size"];
    const cardScore = jsonResponse["score"];

    _updateScore(`#score-${playerOrOpponent}`, cardScore);
    _addPlacedCard(playerOrOpponent, cardPlaced, placedLength);
}

function gameOver(winner) {
    enableActionButtons(false);
    let message;
    switch (winner) {
        case "player":
            message = "Player wins!";
            break;
        case "opponent":
            message = "Opponent wins!";
            break;
        default:
            message = "It's a tie!";
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
function _onClickEndTurnButton() {
    enableActionButtons(false);
    _switchTurnIconTo(g_OPPONENT);
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
                turn: g_PLAYER
            },
            "success": success
        });
    });
}

function bindHand() {
    $("#hand-player > .pazaak-card").each((index, element) => {
        _bindCardInHand(element.id)
    });
}

function _bindCardInHand(cardId) {
    $(`#${cardId}`).click((e) => {
        $.ajax({
            type: "POST",
            data: {
                action: "hand-player",
                turn: "player",
                card: cardId
            },
            success: () => {}
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
            turn: playerOrOpponent
        },
        "success": success
    });
}

//TODO handle standing and winning
function _endTurnHandler(jsonResponse) {
    const playerToUpdate = jsonResponse["turn"];
    const playerJustWent = playerToUpdate === g_PLAYER;
    const otherPlayer = _oppositePlayer(playerToUpdate);
    const isStanding = jsonResponse["is_standing"];

    updateSideFor(playerToUpdate, jsonResponse);

    // if it's the opponent's turn, get their next move.
    // otherwise, it's the player's turn, so wait for user input
    if (!playerJustWent) {
        _switchTurnIconTo(otherPlayer);         // which is g_PLAYER in this conditional
        enableActionButtons(!playerJustWent);   // which is true in this conditional
        getMove(playerToUpdate, (response) => onEndTurn(response, otherPlayer));
    }
}

function onEndTurn(response, whoEndedTurn) {
    setTimeout(() => _endTurnHandler(response, whoEndedTurn), 1 * 1000);
}

// ==================================================================
// ENDREGION
// ==================================================================


// ==================================================================
// REGION Main
// ==================================================================

function setUpGame() {
    bindActionButton("#btn-end-turn", "POST", _onClickEndTurnButton, "end-turn-player", (response) => onEndTurn(response, g_PLAYER));
    //TODO bindActionButton("#btn-stand", "POST", undefined, "stand-player", () => {});
    bindActionButton("#btn-restart", "GET", undefined, "restart", _onClickRestartButton);
    bindHand();

    const initialPlayerMove = "{{ player_move }}";
    const pseudoResponse = {
        "last_placed": initialPlayerMove,
        "size": 1,
        "score": initialPlayerMove
    };

    updateSideFor(g_PLAYER, pseudoResponse);
    enableActionButtons(true);
    _switchTurnIconTo(g_PLAYER, false);
}

// ==================================================================
// ENDREGION
// ==================================================================