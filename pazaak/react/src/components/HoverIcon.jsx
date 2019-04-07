import React from 'react';
import PropTypes from 'prop-types';

import { classes } from '../js/util';

import '../styles/common.css';


class HoverIcon extends React.Component {
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
        this._onClick = this._onClick.bind(this);
        this._onMouseEnter = this._onMouseEnter.bind(this);
        this._onMouseLeave = this._onMouseLeave.bind(this);
    }

    _onMouseEnter() {
        if (!this.props.disabled) {
            this.props.onHover();
        }
    }

    _onMouseLeave() {
        if (!this.props.disabled && this.props.onLeave) {
            this.props.onLeave();
        }
    }

    _onClick() {
        if (!this.props.disabled) {
            this.props.onClick();
        }
    }

    render() {
        const className = classes({
            HoverIcon: true,
            [this.props.fontAwesomeClassName]: true,
            [this.props.className]: true,
            'clickable': !this.props.disabled,
            'icon-disabled': this.props.disabled,
        });

        return (
            <i className={className}
               onClick={this._onClick}
               onMouseEnter={this._onMouseEnter}
               onMouseLeave={this._onMouseLeave}
            />
        );
    }
}

export default HoverIcon;