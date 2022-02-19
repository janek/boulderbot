<script>
	const halls = ['Bouldergarten', 'Boulderklub', 'Der Kegel', 'Suedbloc'];
	// TODO: enable TS and define JSON schema?
	import * as jsonInfo from '/Users/janek/Developer/boulderbot/cache/all.json';
	const today = new Date().toISOString().slice(0, 10);
	console.log(jsonInfo.default[halls[2]][today]);

	console.log(hallInfoForToday(halls[2]));

	function hallInfoForToday(hall) {
		const today = new Date().toISOString().slice(0, 10);
		return hallInfoPerDay(hall, today);
	}

	function hallInfoPerDay(hall, day) {
		console.log(`Getting info for ${hall}, ${day}`);
		const infoPerDay = jsonInfo.default[hall][day];
		console.log(infoPerDay);
		console.log(typeof infoPerDay);
		console.log(infoPerDay.length);
		console.log('\n');
		if (infoPerDay.length === 0) {
			return 'No slots available';
		}
		// 'day' formatted as 2022-02-18
		return infoPerDay.reduce(
			(outputHTML, slotInformation) =>
				outputHTML +
				slotInformation.start_time +
				' - ' +
				slotInformation.end_time +
				' → ' +
				String(slotInformation.free_places).padStart(2, '\u00A0') +
				' places ' +
				'<br/>',
			''
		);
	}
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<section>
	{#each halls as hall}
		<h1>{hall}</h1>
		<p>{@html hallInfoForToday(hall)}</p>
	{/each}
</section>
