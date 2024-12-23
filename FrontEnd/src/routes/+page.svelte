<script lang="ts">
    import { slide } from 'svelte/transition';
    import { Search, Button } from 'flowbite-svelte';
    import { Dropdown, DropdownItem, Badge } from 'flowbite-svelte';
    import { Datepicker, P } from 'flowbite-svelte';
    import { Range, Label } from 'flowbite-svelte';
    import {
        SearchOutline,
        CalendarEditOutline,
        ChevronDownOutline,
        PlusOutline,
        ExclamationCircleSolid
    } from 'flowbite-svelte-icons';
    import { onMount } from 'svelte';
    import Typewriter from 'svelte-typewriter';
    import { Slider } from 'bits-ui';
    import { get } from 'svelte/store';
    import { Toast } from 'flowbite-svelte';
    import all_clubs from '$lib/all_clubs.json';
    import { fetch } from 'whatwg-fetch';
    import ResultView from '$lib/components/ResultView.svelte';

    let liveValue = [10];
    let highlightValue = [20];
    let displayClubNotFound: string | false = '';
    let searchQuery = '';
    let dateRange = { from: null, to: null };
    let selectedClubs: string[] = [];
    let clubs = all_clubs;
    let results = null;

    const badgeColors = ['dark', 'red', 'green', 'yellow', 'indigo', 'purple', 'pink'];

    function getRandomColor() {
        return badgeColors[Math.floor(Math.random() * badgeColors.length)];
    }

    function getLiveValueStatement(liveValue: number[]): string {
        if (liveValue[0] <= 0) {
            return 'Not at all.';
        } else if (liveValue[0] <= 30) {
            return 'A little bit.';
        } else if (liveValue[0] < 70) {
            return 'I do care.';
        } else if (liveValue[0] < 100) {
            return 'I care A LOT! 🍿';
        }else {
            return 'MUST. HAVE. 🤯';
        }
    }

    function handleSearch() {
        console.log('Searching for:', searchQuery, selectedTournament, dateRange);
        // Make API call with searchQuery, selectedTournament, and dateRange
    }

    function addClub() {
        if (clubs.includes(searchQuery) && !selectedClubs.includes(searchQuery)) {
            selectedClubs = [...selectedClubs, searchQuery];
            searchQuery = '';
            displayClubNotFound = false;
        } else if (selectedClubs.includes(searchQuery)) {
            displayClubNotFound = 'Club is already selected.';
            setTimeout(() => {
                displayClubNotFound = '';
            }, 3000);
        } else {
            displayClubNotFound = 'Club is not in our list.';
            setTimeout(() => {
                displayClubNotFound = false;
            }, 3000);
        }
    }

    async function findPackage() {
        const response = await fetch('http://127.0.0.1:5000/optimizePackages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                clubs: selectedClubs,
                timespan: {
                    start_date: dateRange.from,
                    end_date: dateRange.to
                },
                live_value: liveValue[0],
                highlight_value: highlightValue[0]
            })
        });
        results = await response.json();
    }
</script>

