import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';
import PazaakCard from './PazaakCard';

import '../styles/common.css';
import '../styles/TableSide.css';


class TableSide extends PureComponent {
    static propTypes = {
        isPlayer: PropTypes.bool,
        placedCards: PropTypes.array,
        handCards: PropTypes.array,
        showHandCards: PropTypes.bool,
    };

    static defaultProps = {
        showHandCards: true,
    };

    render() {
        const columnClass = classes({
            column: true,
            columnLeftBorder: this.props.isPlayer,
        });
        const placedCards = this._getCards(this.props.placedCards, false);
        const handCards = this.props.showHandCards && this._getCards(this.props.handCards, true);

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
        return cards && cards.map((card, index) => {
            return (
                <PazaakCard
                    key={index}
                    modifier={card}
                    isHandCard={isHand}
                />
            );
        });
    }
}

export default TableSide;