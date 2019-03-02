import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';

import 'font-awesome/css/font-awesome.min.css';
import '../styles/common.css';
import '../styles/colors.css';
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
        const playerLabel = this.props.isPlayer ? 'You' : 'Opponent';
        const scoreLabel = `${playerLabel}: ${this.props.text}`;
        const icon = this._getIcon();
        const containerClassName = classes({
            PlayerHeader: true,
            column: true,
            'column-left-border': this.props.isPlayer,
            'column-right-border': !this.props.isPlayer,
        });

        // TODO flash turn icon on switch
        return (
            <div className={containerClassName}>
                <div className="icon-turn">
                    {icon}
                </div>
                <h2 className="color-white">{scoreLabel}</h2>
            </div>
        );
    }

    _getIcon() {
        const { gameOverData, hasCurrentTurn } = this.props;
        const iconClasses = classes({
            'color-white': !gameOverData.isWinner,
            'fas fa-trophy fa-3x color-gold': gameOverData.value && gameOverData.isWinner,
            'fas fa-play-circle fa-3x': !gameOverData.value && hasCurrentTurn,
            'far fa-times-circle fa-3x': !gameOverData.value && !hasCurrentTurn,
        });

        return (
            <i className={iconClasses} />
        );
    }
}

export default PlayerHeader;