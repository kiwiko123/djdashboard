import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Cell from './Cell';

import '../../common/styles/colors.css';


export default class TextCell extends Component {

    static propTypes = {
        ...Cell.propTypes,
        text: PropTypes.string,
    };

    static defaultProps = {
        ...Cell.defaultProps,
        text: null,
    };

    render() {
        return (
            <Cell
                className={this.props.className}
                onClick={this.props.onClick}
                draggable={this.props.draggable}
                onDragStart={this.props.onDragStart}
                onDragOver={this.props.onDragOver}
                onDrop={this.props.onDrop}
            >
                <span className="color-white">
                    {this.props.text}
                </span>
            </Cell>
        );
    }
}