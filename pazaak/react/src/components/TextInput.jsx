import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';
import '../styles/TextInput.css';


export default class TextInput extends PureComponent {
    static propTypes = {
        className: PropTypes.string,
        labelClassName: PropTypes.string,
        label: PropTypes.string.isRequired,
        placeholder: PropTypes.string,
        width: PropTypes.number,
        minLength: PropTypes.number,
        maxLength: PropTypes.number,
        maskInput: PropTypes.bool,
        disabled: PropTypes.bool,
        onTextEntered: PropTypes.func.isRequired,
    };

    static defaultProps = {
        maskInput: false,
        width: 32,
        minLength: 0,
        disabled: false,
    };

    static _id = 0;

    constructor(props) {
        super(props);
        this._labelId = TextInput._id++;
    }

    render() {
        const labelClassName = classes({
            TextInputLabel: true,
            [this.props.labelClassName]: true,
        });
        const label = `TextInput-${this._labelId}`;
        const inputType = this.props.maskInput ? 'password' : 'text';

        return (
            <div className="TextInput">
                <label
                    htmlFor={label}
                    className={labelClassName}
                >
                    {this.props.label}
                </label>
                <input
                    type={inputType}
                    className={this.props.className}
                    name={label}
                    size={this.props.width}
                    placeholder={this.props.placeholder}
                    minLength={this.props.minLength}
                    readOnly={this.props.disabled}
                    onChange={this.props.onTextEntered}
                />
            </div>
        );
    }
}