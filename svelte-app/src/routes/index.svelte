<script>
	import * as jsonInfo from '/Users/janek/Developer/boulderbot/cache/Boulderklub.json';
	console.log(jsonInfo);

	function jsonGymInfoToText(info) {
		return info
			.filter((slotInformation) => slotInformation.free_places != 0)
			.reduce(
				(outputHTML, slotInformation) =>
					outputHTML +
					slotInformation.start_time +
					' - ' +
					slotInformation.end_time +
					' → ' +
					slotInformation.free_places +
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
	<h1>Boulderklub</h1>
	<div>{@html jsonGymInfoToText(jsonInfo.default)}</div>
</section>
