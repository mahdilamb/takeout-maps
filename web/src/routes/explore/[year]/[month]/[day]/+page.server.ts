import { error, redirect } from '@sveltejs/kit';
import axios from 'axios';
import { dateToPath, pathToIsoDate } from '$lib/dates/formatting.js';
import { dateFrom } from '$lib/dates/utils.js';
import { clipAndSort as sortAndClip } from '$lib/dates/etl.js';
import { BACKEND } from '../../../../../app';
import type { ExceptionDetail, LocationData } from '$lib/shared';
import type { ExploreData } from '$lib/common';

export const load = async ({
	params: urlParams
}: {
	params: Record<'year' | 'month' | 'day', string>;
}): Promise<ExploreData> => {
	/**
	 * Load the data for this page.
	 */
	const url = `/locations/${urlParams.year}-${urlParams.month}-${urlParams.day}.json`;
	const pageDate = await axios.get<LocationData>(`${BACKEND}${url}`).catch((resp) => {
		if ((resp.response.data.detail as ExceptionDetail).errorID === 'date-out-of-range') {
			throw redirect(302, dateToPath(dateFrom(resp.response.data.detail.end), '/explore'));
		}
	});
	if (!pageDate) {
		throw error(404);
	}
	return {
		locations: sortAndClip(pageDate.data.locations, dateFrom(pathToIsoDate(url))),
		currentDate: dateFrom(pathToIsoDate(url)),
		minDate: dateFrom(pageDate.data.start),
		maxDate: dateFrom(pageDate.data.end)
	};
};
