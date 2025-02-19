<script lang="ts">
    // Environment variables and API constants
    import { PUBLIC_API_BASE } from '$env/static/public';
    
    // Svelte-specific imports
    import { slide } from 'svelte/transition';
    import { onMount } from 'svelte';

    // UI components from external libraries
    import { Search, Button, Dropdown, DropdownItem, Badge, Datepicker, Range, Label, Toast } from 'flowbite-svelte';
    import { SearchOutline, CalendarEditOutline, ChevronDownOutline, PlusOutline, ExclamationCircleSolid, ChevronLeftOutline, CloseOutline } from 'flowbite-svelte-icons';
    import Typewriter from 'svelte-typewriter';
    import { Slider } from 'bits-ui';

    // Custom utility functions and local assets
    import { getRandomColor } from '$lib/functions';
    import all_clubs from '$lib/all_clubs.json';
    import ResultView from '$lib/components/ResultView.svelte';
    import loadinggif from '$lib/assets/loading.gif';

    // State management
    let liveValue = [10]; // User input for live match importance
    let highlightValue = [20]; // User input for highlight importance
    let error: string | false = ''; // Error message handler
    let searchQuery = ''; // User input for club search
    let dateRange = { from: null, to: null }; // Selected date range
    let selectedClubs: string[] = []; // Clubs chosen by the user
    let clubs = all_clubs; // Initialize clubs from the imported JSON
    let results = null; // API response results
    let showresults = false; // Flag for toggling result view
    let loading = false; // Loading state

    // API base configuration
    const apiBase = PUBLIC_API_BASE ? PUBLIC_API_BASE : 'http://127.0.0.1:5000'; // Default Flask port

    // Lifecycle method to check API health
    onMount(() => {
        fetch(apiBase)
            .then(response => response)
            .then(data => {
                console.log('API health check successful for ' + apiBase + ':', data);
            })
            .catch(error => {
                console.error('Error making API call for ' + apiBase + ':', error);
            });
    });

    // Helper function to describe live value selection
    function getLiveValueStatement(liveValue: number[]): string {
        if (liveValue[0] <= 0) {
            return 'Not at all.';
        } else if (liveValue[0] <= 30) {
            return 'A little bit.';
        } else if (liveValue[0] < 70) {
            return 'I do care.';
        } else if (liveValue[0] < 100) {
            return 'I care A LOT! 🍿';
        } else {
            return 'MUST. HAVE. 🤯';
        }
    }

    // Display error message with timeout
    function displayError(msg: string, duration: number = 3000) {
        error = msg;
        setTimeout(() => {
            error = false;
        }, duration);
    }

    // Add a club to the selection
    function addClub(query: string) {
        if (clubs.includes(query) && !selectedClubs.includes(query)) {
            selectedClubs = [...selectedClubs, query];
            query = '';
            error = false;
        } else if (selectedClubs.includes(query)) {
            displayError('Club already added.', 3000);
        } else {
            displayError('Club not found.', 3000);	
        }
    }

    // Remove a club from the selection
    function removeClub(club: string) {
        selectedClubs = selectedClubs.filter(selectedClub => selectedClub !== club);
    }

    // Fetch optimal package based on user inputs
    async function findPackage() {
        if (selectedClubs.length <= 0) {
            displayError('Please select at least one club.', 3000);
            return;
        }

        showresults = true;
        loading = true;

        const response = await fetch(`${apiBase}/optimizePackages`, {
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

        if (response.status !== 200) {
            showresults = false;
            loading = false;
            results = await response.json();
            displayError(results['solver_status'], 5000);
            return;
        }

        results = await response.json();
        loading = false;
    }
</script>

{#if !showresults}
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
                <Badge dismissable large color={getRandomColor()} on:close={() => {removeClub(club)}}
                    
                    >{club}
                    <button slot="close-button" on:click={() => removeClub(club)} type="button" class="inline-flex items-center rounded-full p-0.5 my-0.5 ms-1.5 -me-1.5 text-sm  " aria-label="Remove">
                        <CloseOutline class="h-4 w-4 bg-transparent" />
                        <span class="sr-only">Remove badge</span>
                      </button>
                </Badge>
            {/each}
        </div>
        <div class="relative">
            <Search
                placeholder="Bayern München, FC Barcelona, ..."
                bind:value={searchQuery}
            >
                <Button class="mx-3 gap-1" on:click={() => addClub(searchQuery)}><PlusOutline /> Add</Button>
            </Search>
            {#if searchQuery}
                <ul class="mt-2 bg-white border border-gray-300 rounded-lg shadow-lg absolute w-full z-10">
                    {#each clubs.filter(club => club.toLowerCase().includes(searchQuery.toLowerCase()) && !selectedClubs.includes(club)).slice(0, 5) as club}
                        <li class="p-2 hover:bg-gray-200 cursor-pointer " on:click={() => addClub(club)}>
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
                {#if dateRange.from || dateRange.to}
                    <Button outline color="primary" size="sm" on:click={() => dateRange = { from: null, to: null }}>Clear</Button>
                {/if}
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
        <p class="text-center underline-offset-3 underline text-gray-600 cursor-pointer" 
        on:click={displayError("<a href='https://github.com/tmaringgele/streaming-package-comperator/fork' class='underline'>ToDo. Feel free to contribute</a>", 5000)}>or choose specific games</p>
    </div>
</div>

<Toast color="red" position="bottom-right" transition={slide} toastStatus={error}
divClass="w-full max-w-xs p-4 text-gray-500 bg-white shadow dark:text-gray-400 dark:bg-gray-800 gap-3">
    <svelte:fragment slot="icon">
      <ExclamationCircleSolid class="w-5 h-5" />
      <span class="sr-only">Warning icon</span>
    </svelte:fragment>
    {@html error}
</Toast>

{:else}
{#if loading}
<div class="flex-col bg-primary-800 bg-gradient-to-tr from-primary-800 to-primary-600 flex h-screen overflow-y-auto  items-center justify-center">

    <img src={loadinggif} alt="Loading" class=" w-20 "/>
<h1 class="text-2xl text-white">Loading...</h1>
</div>
{:else}
<Button class="m-3 absolute " color="primary" size="sm" on:click={() => {
    results = null
    showresults = false
    } }><ChevronLeftOutline />New Search</Button>
<ResultView {results} {selectedClubs}/>
{/if}
{/if}