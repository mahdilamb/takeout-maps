export const dateFrom = (iso8601: string, ignoreTimezone = true): Date => {
	if (ignoreTimezone) {
		iso8601 = iso8601.replace(/^(.*?)(?:Z|([+0]\d{2}:\d{2}))$/, `$1Z`);
	}
	return new Date(iso8601);
};

export const resetTime = (date: Date) => {
	date.setUTCHours(0);
	date.setUTCMinutes(0);
	date.setUTCSeconds(0);
	date.setUTCMilliseconds(0);
	return date;
};

export const nextDate = (date: Date): Date => {
	const result = new Date(date);
	result.setUTCDate(result.getUTCDate() + 1);
	return result;
};

export const inDate = (from: Date, date: Date) => {
	return (date - from) / 8.64e7;
};
