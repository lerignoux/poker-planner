<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <div class="title">
    <img alt="Poker planner logo" class="logo" src="/poker-planner-logo.png" width="125" height="125" />
    <div>
      <h1 class="green">{{ msg }}</h1>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: 0px;
}

.title {
  display: flex;
}

.title h1 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
