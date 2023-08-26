import { pad, zfill } from '$lib/utils';
import { expect, test } from 'vitest';

test('string padding works correctly for a simple string.', () => {
	return expect(zfill(2, 5)).toBe('00002');
});
