<script lang="ts">
    import type { OptimizationResponse, Subscription, Game } from '$lib/types';
    import { Badge, Alert, AccordionItem, Accordion  } from 'flowbite-svelte';
    import GameCalender from '$lib/components/GameCalender.svelte';
    import { Section, Schedule, ScheduleItem } from "flowbite-svelte-blocks";
    import { Timeline, TimelineItem, Button, Popover } from 'flowbite-svelte';
  import { ArrowRightOutline, InfoCircleSolid } from 'flowbite-svelte-icons';
  import { getRandomColor } from '$lib/functions';
	import { onMount } from 'svelte';

    export let results: OptimizationResponse;
    export let selectedClubs: string[] = [];
    let start_date = new Date(results.start_date);
    let end_date = new Date(results.end_date);
    let games = results.games.filter(game => game.covered_by.length > 0);
    let showAllClubs = false;

    let neglectedGames: Game[] = []
    let neglectedSubscriptions: Subscription[] = []

  function isBetweenDates(startDate, endDate, date) {
  return date.getTime() >= startDate.getTime() && date.getTime() <= endDate.getTime();
  }
    function calculateDependentGames(subscription: Subscription, games) {
      let start_date_subscription = new Date(subscription.start_date);
      let end_date_subscription = new Date(start_date_subscription);
      end_date_subscription.setDate(end_date_subscription.getDate() + (subscription.yearly == 1 ? 365 : 30));
        let dependentGames = games.filter(game =>  
            game.covered_by.filter(pkg => pkg.id != subscription.package.id).length == 0
            &&
            isBetweenDates(start_date_subscription, end_date_subscription, new Date(game.starts_at))//if game is in scope of subscription
            
        ); // a game is dependent from a package, if there is no other package covering it
        
        return dependentGames;
    }

    // get subscription with the highest price/dependentGames ratio
    function calculateWorstSubscription(payedPlans: Subscription[]) {
      if(payedPlans.length <= 0 || usedPackages.length <= 1){
        return null
      }

      if(payedPlans.length <= 1 && (results.live_value >= 1 || results.highlight_value >= 1)){
        return null
      }

        let worstSubscription: {
            subscription: Subscription;
            dependentGames: Game[];

        } = {
            subscription: payedPlans[0],
            dependentGames: calculateDependentGames(payedPlans[0], games)
        }

        payedPlans.forEach(subscription => {
          let dependentGames = calculateDependentGames(subscription, games);
            if ((subscription.price / dependentGames.length) > ( worstSubscription.subscription.price / worstSubscription.dependentGames.length)) {
                worstSubscription = {
                    subscription,
                    dependentGames
                }
            }
        });
        return worstSubscription;
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
    let usedPackages
    let totalCost
    ({usedPackages, totalCost} = calculateUsedPackages(results.packages));

    let numberOfShownActionPlans = 3
    function getPayedSubscriptions(subscriptions: Subscription[]) {
      
        return subscriptions.filter(subscription => 
            subscription.price > 0
        )
      
      
    }

    let payedPlans = getPayedSubscriptions(results.packages);
    let worstSubscription = calculateWorstSubscription(payedPlans);

    
    
    
    
    function neglectWorstDeal(){
      if(!worstSubscription){
        return
      }
      
      // add worst deal to neglected games
      neglectedGames = [...neglectedGames, ...worstSubscription.dependentGames];
      neglectedSubscriptions = [...neglectedSubscriptions, worstSubscription.subscription];
      
      // from all the existing games remove the neglected subscription from the covered_by attribute
      // (if the game is happening in the time frame of the subscription)
      games.forEach(game => {
        if(isBetweenDates(new Date(worstSubscription.subscription.start_date), new Date(worstSubscription.subscription.start_date), new Date(game.starts_at))){
          game.covered_by = game.covered_by.filter(pkg => pkg.id != worstSubscription.subscription.package.id);
        }
      });


      games = games.filter(game => !neglectedGames.includes(game));
      results.packages = results.packages.filter(subscription => !neglectedSubscriptions.includes(subscription));
      ({usedPackages, totalCost} = calculateUsedPackages(results.packages));
      payedPlans = getPayedSubscriptions(results.packages);
      worstSubscription = calculateWorstSubscription(payedPlans);

      console.log('results.packages', results.packages)
      console.log("neglected games", neglectedGames)
      console.log('neglected Subscriptions',neglectedSubscriptions)
      if(worstSubscription && worstSubscription?.dependentGames.length == 0){
        // This normally should not happen.
        console.log('subscription neglected recursively')
        neglectWorstDeal()
      }
    }

</script>

<div class="flex flex-col gap-1 items-center mt-5">
    <h1 class="text-3xl font-semibold">⚡Results 📈</h1>
    <p class="text-center text-gray-600">Status: {results.solver_status}</p>
    <!-- <p class="text-center text-gray-600">{(results.live_value == 1 || results.highlight_value == 1) && results.ignored_games > 0 ? '(not including '+results.ignored_games+' non-live or non-highlight games)' : ''}</p> -->
    
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

  
  {#if neglectedGames.length > 0}
  <Alert class='underline' color='red' id="neglected-games">{neglectedGames.length} neglected game{neglectedGames.length == 1 ? '' : 's'}</Alert>
    <Popover class="w-64 text-sm font-light w-lg" triggeredBy={`#neglected-games`}>
      <ul class="">
        {#each neglectedGames as game}
        <li class='py-1'>
          {new Date(game.starts_at).toDateString()}: <span class=" font-semibold">{game.team_home} vs. {game.team_away}</span>
        </li>
        {/each}
        </ul>
  </Popover>
  {/if}
  {#if results.live_value >= 1}
  <p class="text-center text-gray-600"><span class="font-bold">Warning:</span> All non-live games are neglected.</p>
  {/if}
  {#if results.highlight_value >= 1}
  <p class="text-center text-gray-600"><span class="font-bold">Warning:</span> All non-highlight games are neglected.</p>
  {/if}

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
        <p class="mt-3 underline text-center text-gray-600 font-semibold cursor-pointer" on:click={() => {numberOfShownActionPlans = getPayedSubscriptions(results.packages).length}}>Show more</p>
      {:else if payedPlans.length > 3}
        <p class="mt-3 underline text-center text-gray-600 font-semibold cursor-pointer"  on:click={() => {numberOfShownActionPlans = 3}}>Show less</p>
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
        <tr class="border-black  border-t-2">
          <td></td>
          <td class=" px-4 py-2 font-bold ">Total Costs</td>
          <td class=" px-4 py-2 font-bold ">{(totalCost / 100).toFixed(2)} €</td>
        </tr>
      </tbody>
    </table>
    {#if worstSubscription}
    <Alert color='red'>
      <div class="flex items-center gap-3">
        <InfoCircleSolid class="w-5 h-5" />
        <span class="text-lg"><span class="font-medium">Worst Deal:</span> {worstSubscription.subscription.package.name}</span> 
      </div>
      <p class="mt-2 mb-4 text-sm">You can remove this {worstSubscription.subscription.yearly == 1 ? 'yearly' : 'monthly'} subscription starting at { new Date(worstSubscription.subscription.start_date).toDateString()} to save 
        {((worstSubscription.subscription.price / 100)).toFixed(2)} €
      while losing <span class='underline' id="worstDealGames">{worstSubscription.dependentGames.length} game{worstSubscription.dependentGames.length == 1 ? '' : 's'}.</span>
      </p>
     
      <div class="flex gap-2">
        <Button size="xs" color='red' outline on:click={neglectWorstDeal}>Remove</Button>
      </div>
    </Alert>
    <Popover class="w-fit text-sm font-light w-lg" triggeredBy={`#worstDealGames`}>
      <ul class="">
      {#each worstSubscription.dependentGames as game}
      <li class='py-1'>
        {new Date(game.starts_at).toDateString()}: <span class=" font-semibold">{game.team_home} vs. {game.team_away}</span>
      </li>
      {/each}
      </ul>
  </Popover>
  {/if}
  </div>
  


</div>

<div class="flex flex-col gap-5 mt-10 items-center"> 

<h2 class="text-xl font-semibold">Available Games 🍿</h2>
<GameCalender {start_date} {end_date}  {games}/>
</div>
