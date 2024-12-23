<script lang="ts">
    export let results: any;
</script>

<div class="mt-10">
    <h2 class="text-xl font-semibold">Optimization Results</h2>
    <p>Status: {results.optimization_results.status}</p>
    <p>Total Cost: {results.optimization_results.total_cost}</p>
    <h3 class="mt-4 text-lg font-semibold">Filtered Games</h3>
    <ul>
        {#each results.filtered_games as game}
            <li>
                {game.team_home} vs {game.team_away} on {game.starts_at} - Covered by: {game.covered_by.join(', ')}
            </li>
        {/each}
    </ul>
</div>
