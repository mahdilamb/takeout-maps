<script lang="ts">
	import { goto } from '$app/navigation';
	import { dateToPath } from '$lib/dates/formatting';

	import DatePicker from './DatePicker.svelte';
	import Timeline from './Timeline.svelte';

	export let data;
	export let map;
	const back = (e: MouseEvent) => {
		goto(
			dateToPath(
				new Date(new Date(data.currentDate).setUTCDate(data.currentDate.getUTCDate() - 1)),
				'/explore'
			),
			{ keepFocus: true, replaceState: false }
		);
	};
	const next = (e: MouseEvent) => {
		goto(
			dateToPath(
				new Date(new Date(data.currentDate).setUTCDate(data.currentDate.getUTCDate() + 1)),
				'/explore'
			),
			{ keepFocus: true, replaceState: false }
		);
	};
</script>

<DatePicker {data} />
<div class="overview">
	<a href="#" class="back" on:click|stopPropagation|preventDefault={back}>&#8592;</a>
	<Timeline {data} {map} />
	<a href="#" on:click|stopPropagation|preventDefault={next} class="next">&#8594;</a>
</div>

<style>
	.overview {
		display: flex;
		flex-direction: row;
		width: 100%;
	}
</style>
