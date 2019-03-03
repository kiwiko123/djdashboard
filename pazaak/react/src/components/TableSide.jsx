import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';
import PazaakCard from './PazaakCard';

import '../styles/common.css';
import '../styles/TableSide.css';


class TableSide extends PureComponent {
    static propTypes = {
        isPlayer: PropTypes.bool,
        placedCards: PropTypes.arrayOf(
            PropTypes.shape({
                modifier: PropTypes.number,
                parity: PropTypes.string,
            }),
        ).isRequired,
        handCards: PropTypes.arrayOf(
            PropTypes.shape({
                modifier: PropTypes.number,
                parity: PropTypes.string,
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
        return cards.map((card, index) => this._getCard(card, index, isHandCard));
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