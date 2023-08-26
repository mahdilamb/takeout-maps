import { dateToPath } from '$lib/dates/formatting';
import { redirect } from '@sveltejs/kit';

export const load = () => {
	/**
	 * Redirect to today if at the index.
	 */
	throw redirect(302, dateToPath(new Date(), '/explore'));
};
