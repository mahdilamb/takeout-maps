import type { Location } from '$lib/shared.js';
import { dateFrom } from './utils';
import { clip } from '$lib/utils';

export type LocationData = Omit<Location, 'timestamp'> & { timestamp: Date };
export const clipAndSort = (
	data: Location[],
	clipDate: Date | undefined = undefined,
	sortByDate = true
): LocationData[] => {
	/**
	 * Flatten the data and perform other ETL tasks.
	 */
	let output: LocationData[] = data.map((row) => {
		return { ...row, timestamp: dateFrom(row.timestamp) };
	});
	if (sortByDate) {
		return output.sort((a, b) => a.timestamp - b.timestamp);
	}
	if (clipDate !== undefined) {
		const nextDate = new Date(clipDate);
		nextDate.setUTCDate(nextDate.getUTCDate() + 1);
		const from = clipDate.getTime(),
			to = nextDate.getTime();
		const a = new Date(),
			b = new Date();
		a.setTime(from);
		b.setTime(to);
		const clipper = (val: Date) => {
			const result = new Date();
			result.setTime(clip(val, from, to));
			return result;
		};
		output = output.map((el) => {
			return { ...el, timestamp: clipper(el.timestamp) };
		});
	}

	return output;
};
