export const pad = (value: any, width: number, fill = ' ') => {
	/**
	 * Pad a string with a given character so that it is the correct length.
	 */
	value = value.toString();
	while (value.length < width) {
		value = fill + value;
	}
	return value;
};

export const zfill = (value: any, width: number) => {
	return pad(value, width, '0');
};

export const clip = <T extends number>(val: T, min: T, max: T) => {
	return Math.min(Math.max(val, min), max);
};
