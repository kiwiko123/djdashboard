import React from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';

import '../styles/common.css';
import '../styles/PazaakCard.css';


class PazaakCard extends React.PureComponent {
    static propTypes = {
        modifier: PropTypes.string.isRequired,
        isHandCard: PropTypes.bool,
    };

    render() {
        const cardClasses = classes({
            'horizontal-row': true,
            'pazaak-card': true,
            'hand-card': this.props.isHandCard,
        });

        return (
            <div className={cardClasses}>
                {this.props.modifier}
            </div>
        );
    }
}

export default PazaakCard;