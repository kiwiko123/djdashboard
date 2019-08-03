import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../../common/js/util';

import '../styles/common.css';
import '../styles/colors.css';
import '../styles/PlayerHeader.css';


class PlayerHeader extends PureComponent {
    static propTypes = {
        text: PropTypes.oneOfType([
            PropTypes.number,
            PropTypes.string,
        ]),
        isPlayer: PropTypes.bool.isRequired,
        hasCurrentTurn: PropTypes.bool.isRequired,
        gameOverData: PropTypes.shape({
            value: PropTypes.bool,
            id: PropTypes.number,
            isWinner: PropTypes.bool,
        }),
        recordData: PropTypes.shape({
            wins: PropTypes.number.isRequired,
            losses: PropTypes.number.isRequired,
            ties: PropTypes.number.isRequired,
            isDisplayed: PropTypes.bool.isRequired,
        }),
    };

    static defaultProps = {
        gameOverData: {
            value: false,
            isWinner: false,
        },
        recordData: {
            wins: 0,
            losses: 0,
            ties: 0,
            isDisplayed: false,
        },
    };

    render() {
        const playerLabel = this.props.isPlayer ? 'You' : 'Opponent';
        const scoreLabel = `${playerLabel}: ${this.props.text}`;
        const icon = this._getIcon();
        const recordContent = this._getRecordContent();
        const containerClassName = classes({
            PlayerHeader: true,
            column: true,
            'column-left-border': this.props.isPlayer,
            'column-right-border': !this.props.isPlayer,
        });

        // TODO flash turn icon on switch
        return (
            <div className={containerClassName}>
                {recordContent}
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

    _getRecordContent() {
        return this.props.recordData.isDisplayed && (
            <div className="record color-gray">
                <span className="row">{`Wins: ${this.props.recordData.wins}`}</span>
                <span className="row">{`Losses: ${this.props.recordData.losses}`}</span>
                <span className="row">{`Ties: ${this.props.recordData.ties}`}</span>
            </div>
        );
    }
}

export default PlayerHeader;