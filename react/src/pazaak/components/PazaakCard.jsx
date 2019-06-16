import React from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';

import '../styles/common.css';
import '../styles/colors.css';
import '../styles/PazaakCard.css';


class PazaakCard extends React.Component {
    static propTypes = {
        /** Equivalent to the 'parity' in the code.
         *  Consists of the '+'/'-' and the numeric value.
         *  e.g., '+5'
         */
        displayModifier: PropTypes.string,
        index: PropTypes.number.isRequired,
        handData: PropTypes.shape({
            isHandCard: PropTypes.bool,
            showValue: PropTypes.bool,
            onClick: PropTypes.func,
        }),
    };

    static defaultProps = {
        handData: {
            isHandCard: false,
        },
    };

    constructor(props) {
        super(props);
        this._onClickHandCard = this._onClickHandCard.bind(this);
    }

    _onClickHandCard() {
        const { handData } = this.props;
        if (handData.isHandCard && handData.onClick) {
            handData.onClick(this.props.index);
        }
    }

    render() {
        const { handData } = this.props;
        const cardClasses = classes({
            'horizontal-row': true,
            'PazaakCard': true,
            'pazaak-card-shape': true,
            'rounded-corners-small': true,
            'clickable': handData.isHandCard && handData.onClick,
        });
        const modifier = (!handData.isHandCard || handData.showValue) && this.props.displayModifier;

        return (
            <div className={cardClasses} onClick={this._onClickHandCard}>
                <span className="color-black">
                    {modifier}
                </span>
            </div>
        );
    }
}

export default PazaakCard;