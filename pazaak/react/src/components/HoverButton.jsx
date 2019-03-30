import React from 'react';
import PropTypes from 'prop-types';

import { classes } from '../js/util';

import '../styles/HoverButton.css';


class HoverButton extends React.Component {
    static propTypes = {
        className: PropTypes.string,

        /* See https://fontawesome.com/icons */
        fontAwesomeClassName: PropTypes.string.isRequired,

        disabled: PropTypes.bool,

        onClick: PropTypes.func.isRequired,

        onHover: PropTypes.func.isRequired,

        onLeave: PropTypes.func,
    };

    static defaultProps = {
        className: '',
        disabled: false,
    };

    constructor(props) {
        super(props);
        this._onMouseEnter = this._onMouseEnter.bind(this);
        this._onMouseLeave = this._onMouseLeave.bind(this);
    }

    _onMouseEnter() {
        this.props.onHover();
    }

    _onMouseLeave() {
        if (this.props.onLeave) {
            this.props.onLeave();
        }
    }

    render() {
        const classNames = classes({
            HoverButton: true,
            [this.props.className]: this.props.className,
            [this.props.fontAwesomeClassName]: true,
        });

        return (
            <i className={classNames}
               onClick={this.props.onClick}
               onMouseEnter={this._onMouseEnter}
               onMouseLeave={this._onMouseLeave}
            />
        );
    }
}

export default HoverButton;