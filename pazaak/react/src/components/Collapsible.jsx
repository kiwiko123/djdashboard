import React, { Component } from 'react';
import PropTypes from 'prop-types';
import HoverIcon from './HoverIcon';
import { classes } from '../js/util';

import '../styles/colors.css';
import '../styles/Collapsible.css';


class Collapsible extends Component {
    static propTypes = {
        className: PropTypes.string,
        collapseIconClassName: PropTypes.string,
        children: PropTypes.node,
        isCollapsed: PropTypes.bool.isRequired,
        hideCollapseIcon: PropTypes.bool,
    };

    static defaultProps = {
        isCollapsed: false,
        hideCollapseIcon: false,
    };

    constructor(props) {
        super(props);

        this._toggleCollapse = this._toggleCollapse.bind(this);
        this._reverseCollapseIcon = this._reverseCollapseIcon.bind(this);
        this._restoreCollapseIcon = this._restoreCollapseIcon.bind(this);

        this.state = {
            isCollapsed: this.props.isCollapsed,
            collapseIconClassName: this._getCollapseIconClassName(this.props.isCollapsed),
            collapseIconColorClassName: 'color-gray-light',
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.isCollapsed !== this.props.isCollapsed) {
            this.setState({ isCollapsed: this.props.isCollapsed });
        }
    }

    render() {
        const className = classes({
            'Collapsible': true,
            [this.props.className]: this.props.className,
        });
        const collapseIcon = this._getCollapseIcon();
        const content = !this.state.isCollapsed && this.props.children;

        return (
            <div className={className}>
                {collapseIcon}
                {content}
            </div>
        );
    }

    _getCollapseIcon() {
        const hoverIconClassName = classes({
            'collapse-button': true,
            [this.props.collapseIconClassName]: this.props.collapseIconClassName,
            [this.state.collapseIconColorClassName]: true,
        });

        return !this.props.hideCollapseIcon && (
            <HoverIcon
                className={hoverIconClassName}
                fontAwesomeClassName={this.state.collapseIconClassName}
                onClick={this._toggleCollapse}
                onHover={this._reverseCollapseIcon}
                onLeave={this._restoreCollapseIcon}
            />
        );
    }

    _getCollapseIconClassName(isCollapsed) {
        return classes({
            'fas fa-chevron-down': isCollapsed,
            'fas fa-chevron-up': !isCollapsed,
        });
    }

    _toggleCollapse() {
        const isCollapsed = this.state.isCollapsed;
        const iconClassName = this._getCollapseIconClassName(isCollapsed);
        this.setState({
            isCollapsed: !isCollapsed,
            collapseIconClassName: iconClassName,
            collapseIconColorClassName: 'color-gray-light',
        });
    }

    _reverseCollapseIcon() {
        const isCollapsed = this.state.isCollapsed;
        const reversedIconClassName = this._getCollapseIconClassName(!isCollapsed);
        this.setState({
            collapseIconClassName: reversedIconClassName,
            collapseIconColorClassName: 'color-gray-dark',
        });
    }

    _restoreCollapseIcon() {
        const isCollapsed = this.state.isCollapsed;
        const iconClassName = this._getCollapseIconClassName(isCollapsed);
        this.setState({
            collapseIconClassName: iconClassName,
            collapseIconColorClassName: 'color-gray-light',
        });
    }

}

export default Collapsible;