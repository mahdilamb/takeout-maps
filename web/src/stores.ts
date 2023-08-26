import axios from 'axios';
import { derived, readable, writable } from 'svelte/store';
import { BACKEND } from './app';
import type { Connection } from '$lib/shared';

export const connections = writable<Connection[]>(undefined);
export const selectedLayer = writable<string>('None');

(async () => {
	await axios.get<Connection[]>(`${BACKEND}/connections`).then((resp) => {
		connections.set(resp.data);
	});
})();
