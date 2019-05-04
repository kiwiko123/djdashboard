import PropTypes from 'prop-types';


export const TextInputProps = {
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