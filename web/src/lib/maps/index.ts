import L from 'leaflet';
import * as TileLayers from '$lib/maps/layers';
import { Connections, TimelineControl, ZoomWithHome } from './controls';
import { selectedLayer } from '../../stores';
import type { ExploreData, MapExtended } from '$lib/common';
import type { Layer } from '$lib/shared';
import type { Segment } from '$lib/datasets/polyline';
import type { Sampler } from '$lib/datasets/sampler';

export type LeafletMap = L.Map & MapExtended;
type PrivateFields = {
	_movement: L.Layer | undefined;
	_additionalLayers: L.Control.Layers;
	_layerNames: Set<string>;
	_samplers: { [name: string]: Sampler };
	_segments: { [name: string]: Segment[] };
	_track: L.Polyline | undefined;
};
const EMPTY = L.polyline([]);
const initAdditionalLayers = () => {
	return L.control.layers({ None: EMPTY });
};
const wrapMap = (mapElement: HTMLElement): LeafletMap => {
	const map = L.map(mapElement, { zoomControl: false }) as LeafletMap & PrivateFields;

	map.clearDay = () => {
		map._additionalLayers?.remove();
		map._additionalLayers = initAdditionalLayers();
		map._additionalLayers.addTo(map);
		map._samplers = {};
		map._segments = {};
		map.getSegments = (layerKey: string) => map._segments[layerKey];
		map._layerNames = new Set();
		map.hasBaseLayer = (layerKey: string) => {
			return map._layerNames.has(layerKey);
		};
		map._movement?.remove();
		map._track?.remove();
		map.resetView = () => {
			return;
		};
		return map;
	};
	map.addDay = (data: ExploreData) => {
		if (typeof window === 'undefined') {
			console.log('Trying to update map before the window is available.');
			return map;
		}
		if (!data.locations.length) {
			map.locate({ setView: true, maxZoom: 16 });
			return map;
		}
		const points: L.LatLngExpression[] = data.locations.map((event) => [
			event.latitude,
			event.longitude
		]);
		const bounds = L.latLngBounds(points);
		map._track = L.polyline(points, { weight: 5 });
		map._track._layerKey = '/takeout/movement';
		map._additionalLayers.addBaseLayer(map._track, 'Movement');
		map._samplers['/takeout/movement'] = () => '#999';
		map._segments['/takeout/movement'] = [
			{
				coordinates: points,
				color: '#999',
				start: data.locations[0].timestamp,
				end: data.locations[data.locations.length - 1].timestamp
			}
		];
		map._track.addTo(map);
		map.resetView = () => map.fitBounds(bounds);
		map.resetView();
		return map;
	};
	map.addBaseLayer = (layerKey: string, layer: Layer, segments: Segment[], sampler: Sampler) => {
		const layerGroup = L.layerGroup(
			segments.map((segment) => {
				return L.polyline(segment.coordinates, { color: segment.color });
			})
		);
		layerGroup._layerKey = layerKey;
		map._additionalLayers.addBaseLayer(layerGroup, layer.label);
		map._layerNames.add(layerKey);
		map._samplers[layerKey] = sampler;
		map._segments[layerKey] = segments;
	};
	map.destroy = () => map.remove();
	return map.clearDay();
};
export const createMap = (
	mapElement: HTMLElement,
	timelineElement: HTMLDivElement,
	connectionsElement: HTMLDivElement
): LeafletMap => {
	if (typeof window === 'undefined') {
		throw 'Trying to update map before the window is available.';
	}
	const map = wrapMap(mapElement) as LeafletMap & PrivateFields;

	const timeline = new TimelineControl(timelineElement);
	timeline.getContainer()?.classList.add('timeline');

	map.addControl(timeline);

	map.addControl(new ZoomWithHome());
	map.addControl(
		L.control.layers({
			map: TileLayers.OpenStreetMap_Mapnik,
			satellite: TileLayers.Esri_WorldImagery
		})
	);
	map.addControl(map._additionalLayers);
	map.on('baselayerchange', function (e) {
		selectedLayer.set(e.layer._layerKey);
	});
	map.addControl(new Connections(connectionsElement));
	TileLayers.OpenStreetMap_Mapnik.addTo(map);
	EMPTY.addTo(map);
	return map;
};
