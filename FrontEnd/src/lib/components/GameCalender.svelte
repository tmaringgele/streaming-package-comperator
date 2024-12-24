<script lang="ts">
    import type { Game } from '$lib/types';
    import { Popover, Button, Badge } from 'flowbite-svelte';
    import liveicon from '$lib/assets/live-icon.png';
    import liveiconmini from '$lib/assets/live-icon-mini.png';
    import highlighticon from '$lib/assets/highlight-icon.png';
    export let start_date: Date;
    export let end_date: Date;
    export let games: Game[];

    let years: number[] = [];
    let months: string[] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let gamesByYearMonth: { [key: string]: Game[] } = {};

    const badgeColors = ['dark', 'red', 'green', 'yellow', 'indigo', 'purple', 'pink'];


    $: if (start_date && end_date) {
        let startYear = start_date.getFullYear();
        let endYear = end_date.getFullYear();
        years = [];
        for (let year = startYear; year <= endYear; year++) {
            years.push(year);
        }

        gamesByYearMonth = {};
        games.forEach(game => {
            let gameDate = new Date(game.starts_at);
            let yearMonth = `${gameDate.getFullYear()}-${gameDate.getMonth()}`;
            if (!gamesByYearMonth[yearMonth]) {
                gamesByYearMonth[yearMonth] = [];
            }
            gamesByYearMonth[yearMonth].push(game);
        });
    }
    console.log(games)
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
                    <td class="border-r">{year}</td>
                    {#each months as month, index}
                        <td class="border-r">
                            <ul>
                            {#each gamesByYearMonth[`${year}-${index}`] as game, gameIndex}
                                <li class=" cursor-crosshair"
                                id="game-{year}-{index}-{gameIndex}">
                                <Badge color={badgeColors[Math.floor(Math.random() * badgeColors.length)]} class="mr-2 gap-2">
                                
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

