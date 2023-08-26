<script lang="ts">
	import type { Dataset } from '$lib/shared';
	import { onDestroy } from 'svelte';
	import '$lib/maps/timeline.css';
	import { page } from '$app/stores';

	import Connections from './Connections.svelte';
	import { connections, selectedLayer } from '../../stores';
	import { BACKEND } from '../../app';
	import axios from 'axios';
	import { createSegments } from '$lib/datasets/polyline';
	import { createSampler } from '$lib/datasets/sampler';
	import TimeBar from './TimelineNavigation.svelte';
	import type { ExploreData, MapExtended } from '$lib/common';

	export let data: ExploreData;
	export let map: MapExtended;
	let mapComponent: HTMLDivElement;
	let timelineComponent: HTMLDivElement;
	let connectionsElement: HTMLDivElement;
	const addLayersFromConnections = () => {
		const isoDate = $page.url.pathname.split(/[\//]/).slice(-3).join('-');
		$connections
			.filter((connection) => connection.connected !== false)
			.flatMap((connection) => {
				return connection.layers
					.filter((layer) => !map.hasBaseLayer(connection.path + layer.path))
					.map((layer) => {
						const layerKey = connection.path + layer.path;
						try {
							axios.get<Dataset>(BACKEND + layerKey + '/' + isoDate + '.json').then((resp) => {
								if (resp.status !== 200) {
									return;
								}
								map?.addBaseLayer(
									layerKey,
									layer,
									...createSegments(
										data.locations,
										createSampler(layer, resp.data, new Date(isoDate))
									)
								);
							});
						} catch (e) {
							console.error(e);
						}
					});
			});
	};
	const updateMap = async (data: ExploreData) => {
		if (typeof window === 'undefined') {
			return;
		}
		if (map === undefined || mapComponent._leaflet_id === undefined) {
			const L = await import('$lib/maps');
			map = L.createMap(mapComponent, timelineComponent, connectionsElement)
				.clearDay()
				.addDay(data);
		} else {
			map.clearDay().addDay(data);
		}
		addLayersFromConnections();

		return map;
	};

	onDestroy(() => {
		map?.destroy();
	});
	connections.subscribe((connections) => {
		if (connections === undefined || map === undefined) {
			return;
		}
		addLayersFromConnections();
	});
	$: updateMap(data).then((res) => (map = res));
</script>

<div class="map" bind:this={mapComponent} />
<div class="timeline" bind:this={timelineComponent}><TimeBar {data} {map} /></div>
<div bind:this={connectionsElement}><Connections /></div>

<style>
	.map {
		height: 100%;
		width: 100%;
	}
	.timeline {
		display: flex;
		width: 100%;
		flex-direction: row;
		height: 100%;
	}
</style>
