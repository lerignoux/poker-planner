<script setup lang="ts">

import { ref, computed, reactive } from 'vue'

defineProps<{
  story: Object
}>()

const emit = defineEmits(['updateBet'])
const bet = ref(0)

function updateBet(story_id, bet) {
  console.log(`New bet on ${story_id} bet: ${bet}`)
  emit('updateBet', story_id, bet)
}

</script>

<template>
  <div class="card">
  <h1>{{ story.jira_id }}</h1>
  <p>{{ story.summary }}</p>

  <label for="betSelect">Your bet</label>
  <select @change="updateBet(story.id, bet)" id="betSelect" v-model="bet">
    <option value='0'>S</option>
    <option value='1'>M</option>
    <option value='2'>L</option>
  </select>
  Status:

  </div>
</template>

<style scoped>
.item {
  margin-top: 2rem;
  display: flex;
  position: relative;
}

.details {
  flex: 1;
  margin-left: 1rem;
}

i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;

  color: var(--color-text);
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}

@media (min-width: 1024px) {
  .item {
    margin-top: 0;
    padding: 0.4rem 0 1rem calc(var(--section-gap) / 2);
  }

  i {
    top: calc(50% - 25px);
    left: -26px;
    position: absolute;
    border: 1px solid var(--color-border);
    background: var(--color-background);
    border-radius: 8px;
    width: 50px;
    height: 50px;
  }

  .item:before {
    content: ' ';
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    bottom: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:after {
    content: ' ';
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    top: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:first-of-type:before {
    display: none;
  }

  .item:last-of-type:after {
    display: none;
  }
}

.user-waiting {
  width: 20px;
  margin-right:4px;
  background-color: #aa0000;
}

.user-played {
  width: 20px;
  margin-right:4px;
  background-color: #00ff00;
}
</style>
