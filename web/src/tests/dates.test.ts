import { clipAndSort } from '$lib/dates/etl';
import { dateFrom } from '$lib/dates/utils';
import type { Data } from '$lib/shared';
import { test, expect } from 'vitest';

const randomLatLng = (): [number, number] => {
	return [Math.random() * 180 - 90, Math.random() * 180 - 90];
};
test('Data from UTC=0', () => {
	const [lat, lng] = randomLatLng();
	const data: Data = [
		{
			waypoints: [
				{
					latitude: lat,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2020-11-30T22:35:06.248000Z'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 14,
					accuracy: 14,
					timestamp: '2020-12-01T22:38:46.552000Z'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 20,
					accuracy: 20,
					timestamp: '2020-12-01T22:39:48.304000Z'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 59,
					accuracy: 59,
					timestamp: '2020-12-01T22:40:08.046000Z'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 16,
					accuracy: 16,
					timestamp: '2020-12-01T23:09:38.525000Z'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 18,
					accuracy: 18,
					timestamp: '2020-12-01T23:10:03.267000Z'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2020-12-01T23:10:21.625000Z'
				}
			],
			type: 'WALKING'
		}
	];
	const clipDate = new Date(Date.UTC(2020, 12 - 1, 1));
	const result = clipAndSort(data, clipDate);
	expect(result[0][1]).toStrictEqual(clipDate);
	expect(result[0]).toHaveLength(5);
});

test('Data from UTC=+1', () => {
	const [lat, lng] = randomLatLng();
	const data: Data = [
		{
			waypoints: [
				{
					latitude: lng,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2021-07-11T20:51:43.197000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2021-07-11T20:52:09.753000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2021-07-11T20:54:39.087000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 13,
					accuracy: 13,
					timestamp: '2021-07-11T20:56:38.825000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 13,
					accuracy: 13,
					timestamp: '2021-07-11T20:59:13.489000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 13,
					accuracy: 13,
					timestamp: '2021-07-11T21:01:17.872000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 13,
					accuracy: 13,
					timestamp: '2021-07-11T21:01:33.126000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 13,
					accuracy: 13,
					timestamp: '2021-07-11T21:05:00.283000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 13,
					accuracy: 13,
					timestamp: '2021-07-11T21:07:23.768000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2021-07-11T21:09:32.911000+01:00'
				},
				{
					latitude: lng,
					longitude: lng,
					altitude: 12,
					accuracy: 12,
					timestamp: '2021-07-11T21:11:33.414000+01:00'
				}
			]
		}
	];
	const result = clipAndSort(data, new Date(Date.UTC(2021, 7 - 1, 11)));
	expect(result[0]).toHaveLength(5);
});

test('Dates stay the same after import [Summer]', () => {
	expect(dateFrom('2021-07-11T20:51:43.197000Z').getUTCHours()).toStrictEqual(20);
});

test('Dates stay the same after import [Winter]', () => {
	expect(dateFrom('2021-02-11T20:51:43.197000Z').getUTCHours()).toStrictEqual(20);
});

test('Dates stay the same after import [Summer], timezone specified', () => {
	expect(dateFrom('2021-07-11T20:51:43.197000+03:00').getUTCHours()).toStrictEqual(20);
});

test('Dates stay the same after import [Winter], timezone specified', () => {
	expect(dateFrom('2021-02-11T20:51:43.197000+03:00').getUTCHours()).toStrictEqual(20);
});
