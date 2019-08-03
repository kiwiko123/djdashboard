import React from 'react';
import PropTypes from 'prop-types';
import Button from 'react-bootstrap/Button';

import { classes } from '../../common/js/util';
import '../styles/IconButton.css';


class IconButton extends React.Component {
    static propTypes = {
        /* Typically, this will just be the button's text */
        children: PropTypes.node,

        /* React's Button variant - see https://react-bootstrap.github.io/components/buttons/ */
        variant: PropTypes.string,

        /* See https://fontawesome.com/icons */
        fontAwesomeClassName: PropTypes.string,

        disabled: PropTypes.bool,

        /* Automatically disable the button after click.
         * Button can be re-enabled by updating props.disabled to false.
         */
        disableOnClick: PropTypes.bool,

        /* Show a spinner instead of the Font Awesome icon after clicking the button.
         * The spinner will go away once props.disabled is false again.
         */
        showSpinnerOnClick: PropTypes.bool,

        onClick: PropTypes.func.isRequired,

        className: PropTypes.string,
    };

    static defaultProps = {
        disabled: false,
        disableOnClick: false,
        showSpinnerOnClick: false,
    };

    constructor(props) {
        super(props);
        this._onClick = this._onClick.bind(this);
        this.state = { isLoading: false };
    }

    componentDidUpdate(prevProps, prevState) {
        const wasDisabled = prevProps.disabled || prevState.disabled;
        if (wasDisabled && !this.props.disabled) {
            this.setState({
                isLoading: false,
                disabled: false,
            });
        }
    }

    render() {
        const buttonClassName = {
            "IconButton": true,
            [this.props.className]: this.props.className,
        };

        const iconClassName = classes({
            'icon': true,
            'fas fa-circle-notch fa-spin': this.state.isLoading,
            [this.props.fontAwesomeClassName]: !this.state.isLoading,
        });

        return (
            <Button
                className={buttonClassName}
                variant={this.props.variant}
                disabled={this.props.disabled || this.state.disabled}
                onClick={this._onClick}
            >
                <i className={iconClassName} />
                {this.props.children}
            </Button>
        );
    }

    _onClick() {
        this.setState({
            isLoading: this.props.showSpinnerOnClick,
            disabled: this.props.disabled || this.props.disableOnClick,
        });
        this.props.onClick();
    }
}

export default IconButton;