<script setup lang="ts">
import {ref, watch} from "vue";
import HandCard from './HandCard.vue'

defineProps<{
  stories: Array,
  websocket
}>()

const emit = defineEmits(['updateBet'])

function updateBet(story_id, bet) {
  emit('updateBet', story_id, bet)
}

</script>

<template>
  <div>
    {{stories}}
    Cards:
    <HandCard v-for="story in stories" :key="story.jira_id" :story=story @updateBet=updateBet />
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
