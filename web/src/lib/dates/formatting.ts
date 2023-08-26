import { zfill } from '$lib/utils';

export const dateToPath = (date: Date, prefix = '', suffix = '') => {
	/**
	 * Convert a date to a path.
	 */
	return `${prefix}/${date.getUTCFullYear()}/${zfill(date.getUTCMonth() + 1, 2)}/${zfill(
		date.getUTCDate(),
		2
	)}${suffix}`;
};

export const inputToPath = (input: string) => {
	return '/' + input.replace(/^(\d{4})-([01]\d)-([0-3]\d)$/, '$1/$2/$3');
};

export const pathToIsoDate = (path: string) => {
	const split = path.split(/^(?:.*\/)(\d{4})-(\d{2})-(\d{2})(?:.*)$/);
	return `${split[1]}-${zfill(split[2], 2)}-${zfill(split[3], 2)}`;
};

export const dateForInput = (date: Date) => {
	return `${date.getUTCFullYear()}-${zfill(date.getUTCMonth() + 1, 2)}-${zfill(
		date.getUTCDate(),
		2
	)}`;
};
