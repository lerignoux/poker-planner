<script setup lang="ts">

defineProps<{
  value: Number
}>()

</script>

<template>
  <div class="estimation">
	<span v-if="value == 0">S</span>
	<span v-if="value == 1">M</span>
	<span v-if="value == 2">L</span>
	<span v-if="value == 3">XL</span>
  </div>
</template>

<style scoped>
.estimation {
  display: inline-block;
  margin: 2px;
  display: flex;
  background-color: #ffffff;
  width: 30px;
  height: 40px;
  color: black;

  padding: 2px;
  border-radius: 4px;
  -moz-border-radius: 4px;

  span {
	  width:100%;
	  text-align: center;
	  vertical-align: middle;
	  line-height: 39px;
	  font-weight: bold;
	  font-size: 1.4em;
  }
}

</style>
