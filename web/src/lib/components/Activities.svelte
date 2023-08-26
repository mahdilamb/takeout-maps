<script lang="ts">
	import type { Event } from '$lib/shared';
	export let activity: Event;
	export let previousActivity: Event | undefined;

	const startOfDay = (date: Date) => {
		const output = new Date();
		output.setTime(date.getTime());
		output.setHours(0);
		output.setMinutes(0);
		output.setSeconds(0);
		output.setMilliseconds(0);
		return output;
	};
	const timestampRange = (event: Event): [Date, Date] => {
		const timestamps: Date[] = event.waypoints.map((a) => new Date(a.timestamp));
		timestamps.sort();
		return [timestamps[0], timestamps[timestamps.length - 1]];
	};
	const [start, end] = timestampRange(activity);
	const duration = (end - start) / 86_400_000;
	const paddingFrom = previousActivity ? timestampRange(previousActivity)[1] : startOfDay(start);
	const padding = Math.round(((start - paddingFrom) / 86_400_000) * 100);
	const percent = Math.round(duration * 100);
</script>

<div
	class="breadcrumb"
	style={`margin-left: ${padding}%;width:${percent}%; background: ${ActivityColors[activity.type]}`}
/>

<style>
	.breadcrumb {
		height: 100%;
		display: inline-block;
	}
</style>
