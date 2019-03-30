import React, { Component } from 'react';
import PropTypes from 'prop-types';
import PazaakCard from './PazaakCard';
import { classes } from '../js/util';

import '../styles/common.css';
import '../styles/TableSide.css';
import '../styles/PazaakCard.css';


class TableSide extends Component {
    static propTypes = {
        isPlayer: PropTypes.bool,
        placedCards: PropTypes.arrayOf(
            PropTypes.shape({
                modifier: PropTypes.number.isRequired,
                parity: PropTypes.string.isRequired,
            }),
        ).isRequired,
        handCards: PropTypes.arrayOf(
            PropTypes.shape({
                modifier: PropTypes.number.isRequired,
                parity: PropTypes.string.isRequired,
            }),
        ),
        showHandCards: PropTypes.bool,
        onClickHandCard: PropTypes.func,
    };

    static defaultProps = {
        showHandCards: true,
        placedCards: [],
        handCards: [],
    };

    _getPlaceholder(key) {
        const className = "card-placeholder pazaak-card-shape horizontal-row";
        return (
            <div key={key}
                 className={className}
            />
        );
    }

    _getPlaceholders(numCardsPlaced) {
        const numCardsPerRow = 4;
        const upperBound = Math.max(1, numCardsPlaced);
        const maxPlaceholdersPerRow = numCardsPerRow * Math.ceil(upperBound / numCardsPerRow);
        const numPlaceholdersNeeded = Math.abs(maxPlaceholdersPerRow - numCardsPlaced);
        const placeholders = [];

        for (let i = 0; i < numPlaceholdersNeeded; ++i) {
            const placeholder = this._getPlaceholder(i + numCardsPlaced);
            placeholders.push(placeholder);
        }

        return placeholders;
    }

    _getCard(card, index, isHandCard) {
        const handData = {
            isHandCard,
            showValue: this.props.showHandCards,
            onClick: this.props.onClickHandCard,
        };

        return (
            <PazaakCard
                key={index}
                index={index}
                displayModifier={card.parity}
                handData={handData}
            />
        );
    }

    _getCards(cards, isHandCard) {
        let result = cards.map((card, index) => this._getCard(card, index, isHandCard));
        if (!isHandCard) {
            const placeholders = this._getPlaceholders(cards.length);
            result = result.concat(placeholders);
        }

        return result;
    }

    render() {
        const columnClass = classes({
            column: true,
            columnLeftBorder: this.props.isPlayer,
        });
        const placedCards = this._getCards(this.props.placedCards, false);
        const handCards = this._getCards(this.props.handCards, true);

        return (
            <div className="TableSide full-width">
                <div className="row">
                    <div className={columnClass}>
                        {placedCards}
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className={columnClass}>
                        {handCards}
                    </div>
                </div>
            </div>
        );
    }
}

export default TableSide;