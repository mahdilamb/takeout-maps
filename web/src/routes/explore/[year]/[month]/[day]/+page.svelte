<script lang="ts">
	import type { ExploreData } from '$lib/common';
	import Map from '$lib/components/Map.svelte';
	export let data: ExploreData;
</script>

<main>
	<Map {data} />
</main>

<style>
	main {
		width: 100vw;
		height: 100vh;
	}
</style>
