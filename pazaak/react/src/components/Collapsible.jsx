import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import ActionIcon from './ActionIcon';
import { classes } from '../js/util';

import '../styles/colors.css';
import '../styles/Collapsible.css';


class Collapsible extends PureComponent {
    static propTypes = {
        className: PropTypes.string,
        iconClassName: PropTypes.string,
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

        this._isCollapsed = this.props.isCollapsed;

        this.state = {
            iconClassName: this._geticonClassName(this.props.isCollapsed),
            collapseIconColorClassName: 'color-gray-light',
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.isCollapsed !== this.props.isCollapsed) {
            this._isCollapsed = this.props.isCollapsed;
        }
    }

    render() {
        const className = classes({
            'Collapsible': true,
            [this.props.className]: this.props.className,
        });
        const collapseIcon = this._getCollapseIcon();
        const content = !this._isCollapsed && this.props.children;

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
            [this.props.iconClassName]: this.props.iconClassName,
            [this.state.collapseIconColorClassName]: true,
        });

        return !this.props.hideCollapseIcon && (
            <ActionIcon
                className={hoverIconClassName}
                fontAwesomeClassName={this.state.iconClassName}
                onClick={this._toggleCollapse}
                onHover={this._reverseCollapseIcon}
                onLeave={this._restoreCollapseIcon}
            />
        );
    }

    _geticonClassName(isCollapsed) {
        return classes({
            'fas fa-chevron-down': isCollapsed,
            'fas fa-chevron-up': !isCollapsed,
        });
    }

    _toggleCollapse() {
        const iconClassName = this._geticonClassName(this._isCollapsed);
        this._isCollapsed = !this._isCollapsed;
        this.setState({
            iconClassName: iconClassName,
            collapseIconColorClassName: 'color-gray-light',
        });
    }

    _reverseCollapseIcon() {
        const reversedIconClassName = this._geticonClassName(!this._isCollapsed);
        this.setState({
            iconClassName: reversedIconClassName,
            collapseIconColorClassName: 'color-gray-dark',
        });
    }

    _restoreCollapseIcon() {
        const iconClassName = this._geticonClassName(this._isCollapsed);
        this.setState({
            iconClassName: iconClassName,
            collapseIconColorClassName: 'color-gray-light',
        });
    }

}

export default Collapsible;