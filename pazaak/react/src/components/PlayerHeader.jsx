import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';

import 'font-awesome/css/font-awesome.min.css';
import '../styles/common.css';
import '../styles/PlayerHeader.css';


class PlayerHeader extends PureComponent {
    static propTypes = {
        text: PropTypes.oneOfType([
            PropTypes.number,
            PropTypes.string,
        ]),
        isPlayer: PropTypes.bool,
        hasCurrentTurn: PropTypes.bool,
        gameOverData: PropTypes.shape({
            value: PropTypes.bool,
            id: PropTypes.number,
            isWinner: PropTypes.bool,
        })
    };

    static defaultProps = {
        gameOverData: {
            value: false,
            isWinner: false,
        },
    };

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
        const scoreLabel = `${playerLabel}: ${this.props.text}`;
        divClassName = `PlayerHeader column ${divClassName}`;

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
        const { gameOverData, hasCurrentTurn } = this.props;
        const iconClasses = classes({
            'fas fa-trophy fa-3x': gameOverData.value && gameOverData.isWinner,
            'fas fa-play-circle fa-3x': !gameOverData.value && hasCurrentTurn,
            'far fa-times-circle fa-3x': !gameOverData.value && !hasCurrentTurn,
        });

        return (
            <i className={iconClasses} />
        );
    }
}

export default PlayerHeader;