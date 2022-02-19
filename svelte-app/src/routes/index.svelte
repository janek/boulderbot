<script>
	import * as jsonInfo from '/Users/janek/Developer/boulderbot/cache/all.json';
	const halls = ['Bouldergarten', 'Boulderklub', 'Der Kegel', 'Suedbloc'];

	function hallInfoForToday(hall) {
		const today = new Date().toISOString().slice(0, 10);
		return hallInfoPerDay(hall, today);
	}

	function hallInfoPerDay(hall, day) {
		/* Convert JSON to presentable html-ish text.
  		 'Day' is formatted as 2022-02-18 */
		const infoPerDay = jsonInfo.default[hall][day];
		if (infoPerDay.length === 0) {
			return 'No slots available';
		}

		// TODO: write a closure to process n (make 10+ and pad 3)
		const processFreePlaces = (n) => (n <= 10 ? String(n) : '10+').padStart(3, '\u00A0');

		return infoPerDay.reduce(
			(outputHTML, slotInformation) =>
				outputHTML +
				slotInformation.start_time +
				' - ' +
				slotInformation.end_time +
				' → ' +
				processFreePlaces(slotInformation.free_places) +
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
