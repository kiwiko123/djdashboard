import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from './util';

import 'font-awesome/css/font-awesome.min.css';
import './Score.css';
import './common.css';


class Score extends PureComponent {
    render() {
        let divClassName, playerLabel;
        if (this.props.isPlayer) {
            divClassName = 'column-left-border';
            playerLabel = 'You';
        } else {
            divClassName = 'column-right-border';
            playerLabel = 'Opponent';
        }
        const icon = this._getIcon();
        const scoreLabel = `${playerLabel}: ${this.props.score}`;
        divClassName = `Score column ${divClassName}`;

        // TODO flash turn icon on switch
        return (
            <div className={divClassName}>
                <div className="icon-turn">
                    {icon}
                </div>
                <h2>{scoreLabel}</h2>
            </div>
        );
    }

    _getIcon() {
        const { hasCurrentTurn } = this.props;
        const iconClasses = classes({
            'fas fa-play-circle fa-3x': hasCurrentTurn,
            'far fa-times-circle fa-3x': !hasCurrentTurn,
        });

        return (
            <i className={iconClasses} />
        );
    }
}

Score.propTypes = {
    score: PropTypes.number,
    isPlayer: PropTypes.bool,
    hasCurrentTurn: PropTypes.bool,
};
export default Score;