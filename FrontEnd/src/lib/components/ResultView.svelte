<script lang="ts">
    import type { OptimizationResponse } from '$lib/types';
    import { Badge } from 'flowbite-svelte';
    import GameCalender from '$lib/components/GameCalender.svelte';
    export let results: OptimizationResponse;
    let start_date = new Date(results.start_date);
    let end_date = new Date(results.end_date);
    let games = results.games;
</script>

<div class="flex flex-col gap-5"> 


<p>Status: {results.solver_status}</p>
<p>Total Cost: {results.cost / 100}€</p>
<h2 class="text-xl font-semibold">Used subscriptions</h2>
<div class="flex flex-col gap-2">

{#each results.packages as subscription}
    <div class="flex flex-row gap-2">
        <Badge color="primary">{subscription.package.name}</Badge>
        {#if subscription.price <= 0}
            <span>Free 🤩</span>
        {:else}
            <span>{subscription.price / 100}€</span>{subscription.yearly == 1 ? '/ year' : '/ month'}
        {/if}
    </div>
{/each}
</div>

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
