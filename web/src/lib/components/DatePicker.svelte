<script lang="ts">
	import { goto } from '$app/navigation';
	import { dateForInput, dateToPath } from '$lib/dates/formatting';

	export let data;
</script>

<input
	type="date"
	pattern="\d{4}-\d{2}-\d{2}"
	min={dateForInput(data.minDate)}
	max={dateForInput(data.maxDate)}
	value={dateForInput(data.currentDate)}
	on:input={(e) => {
		const selectedDate = new Date(e.target.value);
		if (selectedDate < data.minDate || selectedDate > data.maxDate) {
			return;
		}
		goto(dateToPath(selectedDate, '/explore'), { keepFocus: true });
	}}
/>
