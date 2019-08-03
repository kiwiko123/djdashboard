import React from 'react';
import PropTypes from 'prop-types';

import { classes } from '../../common/js/util';

import '../styles/common.css';


class ActionIcon extends React.Component {
    static propTypes = {
        className: PropTypes.string,

        /* See https://fontawesome.com/icons */
        fontAwesomeClassName: PropTypes.string.isRequired,

        disabled: PropTypes.bool,

        onClick: PropTypes.func,

        onHover: PropTypes.func,

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

    _onMouseEnter() {
        this._invoke(this.props.onHover);
    }

    _onMouseLeave() {
        this._invoke(this.props.onLeave);
    }

    _onClick() {
        this._invoke(this.props.onClick);
    }

    _invoke(callable) {
        if (!this.props.disabled && callable) {
            callable();
        }
    }
}

export default ActionIcon;