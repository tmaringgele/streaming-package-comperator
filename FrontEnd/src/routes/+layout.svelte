<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>


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


{@render children()}
