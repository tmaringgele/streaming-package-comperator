<script lang="ts">
    // Import required types and components
    import type { Game } from '$lib/types'; // Type definition for Game objects
    import { Popover, Button, Badge } from 'flowbite-svelte'; // UI components
    import liveicon from '$lib/assets/live-icon.png'; // Icon for live games
    import liveiconmini from '$lib/assets/live-icon-mini.png'; // Mini icon for live games
    import highlighticon from '$lib/assets/highlight-icon.png'; // Icon for game highlights
    import { getRandomColor } from '$lib/functions'; // Utility for random colors

    // Props received from parent component
    export let start_date: Date; // Start date of the range
    export let end_date: Date; // End date of the range
    export let games: Game[]; // List of games to display

    // Local state variables
    let years: number[] = []; // List of years in the selected range
    const months: string[] = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]; // Names of months for display
    let gamesByYearMonth: { [key: string]: Game[] } = {}; // Games organized by year and month

    // Reactive statement to calculate years and organize games by year and month
    $: if (start_date && end_date) {
        // Calculate years within the start and end dates
        let startYear = start_date.getFullYear();
        let endYear = end_date.getFullYear();
        years = [];
        for (let year = startYear; year <= endYear; year++) {
            years.push(year);
        }

        // Organize games by "year-month" keys
        gamesByYearMonth = {}; // Reset gamesByYearMonth
        games.forEach(game => {
            let gameDate = new Date(game.starts_at); // Parse the game date
            let yearMonth = `${gameDate.getFullYear()}-${gameDate.getMonth()}`; // Create a "year-month" key
            if (!gamesByYearMonth[yearMonth]) {
                gamesByYearMonth[yearMonth] = []; // Initialize array if key doesn't exist
            }
            gamesByYearMonth[yearMonth].push(game); // Add game to the corresponding year-month bucket
        });
    }
</script>


{#if start_date && end_date}
    <table class="table-auto w-full border-collapse">
        <thead>
            <tr>
                <th class="border-r">Year</th>
                {#each months as month}
                    <th class="border-r">{month}</th>
                {/each}
            </tr>
        </thead>
        <tbody>
            {#each years as year}
                <tr class="border-b">
                    <td class="border-r font-semibold">{year}</td>
                    {#each months as month, index}
                        <td class="border-r">
                            <ul>
                            {#each gamesByYearMonth[`${year}-${index}`] as game, gameIndex}
                                <li class=" cursor-crosshair"
                                id="game-{year}-{index}-{gameIndex}">
                                <Badge color={getRandomColor()} class="mr-2 gap-2">
                                
                                <p>{new Date(game.starts_at).getDate()}. {month}</p> 
                                {#if game.covered_by.filter(p => p.live == 1).length > 0}
                                    <img src={liveiconmini} alt="Live Icon" class="h-3"/>
                                {/if}
                                </Badge>
                            </li>
                                <Popover class="w-64 text-sm font-light" title="{new Date(game.starts_at).toDateString()}" triggeredBy={`#game-${year}-${index}-${gameIndex}`}>
                                    <div class=" font-bold">{game.team_home} vs {game.team_away}</div>
                                    <div>Watch on: 
                                        <ul class="list-inside">
                                            {#each [...new Map(game.covered_by.map(p => [p.id, p])).values()] as p}
                                                <li class="flex flex-row gap-1">📺 {p.name} 
                                                    {#if p.live}
                                                        <img src={liveicon} alt="Live Icon" class="h-4 inline-block"/>
                                                    {/if}
                                                    {#if p.highlights}
                                                        <img src={highlighticon} alt="Live Icon" class="h-4 inline-block"/>
                                                    {/if}
                                                </li>
                                            {/each}
                                        </ul>

                                    </div>
                                </Popover>
                            {/each}
                            </ul>
                        </td>
                    {/each}
                </tr>
            {/each}
        </tbody>
    </table>
{/if}

