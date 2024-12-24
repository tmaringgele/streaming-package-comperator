<script lang="ts">
    import type { OptimizationResponse } from '$lib/types';
    import { Badge } from 'flowbite-svelte';
    import GameCalender from '$lib/components/GameCalender.svelte';
    import { Section, Schedule, ScheduleItem } from "flowbite-svelte-blocks";

    export let results: OptimizationResponse;
    let start_date = new Date(results.start_date);
    let end_date = new Date(results.end_date);
    let games = results.games;

    function calculateDependentGames(subscription, games) {
        let dependentGames = games.filter(game =>  
            !game.covered_by.some(pkg => pkg.id != subscription.package.id)
        ); // a game is dependent from a package, if there is no other package covering it
        
        return dependentGames.length;
    }

    const schedule = [
  {
    time: "08:00 - 09:00",
    href: "/",
    title: "Opening remarks"
  },
  {
    time: "09:00 - 10:00",
    href: "/",
    title: "Bergside LLC: Controlling the video traffic flows"
  },
  {
    time: "10:00 - 11:00",
    href: "/",
    title: "Flowbite - An Open Framework for Forensic Watermarking"
  },
  {
    time: "11:00 - 12:00",
    href: "/",
    title: "Coffee Break"
  },
  {
    time: "12:00 - 13:00",
    href: "/",
    title: "Scaling your brand from \u20AC0 to multimillion euros"
  },
  {
    time: "13:00 - 14:00",
    href: "/",
    title: "Updates from the Open Source Multimedia community"
  },
  {
    time: "14:00 - 15:00",
    href: "/",
    title: "Exploring the balance between customer acquisition and retention"
  }
];
</script>

<div class="flex flex-col gap-5"> 


<p>Status: {results.solver_status}</p>
<p>Total Cost: {results.cost / 100}€ {results.live_value == 1 && results.ignored_games > 0 ? '(not including '+results.ignored_games+' non-live games)' : ''}</p>
<h2 class="text-xl font-semibold">Used subscriptions</h2>
<div class="flex flex-col gap-2">

{#each results.packages as subscription}
    <div class="flex flex-row gap-2">
        <Badge color="primary">{subscription.package.name}</Badge>
        {#if subscription.price <= 0}
            <span>Free 🤩</span>
        {:else}
        {#if subscription.yearly == 1}
            <span>{(subscription.price / 100).toFixed(2)}€ / year</span>
        {:else}
            <span>{(subscription.price / 100).toFixed(2)}€ / month</span>
        {/if}
            Remove this subscription and lose {calculateDependentGames(subscription, results.games)} games
        {/if}
    </div>
{/each}
</div>

<Section name="schedule" sectionClass="bg-white dark:bg-gray-900 antialiased">
    <Schedule scheduleName="Action Plan">
      <div class="mt-4" slot="subtitle">
      </div>
      {#each schedule as item}
        <ScheduleItem {item} />
      {/each}
    </Schedule>
  </Section>

<h2 class="text-xl font-semibold">Available Games</h2>
<GameCalender {start_date} {end_date}  {games}/>
</div>
<!-- <div class="mt-10">
    <h2 class="text-xl font-semibold">Optimization Results</h2>
    <p>Status: {results.solver_status}</p>
    <p>Total Cost: {results.cost}</p>
    <h3 class="mt-4 text-lg font-semibold">Filtered Games</h3>
    <ul>
        {#each results.games as game}
            <li>
                {game.team_home} vs {game.team_away} on {game.starts_at} - Covered by: {game.covered_by.map(pkg => pkg.name).join(', ')}
            </li>
        {/each}
    </ul>
</div> -->
