import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../../common/js/util';

import '../../common/styles/common.css';


export default class Cell extends Component {

    static propTypes = {
        children: PropTypes.node,
        className: PropTypes.string,
        onClick: PropTypes.func,
        draggable: PropTypes.bool,
        onDragStart: PropTypes.func,
        onDragOver: PropTypes.func,
        onDrop: PropTypes.func,
    };

    static defaultProps = {
        children: null,
        className: null,
        onClick: null,
        draggable: false,
        onDragStart: () => {},
        onDragOver: (event) => { event.preventDefault(); },
        onDrop: () => {},
    };

    constructor(props) {
        super(props);
        this._onClick = this._onClick.bind(this);
    }

    render() {
        const className = classes({
            Cell: true,
            [this.props.className]: this.props.className,
            'clickable': this.props.onClick,
        });

        return (
            <div
                className={className}
                onClick={this._onClick}
                draggable={this.props.draggable}
                onDragStart={this.props.onDragStart}
                onDragOver={this.props.onDragOver}
                onDrop={this.props.onDrop}
            >
                {this.props.children}
            </div>
        );
    }

    _onClick(event) {
        if (this.props.onClick) {
            this.props.onClick(event);
        }
    }
}