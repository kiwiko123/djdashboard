import React from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';

import '../styles/IconButton.css';


class IconButton extends React.PureComponent {
    render() {
        const label = ` ${this.props.label}`;
        return (
            <Button
                className="IconButton"
                bsStyle={this.props.bsStyle}
                disabled={this.props.disabled}
                onClick={this.props.onClick}>
                <i className={this.props.faClassName}>
                    {label}
                </i>
            </Button>
        );
    }
}

IconButton.propTypes = {
    label: PropTypes.string,
    bsStyle: PropTypes.string,
    faClassName: PropTypes.string,
    disabled: PropTypes.bool,
    onClick: PropTypes.func,
};
export default IconButton;