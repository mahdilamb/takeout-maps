import { dateFrom, inDate } from '$lib/dates/utils';
import type { Categorical, Dataset, Layer, Linear, Metadata } from '$lib/shared';
import interpolate from 'color-interpolate';

export type Sampler = (time: Date) => string;
type Entry<T = unknown> = {
	t: number;
	value: T;
};
const follow = (path: string, obj: any) => {
	return path.split('.').reduce((out, el) => out[el], obj);
};
const calcMin = <T extends number>(
	dmin: string | number,
	samples: Entry<T>[],
	metadata: Metadata
) => {
	if (typeof dmin === 'string') {
		return follow(dmin, metadata);
	}
	if (dmin !== undefined && dmin !== null) {
		return dmin;
	}

	return Math.min(...samples.map((sample) => sample.value));
};
const calcMax = <T extends number>(
	dmax: string | number,
	samples: Entry<T>[],
	metadata: Metadata
) => {
	if (typeof dmax === 'string') {
		return follow(dmax, metadata);
	}
	if (dmax !== undefined && dmax !== null) {
		return dmax;
	}
	return Math.max(...samples.map((sample) => sample.value));
};
export const createSampler = (layer: Layer, dataset: Dataset, date: Date): Sampler => {
	let colorMapper: (at: number, t: number) => string;
	let samples: Entry[];
	if (layer.color_by) {
		samples = dataset.data.map((el) => {
			return {
				t: inDate(date, dateFrom(el.start)),
				value: el[layer.color_by]
			};
		});

		if (Array.isArray(layer.color_map)) {
			const colormaps = (layer.color_map as Linear[]).map((cmap) => {
				return {
					dmin: calcMin(cmap.dmin, samples, dataset.metadata),
					dmax: calcMax(cmap.dmax, samples, dataset.metadata),
					interpolator: interpolate([cmap.min, cmap.max])
				};
			});

			colorMapper = (at: number, t: number) => {
				const sample = samples[at];
				const colormap = colormaps.find(
					(cmap) => sample.value >= cmap.dmin && sample.value <= cmap.dmax
				);
				if (colormap.dmax === colormap.dmin) {
					return layer.color;
				}
				return colormap.interpolator(
					(sample.value - colormap.dmin) / colormap.dmax - colormap.dmin
				);
			};
		} else if (
			Object.hasOwn(layer.color_map, 'dmin') &&
			Object.hasOwn(layer.color_map, 'dmax') &&
			Object.hasOwn(layer.color_map, 'min') &&
			Object.hasOwn(layer.color_map, 'max')
		) {
			const dmin = calcMin(layer.color_map.dmin, samples, dataset.metadata);
			const dmax = calcMax(layer.color_map.dmax, samples, dataset.metadata);
			const colormap = interpolate([layer.color_map.min, layer.color_map.max]);
			const range = dmax - dmin;
			colorMapper = (at: number, t: number) => {
				if (!range) {
					return layer.color;
				}
				const sample = samples[at];
				return colormap((sample.value - dmin) / range);
			};
		} else if (layer.color_map.color_map) {
			colorMapper = (at: number, t: number) => {
				const sample = samples[at];
				return (layer.color_map as Categorical).color_map[sample.value];
			};
		} else {
			throw `Front end does not currently support the ${JSON.stringify(layer.color_map)} type.`;
		}
	}
	return (time: Date) => {
		if (samples?.length) {
			const t = (time - date) / 8.64e7;
			if (t <= samples[0].t) {
				return layer.color;
			}
			const prevI = Math.max(
				0,
				samples.findIndex((el) => el.t >= t)
			);
			return colorMapper(prevI, t);
		}
		return layer.color;
	};
};
