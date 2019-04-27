/**
 * Given an object of {className: boolean}, returns a string of classes to apply to a component.
 * Example:
 * classes({foo: true, bar: false, baz: true}) => 'foo baz'
 *
 * @param obj        whose keys are classNames and values are booleans.
 * @returns {string} of classNames to apply to a component.
 */
export function classes(obj) {
    return Object.keys(obj)
        .filter(key => key)
        .filter(key => obj[key])
        .join(' ');
}
