<script lang="ts">
	import axios from 'axios';
	import { BACKEND } from '../../app';
	import type { Connection } from '$lib/shared';
	import { connections } from '../../stores';

	let data: Connection[];
	connections.subscribe((value) => {
		data = value;
	});
	const imgHeight = 24;
</script>

{#if data === undefined}
	Loading...
{:else}
	<div class="connections">
		{#if data.filter((connection) => connection.connected === false).length}
			{#each data as connection, connectionIndex}
				{#if connection.connected === false}
					<a
						href="#"
						on:click|preventDefault|stopPropagation={() => {
							const popup = window.open(connection.url, connection.name);
							popup.onunload = async () => {
								await axios.get(`${BACKEND}${connection.path}/connection`).then((resp) => {
									data[connectionIndex] = resp.data;
									connections.set([...data]);
								});
							};
						}}
						style="height:{imgHeight}px;"
						><img
							height="{imgHeight}px"
							alt={connection.name}
							src="{BACKEND}{connection.icon}"
						/></a
					>
				{/if}
			{/each}
		{/if}
	</div>
{/if}

<style>
	.connections a {
		width: auto;
		padding: 2px;
	}
</style>
