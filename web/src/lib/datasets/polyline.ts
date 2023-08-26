import type { LocationData } from '$lib/dates/etl';

import type { Sampler } from './sampler';

export type Segment = {
	coordinates: [number, number][];
	color: string;
	start: Date;
	end: Date;
};

export const createSegments = (
	locations: LocationData[],
	sampler: Sampler
): [Segment[], Sampler] => {
	const colors = locations.map((location) => sampler(location.timestamp));
	let segments: number[][] = [[]];
	let last: string;
	colors.forEach((c, i) => {
		if (c !== last) {
			if (i) {
				segments.push([i - 1, i]);
			}
			segments.push([i]);
			last = c;
		} else {
			segments[segments.length - 1].push(i);
		}
	});

	segments = segments.filter((seg) => seg.length);
	return [
		segments.map((ii) => {
			return {
				start: locations[ii[0]].timestamp,
				end: locations[ii[ii.length - 1]].timestamp,
				color: colors[ii[0]],
				coordinates: ii.map((i) => [locations[i].latitude, locations[i].longitude])
			};
		}),
		sampler
	];
};
