import type { Segment } from './datasets/polyline';
import type { Sampler } from './datasets/sampler';
import type { LocationData } from './dates/etl';
import type { Layer } from './shared';

export type ExploreData = {
	/**
	 * Interface for the main data that is shared throughout the explore section
	 */
	locations: LocationData[];
	currentDate: Date;
	minDate: Date;
	maxDate: Date;
};
export type MapExtended = {
	destroy: () => void;
	clearDay: () => MapExtended;
	addDay: (data: ExploreData) => MapExtended;
	addBaseLayer: (layerKey: string, layer: Layer, segments: Segment[], sampler: Sampler) => void;
	hasBaseLayer: (layer: string) => boolean;
	getSegments: (layerKey: string) => Segment[];
	resetView: () => void;
};
