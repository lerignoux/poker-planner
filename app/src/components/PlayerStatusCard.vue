<script setup lang="ts">

defineProps<{
  played: Boolean
}>()

</script>

<template>
  <div class="status user-played" v-if="played" >
	<img src="/player.png"/>
  </div>
  <div class="status user-waiting" v-else >
	<img src="/player.png"/>
  </div>
</template>

<style scoped>

.user-played {
	background-color: #0c8579;
}

.user-waiting {
	background-color: #9e2416;
}

.status {
  display: inline-block;
  margin: 2px;
  width: 30px;
  height: 40px;
  color: black;

  padding: 2px;
  border-radius: 4px;
  -moz-border-radius: 4px;

  img {
    margin-top: 5px;
    margin-bottom: 5px;
  	width:28px;
	height:28px;
  }
}

</style>
