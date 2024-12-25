<script lang="ts">
    import type { OptimizationResponse, Subscription } from '$lib/types';
    import { Badge } from 'flowbite-svelte';
    import GameCalender from '$lib/components/GameCalender.svelte';
    import { Section, Schedule, ScheduleItem } from "flowbite-svelte-blocks";
    import { Timeline, TimelineItem, Button, Popover } from 'flowbite-svelte';
  import { ArrowRightOutline } from 'flowbite-svelte-icons';
  import { getRandomColor } from '$lib/functions';
	import { onMount } from 'svelte';

    export let results: OptimizationResponse;
    export let selectedClubs: string[] = [];
    let start_date = new Date(results.start_date);
    let end_date = new Date(results.end_date);
    let games = results.games;
    let showAllClubs = false;

    function calculateDependentGames(subscription, games) {
        let dependentGames = games.filter(game =>  
            !game.covered_by.some(pkg => pkg.id != subscription.package.id)
        ); // a game is dependent from a package, if there is no other package covering it
        
        return dependentGames.length;
    }

    // returns a duplicate-free list of used packages with total price
    function calculateUsedPackages(subscriptions: Subscription[]) {
        let usedPackages: {
          amount: number;
          yearly: boolean;
          pkg: {
            id: number;
            name: string;
          };
          price: number;
        } = [];
        let totalCost = 0;
        subscriptions.forEach(subscription => {
          let existingSubscription = usedPackages.find(sub => sub.pkg.id == subscription.package.id);
          if (existingSubscription) {
            existingSubscription.amount++;
            totalCost += subscription.price;
          } else {
            usedPackages.push({
              amount: 1,
              yearly: subscription.yearly == 1,
              pkg: {
                id: subscription.package.id,
                name: subscription.package.name
              },
              price: subscription.price
            });
            totalCost += subscription.price;
          }
        });

        // sort such that free tv is at the bottom
        usedPackages.sort((a, b) => {
          if (a.price == 0) return 1;
          if (b.price == 0) return -1;
          return a.price - b.price;
        });
        return {usedPackages, totalCost};
        
    }
    let {usedPackages, totalCost} = calculateUsedPackages(results.packages);

    let numberOfShownActionPlans = 3
    function getPayedSubscriptions(subscriptions: Subscription[]) {
      
        return subscriptions.filter(subscription => subscription.price > 0)
      
      
    }

    let payedPlans = getPayedSubscriptions(results.packages);

</script>

<div class="flex flex-col gap-1 items-center mt-5">
    <h1 class="text-3xl font-semibold">⚡Results📈</h1>
    <p class="text-center text-gray-600">Status: {results.solver_status}</p>
    <p class="text-center text-gray-600">{(results.live_value == 1 || results.highlight_value == 1) && results.ignored_games > 0 ? '(not including '+results.ignored_games+' non-live or non-highlight games)' : ''}</p>
    
    <div class="flex gap-2 flex-wrap max-w-xl justify-center my-3">
        {#if showAllClubs}
            {#each selectedClubs as club}
                <Badge large color={getRandomColor()} on:close={() => {
                    selectedClubs = selectedClubs.filter(selectedClub => selectedClub !== club);
                }}>{club}</Badge>
            {/each}
        {:else}
            {#each selectedClubs.slice(0, 3) as club}
                <Badge large color={getRandomColor()} on:close={() => {
                    selectedClubs = selectedClubs.filter(selectedClub => selectedClub !== club);
                }}>{club}</Badge>
            {/each}
            {#if selectedClubs.length > 3}
                <span class="underline cursor-pointer" on:click={() => showAllClubs = true}>and {selectedClubs.length - 3} more</span>
            {/if}
        {/if}
    </div>
    <p class="text-center underline " id="query-details">Query Details</p>
    <Popover class="w-64 text-sm font-light w-lg" triggeredBy={`#query-details`}>
      <table class="table-auto w-full border-collapse">
        <tbody class="w-full">
          <tr>
            <td><span class='font-bold'>Start Date:</span></td>
            <td>{start_date.toLocaleDateString()}</td>
          </tr>
          <tr>
            <td><span class='font-bold'>End Date:</span></td>
            <td>{end_date.toLocaleDateString()}</td>
          </tr>
          <tr>
            <td><span class='font-bold'>Live Importance:</span></td>
            <td>{(results.live_value * 100).toFixed(0)}%</td>
          </tr>
          <tr>
            <td><span class='font-bold'>Highlight Importance:</span></td>
            <td>{(results.highlight_value * 100).toFixed(0)}%</td>
          </tr>
        </tbody>
      </table>
  </Popover>

</div>
<hr class="w-full border-gray-300 my-5">
<div class="flex flex-row gap-10 mt-10 w-full justify-items-stretch justify-evenly max-h-full">
  {#if totalCost > 0}
  <div class="flex flex-col justify-start content-center gap-4 items-center px-5">
    <h2 class="text-xl font-semibold self-center">Action plan 💰</h2>
    <Timeline>
      {#each payedPlans.slice(0, numberOfShownActionPlans) as subscription}

      {#if subscription.price > 0}
      
        <TimelineItem spanClass="ring-primary"
         title={subscription.package.name} date={(new Date(subscription.start_date)).toDateString()}>
        
          <p>Subscribe for one {subscription.yearly == 1 ? 'Year' : 'Month'}</p>
          
        </TimelineItem>
      {/if}
      {/each}
      {#if numberOfShownActionPlans < payedPlans.length}
        <p class="mt-3 underline text-center text-gray-600 font-semibold" on:click={() => {numberOfShownActionPlans = getPayedSubscriptions(results.packages).length}}>Show more</p>
      {:else if payedPlans.length > 3}
        <p class="mt-3 underline text-center text-gray-600 font-semibold"  on:click={() => {numberOfShownActionPlans = 3}}>Show less</p>
        {/if}
     
      
    </Timeline>
  
  </div>
  {/if}
  <div class="flex flex-col justify-start content-center gap-4 ">
    <h2 class="text-xl font-semibold self-center">Used subscriptions 📺</h2>
    <table class="table-auto w-full border-collapse">
     
      <tbody>
        {#each usedPackages as {amount, pkg, price, yearly}}
          <tr>
            <td class="">{price != 0 ? amount+'x' : ''}</td>
            <td class=" px-4 py-2">{pkg.name}</td>
            <td class=" px-4 py-2">
              {#if price == 0}
                Free 🤩
              {:else}
                {(price / 100).toFixed(2)}€ {yearly ? 'per year' : 'per month'}
              {/if}
            </td>
          </tr>
        {/each}
        <tr class="">
          <td></td>
          <td class=" px-4 py-2 font-bold border-t-2 border-black">Total Costs</td>
          <td class=" px-4 py-2 font-bold border-t-2 border-black">{(totalCost / 100).toFixed(2)} €</td>
        </tr>
      </tbody>
    </table>
  </div>
  


</div>

<div class="flex flex-col gap-5 mt-10 items-center"> 

<h2 class="text-xl font-semibold">Available Games 🍿</h2>
<GameCalender {start_date} {end_date}  {games}/>
</div>
