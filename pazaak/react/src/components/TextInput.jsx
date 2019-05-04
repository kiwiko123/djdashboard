import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { classes } from '../js/util';
import '../styles/colors.css';
import '../styles/TextInput.css';


export default class TextInput extends PureComponent {
    static propTypes = {
        label: PropTypes.string.isRequired,
        onTextEntered: PropTypes.func.isRequired,
        className: PropTypes.string,
        labelClassName: PropTypes.string,
        placeholder: PropTypes.string,
        width: PropTypes.number,
        maxLength: PropTypes.number,
        maskInput: PropTypes.bool,
        disabled: PropTypes.bool,
        inputValidator: PropTypes.func,
        errorMessage: PropTypes.string,
    };

    static defaultProps = {
        maskInput: false,
        width: 32,
        disabled: false,
    };

    static _id = 0;

    constructor(props) {
        super(props);
        this._onTextEntered = this._onTextEntered.bind(this);
        this._validateInput = this._validateInput.bind(this);

        this._labelId = TextInput._id++;
        this._text = '';

        this.state = {
            isValid: true,
        };
    }

    render() {
        const isValid = this.state.isValid;
        const labelClassName = classes({
            TextInputLabel: true,
            [this.props.labelClassName]: true,
        });
        const inputClassName = classes({
            [this.props.className]: this.props.className,
            error: !isValid,
        });
        const label = `TextInput-${this._labelId}`;
        const inputType = this.props.maskInput ? 'password' : 'text';
        const errorMessage = this._getErrorMessageElement();

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
                    className={inputClassName}
                    name={label}
                    size={this.props.width}
                    placeholder={this.props.placeholder}
                    readOnly={this.props.disabled}
                    onChange={this._onTextEntered}
                    maxLength={this.props.maxLength}
                    onBlur={this._validateInput}
                />
                {errorMessage}
            </div>
        );
    }

    _onTextEntered(event) {
        this._text = event.target.value;
        this.props.onTextEntered(this._text);
    }

    _validateInput() {
        if (!this.props.inputValidator) {
            return;
        }

        const isValid = this.props.inputValidator(this._text);
        if (isValid !== this.state.isValid) {
            this.setState({ isValid });
        }
    }

    _getErrorMessageElement() {
        const errorMessage = this.props.errorMessage;
        return errorMessage && !this.state.isValid && (
            <span className="error-message">
                {errorMessage}
            </span>
        );
    }
}