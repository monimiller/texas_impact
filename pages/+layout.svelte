<script>
	import "@evidence-dev/tailwind/fonts.css";
	import "../app.css";
	import { EvidenceDefaultLayout } from "@evidence-dev/core-components";
	export let data;
</script>

<EvidenceDefaultLayout
	{data}
	githubRepo="https://github.com/monimiller/texas_impact"
	builtWithEvidence="true"
	title="Texas Impact Bill Tracker"
	description="Track and analyze legislation that matters to Texas Impact's mission"
>
	<!-- TODO logo="/texas-impact-logo.png" -->
	<slot slot="content" />
</EvidenceDefaultLayout>
