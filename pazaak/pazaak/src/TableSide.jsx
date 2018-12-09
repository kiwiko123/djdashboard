import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from './util';
import PazaakCard from './PazaakCard';

import './TableSide.css';
import './common.css';


class TableSide extends PureComponent {
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

    _getCards(cards, isHand) {
        return cards && cards.map(card => {
            return (
                <PazaakCard
                    key={card}
                    modifier={card}
                    isHandCard={isHand}
                />
            );
        });
    }
}

TableSide.propTypes = {
    isPlayer: PropTypes.bool,
    placedCards: PropTypes.array,
    handCards: PropTypes.array,
};
export default TableSide;