<script lang="ts">
	import { selectedLayer } from '../../stores';
	import { inDate } from '$lib/dates/utils';
	import type { ExploreData, MapExtended } from '$lib/common';

	export let data: ExploreData;
	export let map: MapExtended;

	$: segments = map?.getSegments($selectedLayer);
</script>

{#if segments}
	<div class="breadcrumbs">
		{#each segments as segment}
			<div
				class="breadcrumb"
				style={`background:${segment.color}; left: ${
					inDate(data.currentDate, segment.start) * 100
				}%;width: ${
					(inDate(data.currentDate, segment.end) - inDate(data.currentDate, segment.start)) * 100
				}%`}
			/>
		{/each}
	</div>
{/if}

<style>
	.breadcrumbs {
		height: 20px;
		border-radius: 4px;
		position: relative;
		flex: 1;
	}
	.breadcrumb {
		height: 100%;
		display: inline-block;
	}
</style>
