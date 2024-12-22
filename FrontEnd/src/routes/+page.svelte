<script>
    import { Search, Button } from "flowbite-svelte";
    import { Dropdown, DropdownItem, Badge } from "flowbite-svelte";
    import { Datepicker } from "flowbite-svelte";
    import { SearchOutline, CalendarEditOutline, ChevronDownOutline, PlusOutline } from "flowbite-svelte-icons";
    import { onMount } from "svelte";
    import Typewriter from 'svelte-typewriter'

    let searchQuery = "";
    let selectedTournament = "";
    let dateRange = { start: "", end: "" };

    let tournaments = [
        { id: 1, name: "Tournament A" },
        { id: 2, name: "Tournament B" },
        { id: 3, name: "Tournament C" },
    ];

    function handleSearch() {
        console.log("Searching for:", searchQuery, selectedTournament, dateRange);
        // Make API call with searchQuery, selectedTournament, and dateRange
    }
</script>

<div class="flex justify-center items-center h-screen bg-primary-800">
    <div class="w-full max-w-2xl bg-gray-50 p-4 rounded-lg shadow-lg">
        <Typewriter delay={500} keepCursorOnFinish={1000}>
        <h1 class="text-2xl font-semibold text-center mb-4">
            
                Welcome! ⚽
        </h1>
    </Typewriter>
    <Typewriter delay={2000} keepCursorOnFinish={3000}>

        <p class="text-center text-gray-600">Let's find your optimal streaming package</p>
    </Typewriter>
    <Typewriter delay={6000} keepCursorOnFinish={1000}>

        <p class="text-center text-gray-600 mb-4 text-xs">(With the help of ✨Integer Programming✨)</p>
    </Typewriter>
        <Search placeholder="Search for your favorite clubs...">
            <Button class="mx-3 gap-1"><PlusOutline /> Add </Button>
          </Search>
    
    <div class='border-b-5 border-black my-4 w-1/2 mx-auto gap-5'>
    <h2 class="text-xl font-semibold text-center mb-4">
        My Clubs
    </h2>
    <Badge dismissable large>Default</Badge>
    <Badge dismissable large color="dark">Dark</Badge>
    <Badge dismissable large color="red">Red</Badge>
    <Badge dismissable large color="green">Green</Badge>
    <Badge dismissable large color="yellow">Yellow</Badge>
    <Badge dismissable large color="indigo">Indigo</Badge>
    <Badge dismissable large color="purple">Purple</Badge>
    <Badge dismissable large color="pink">Pink</Badge>
    </div>

</div>
</div>

<style>
    @font-face {
        font-family: 'Gelasio';
        font-style: normal;
        font-weight: 400;
        src: local('Gelasio Regular'), local('Gelasio-Regular'), url(https://fonts.gstatic.com/s/gelasio/v1/cIf9MaFfvUQxTTqS9C6hYQ.woff2) format('woff2');
    }

    h1 {
        font-family: 'Tommy', sans-serif;
    }
</style>