{#if results == null}
<div class="bg-primary-800 bg-gradient-to-tr from-primary-800 to-primary-600 flex h-screen overflow-y-auto  items-center justify-center">
    <div class="w-full max-w-3xl rounded-lg bg-gray-50 p-4 shadow-lg relative">
        <Typewriter delay={500} keepCursorOnFinish={1000}>
            <h1 class="mb-4 text-center text-3xl font-semibold">Welcome! ⚽</h1>
        </Typewriter>
        <Typewriter delay={2000} keepCursorOnFinish={3000}>
            <p class="text-center text-gray-600">Let's find your optimal streaming package</p>
        </Typewriter>
        <Typewriter delay={6000} keepCursorOnFinish={1000}>
            <p class="mb-4 text-center text-xs text-gray-600">
                (With the help of ✨Integer Programming✨)
            </p>
        </Typewriter>
        <h2 class="mb-4 mt-4 text-center text-xl font-semibold">
            Which clubs are you interested in? 🏟️
        </h2>
        <div class="mb-3 flex flex-wrap gap-2">
            {#each selectedClubs as club}
                <Badge dismissable large color={getRandomColor()} on:close={() => {
                    selectedClubs = selectedClubs.filter(selectedClub => selectedClub !== club);
                }}>{club}</Badge>
            {/each}
        </div>
        <div class="relative">
            <Search
                placeholder="Bayern München, FC Barcelona, ..."
                bind:value={searchQuery}
                on:search={handleSearch}
            >
                <Button class="mx-3 gap-1" on:click={addClub}><PlusOutline /> Add</Button>
            </Search>
            {#if searchQuery}
                <ul class="mt-2 bg-white border border-gray-300 rounded-lg shadow-lg absolute w-full z-10">
                    {#each clubs.filter(club => club.toLowerCase().includes(searchQuery.toLowerCase()) && !selectedClubs.includes(club)).slice(0, 5) as club}
                        <li class="p-2 hover:bg-gray-200 cursor-pointer " on:click={() => searchQuery = club}>
                            {club}
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>
        <div class="mt-8 flex flex-row gap-8">
            <div class="flex flex-col gap-3 grow">
                <Label class="text-md">Looking for a specific timespan?</Label>
                <Datepicker range bind:rangeFrom={dateRange.from} bind:rangeTo={dateRange.to} 
                dateFormat={
                    {
                        day: 'numeric',
                        month: 'numeric',
                        year: 'numeric'
                    }
                }
                />
            </div>
            <div class="flex flex-col gap-8">
                <div class=" flex grow flex-col gap-3">
                    <Label class="text-md">How much do you care about live?</Label>
                    <div class="flex flex-row gap-4">
                        <Slider.Root
                            bind:value={liveValue}
                            let:thumbs
                            class="relative flex w-full touch-none select-none items-center"
                        >
                            <span class="bg-dark-10 relative h-2 w-full grow overflow-hidden rounded-full">
                                <Slider.Range class="bg-primary absolute h-full" />
                            </span>
                            {#each thumbs as thumb}
                                <Slider.Thumb
                                    {thumb}
                                    class="border-border-input bg-primary-600 hover:border-dark-40 focus-visible:ring-foreground active:scale-98 dark:bg-foreground dark:shadow-card block  size-[25px] cursor-pointer rounded-full border shadow transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
                                />
                            {/each}
                        </Slider.Root>
                        <p class="min-w-32 text-sm">{getLiveValueStatement(liveValue)}</p>
                    </div>
                </div>
                <div class=" flex grow flex-col gap-3">
                    <Label class="text-md">How much do you care about highlights?</Label>
                    <div class="flex flex-row gap-4">
                        <Slider.Root
                            bind:value={highlightValue}
                            let:thumbs
                            class="relative flex w-full touch-none select-none items-center"
                        >
                            <span class="bg-dark-10 relative h-2 w-full grow overflow-hidden rounded-full">
                                <Slider.Range class="bg-primary absolute h-full" />
                            </span>
                            {#each thumbs as thumb}
                                <Slider.Thumb
                                    {thumb}
                                    class="border-border-input bg-primary-600 hover:border-dark-40 focus-visible:ring-foreground active:scale-98 dark:bg-foreground dark:shadow-card block  size-[25px] cursor-pointer rounded-full border shadow transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
                                />
                            {/each}
                        </Slider.Root>
                        <p class="min-w-32 text-sm">{getLiveValueStatement(highlightValue)}</p>
                    </div>
                </div>
            </div>
        </div>

        <Button class="mt-10 w-full mb-2" color="primary" size="lg" on:click={findPackage}>Find my package</Button>
        <p class="text-center underline-offset-3 underline text-gray-600 cursor-pointer">or choose specific games</p>
    </div>
</div>

<Toast color="red" position="bottom-right" transition={slide} toastStatus={displayClubNotFound}
divClass="w-full max-w-xs p-4 text-gray-500 bg-white shadow dark:text-gray-400 dark:bg-gray-800 gap-3">
    <svelte:fragment slot="icon">
      <ExclamationCircleSolid class="w-5 h-5" />
      <span class="sr-only">Warning icon</span>
    </svelte:fragment>
    {displayClubNotFound}
</Toast>

{:else}
<Button class="mt-10 w-full mb-2" color="primary" size="lg" on:click={() => results = null}>Go back</Button>
<ResultView {results} />
{/if}