<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data} githubRepo=https://github.com/edmundmiller/periodic_legislation
logo=/periodic_logo.jpg>
	<slot slot="content" />
</EvidenceDefaultLayout>