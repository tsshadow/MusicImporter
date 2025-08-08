<script>
import { createEventDispatcher } from 'svelte';
import { getJobsContext } from '$lib/jobs-context';

const { steps, start } = getJobsContext();
let selected = '';
let breakOnExisting = true;
let repeatInterval = 0;
let breakOnExisting = false;
const dispatch = createEventDispatcher();

$: if (!selected && $steps.length > 0) {
  selected = $steps[0];
}

async function startSelected() {
  if (!selected) return;
  const job = await start(selected, { breakOnExisting });
  const options = {};
  if (repeatInterval > 0) options.repeatInterval = repeatInterval;
  if (breakOnExisting) options.breakOnExisting = true;
  const job = await start(selected, options);
  if (job) {
    dispatch('started', job);
  }
}
</script>

<div>
  <select bind:value={selected}>
    {#each $steps as step}
      <option value={step}>{step}</option>
    {/each}
  </select>
  <label>
    <input type="checkbox" bind:checked={breakOnExisting} />
    Break on existing
  </label>
  <input
    type="number"
    min="0"
    placeholder="Repeat interval"
    bind:value={repeatInterval}
  />
  <label>
    <input type="checkbox" bind:checked={breakOnExisting} /> Break on existing
  </label>
  <button on:click={startSelected}>Start</button>
</div>
