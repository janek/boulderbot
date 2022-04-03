<script>
	import * as jsonInfo from '/Users/janek/Developer/boulderbot/cache/all.json';
	const halls = ['Bouldergarten', 'Boulderklub', 'Der Kegel', 'Suedbloc'];

    let info = jsonInfo.default

	function hallInfoForToday(hall) {
        const today = new Date().toISOString().slice(0, 10);
		return hallInfoPerDay(hall, today);
	}

	function hallInfoPerDay(hall, day) {
		/* Convert JSON to presentable html-ish text.
  		 'Day' is formatted as 2022-02-18 */
        if (!(hall in info)) {
            return "No info for " + hall;
        }

        const infoPerDay = info[hall][day];
		if (!infoPerDay || infoPerDay.length === 0) {
			return 'No slots available';
		}

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

    function refresh() {
        // const fetchJSON = fetch('http://localhost:8001/all.json')
        //      .then((res) => res.json())
        //      .then((data) => {
        //         info = data;
        //         console.log(info[halls[2]]["2022-02-19"][0]["start_time"]);
        //      });
    }
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<section>
    <button on:click={refresh}>Refresh</button>
	{#each halls as hall}
		<h1>{hall}</h1>
		<p>{@html hallInfoForToday(hall)}</p>
	{/each}
</section>
