<script lang="ts">
	import { Search, Button } from 'flowbite-svelte';
	import { Dropdown, DropdownItem, Badge } from 'flowbite-svelte';
	import { Datepicker, P } from 'flowbite-svelte';
	import { Range, Label } from 'flowbite-svelte';
	import {
		SearchOutline,
		CalendarEditOutline,
		ChevronDownOutline,
		PlusOutline
	} from 'flowbite-svelte-icons';
	import { onMount } from 'svelte';
	import Typewriter from 'svelte-typewriter';
	import { Slider } from 'bits-ui';
	import { get } from 'svelte/store';

	let liveValue = [10];
	let highlightValue = [20];

	function getLiveValueStatement(liveValue: number[]): string {
		if (liveValue[0] <= 0) {
			return 'Not at all.';
		} else if (liveValue[0] <= 30) {
			return 'A little bit.';
		} else if (liveValue[0] < 70) {
			return 'I do care.';
		} else {
			return 'I care A LOT! 🍿';
		}
	}

	let searchQuery = '';
	let selectedTournament = '';
	let dateRange = { from: null, to: null };

	let tournaments = [
		{ id: 1, name: 'Tournament A' },
		{ id: 2, name: 'Tournament B' },
		{ id: 3, name: 'Tournament C' }
	];

	function handleSearch() {
		console.log('Searching for:', searchQuery, selectedTournament, dateRange);
		// Make API call with searchQuery, selectedTournament, and dateRange
	}
</script>

<div class="bg-primary-800 bg-gradient-to-tr from-primary-800 to-primary-600 flex h-screen items-center justify-center">
	<div class="w-full max-w-2xl rounded-lg bg-gray-50 p-4 shadow-lg">
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
			<Badge dismissable large>Default</Badge>
			<Badge dismissable large color="dark">Dark</Badge>
			<Badge dismissable large color="red">Red</Badge>
			<Badge dismissable large color="green">Green</Badge>
			<Badge dismissable large color="yellow">Yellow</Badge>
			<Badge dismissable large color="indigo">Indigo</Badge>
			<Badge dismissable large color="purple">Purple</Badge>
			<Badge dismissable large color="pink">Pink</Badge>
		</div>
		<Search
			placeholder="Bayern München, FC Barcelona, ..."
			bind:value={searchQuery}
			on:search={handleSearch}
		>
			<Button class="mx-3 gap-1"><PlusOutline /> Add</Button>
		</Search>

		<div class="mt-8 flex flex-row gap-8">
			<div class="flex flex-col gap-3 grow">
				<Label class="text-md">Looking for a specific timespan?</Label>
				<Datepicker range bind:rangeFrom={dateRange.from} bind:rangeTo={dateRange.to} 
                dateFormat={
                    {
                        month: 'short',
                        day: 'numeric',
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

        <Button class="mt-10 w-full mb-2" color="primary" size="lg">Find my package</Button>
        <p class="text-center underline-offset-3 underline text-gray-600 cursor-pointer">or choose specific games</p>


	</div>
</div>

<style>
	@font-face {
		font-family: 'Gelasio';
		font-style: normal;
		font-weight: 400;
		src:
			local('Gelasio Regular'),
			local('Gelasio-Regular'),
			url(https://fonts.gstatic.com/s/gelasio/v1/cIf9MaFfvUQxTTqS9C6hYQ.woff2) format('woff2');
	}

	h1,
	h2 {
		font-family: 'Tommy', sans-serif;
	}
</style>
