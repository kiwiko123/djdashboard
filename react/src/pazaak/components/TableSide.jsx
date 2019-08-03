import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { chunk } from 'lodash';
import PazaakCard from './PazaakCard';
import Collapsible from './Collapsible';
import { classes } from '../../common/js/util';

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
        const className = "card-placeholder pazaak-card-shape horizontal-row rounded-corners-small";
        return (
            <div key={key}
                 className={className}
            />
        );
    }

    _getPlaceholders(numCardsPlaced, maxCardsPerRow) {
        const upperBound = Math.max(1, numCardsPlaced);
        const maxPlaceholdersPerRow = maxCardsPerRow * Math.ceil(upperBound / maxCardsPerRow);
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

    _getCards(cards, isHandCard, maxCardsPerRow) {
        let result = cards.map((card, index) => this._getCard(card, index, isHandCard));
        if (!isHandCard) {
            const placeholders = this._getPlaceholders(cards.length, maxCardsPerRow);
            result = result.concat(placeholders);
        }

        return result;
    }

    _getCollapsibleCardRow(index, groupedCards, isCollapsed, hideCollapseIcon, columnClassName) {
        return (
            <Collapsible
                key={index}
                className="row"
                isCollapsed={isCollapsed}
                hideCollapseIcon={hideCollapseIcon}
            >
                <div className={columnClassName}>
                    {groupedCards}
                </div>
            </Collapsible>
        );
    }

    _getGroupedCollapsibleCardRows(maxCardsPerRow, columnClassName) {
        const placedCards = this._getCards(this.props.placedCards, false, maxCardsPerRow);
        const groupedCards = chunk(placedCards, maxCardsPerRow);
        return groupedCards.map((group, index) => this._getCollapsibleCardRow(
            index,
            group,
            index < (groupedCards.length - 1),
            groupedCards.length === 1,
            columnClassName
        ));
    }

    render() {
        const maxCardsPerRow = 4;
        const columnClass = classes({
            column: true,
            columnLeftBorder: this.props.isPlayer,
        });

        const collapsibleGroupedCards = this._getGroupedCollapsibleCardRows(maxCardsPerRow, columnClass);
        const handCards = this._getCards(this.props.handCards, true);

        return (
            <div className="TableSide full-width">
                {collapsibleGroupedCards}
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