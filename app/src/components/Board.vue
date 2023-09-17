<script setup lang="ts">
import BoardStory from './BoardStory.vue'

  const props = defineProps({
    gameId: String,
    stories: Array,
    players: Array,
  });

</script>

<template>
 Board:
  <BoardStory
    v-for="story in stories"
    :story="story"
    :key="story.id"
    :playerCount="players.length"
   />
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
