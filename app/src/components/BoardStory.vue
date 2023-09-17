<script setup lang="ts">

import EstimationCard from './EstimationCard.vue'
import PlayerStatusCard from './PlayerStatusCard.vue'

defineProps<{
  story: Object
  playerCount: Number
}>()

</script>

<template>
  <div class="card">
  <h1>{{ story.jira_id }}</h1>
  <p>{{ story.summary }}</p>
  <div n-if="story.bets.length == playerCount">
    <span n-for="bet in story.bets"></span>
  </div>
  <div v-if="story.bets.length < playerCount">
    <PlayerStatusCard class="user-played" v-for="played in story.bets.length" v-bind:played="true" />
    <PlayerStatusCard class="user-waiting" v-for="unplayed in playerCount - story.bets.length" v-bind:played="false" />
  </div>
  <div class="bets" v-if="story.bets.length == playerCount">
    <EstimationCard v-for="bet in story.bets" :value=bet.bet />
  </div>
    <i>
      <slot name="icon"></slot>
    </i>
    <div class="details">
      <h3>
        <slot name="heading"></slot>
      </h3>
      <slot></slot>
    </div>
  Status:
  {{story.bets.length}}
  

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

.bets {
  display: flex;
  flex-direction: row;
}
</style>
