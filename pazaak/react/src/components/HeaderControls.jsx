import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';

import '../styles/common.css';


export default class HeaderControls extends Component {

    static propTypes = {
        controls: PropTypes.arrayOf(
            PropTypes.shape({
                text: PropTypes.string.isRequired,
                onClick: PropTypes.func,
                className: PropTypes.string,
            }),
        ).isRequired,
        className: PropTypes.string,
    };

    constructor(props) {
        super(props);
        this._onCursorLeaveOption = this._onCursorLeaveOption.bind(this);
        this.state = { hoveringOverIndex: null };
    }

    shouldComponentUpdate(nextProps, nextState) {
        return nextState.hoveringOverIndex !== this.state.hoveringOverIndex;
    }

    render() {
        const className = classes({
            HeaderControls: true,
            [this.props.className]: this.props.className,
        });
        const controls = this.props.controls
            .filter(control => control)
            .map((control, index) => this._getControl({ ...control, index }));

        return (
            <div className={className}>
                {controls}
            </div>
        );
    }

    _getControl({ text, onClick, className, index }) {
        const totalClassName = classes({
            [`control-${index}`]: true,
            [className]: className,
            underlined: this.state.hoveringOverIndex === index,
            clickable: onClick,
        });
        const onHover = onClick && (() => this.setState({ hoveringOverIndex: index }));

        return (
            <span
                className={totalClassName}
                onClick={onClick}
                onMouseEnter={onHover}
                onMouseLeave={this._onCursorLeaveOption}
                key={index}
            >
                {text}
            </span>
        );
    }

    _onCursorLeaveOption() {
        this.setState({ hoveringOverIndex: null });
    }
}