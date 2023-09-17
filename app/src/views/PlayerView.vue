<script setup lang="ts">

import { ref, computed, reactive } from 'vue'
import axios from 'axios'
import Board from '../components/Board.vue'
import PlayerHand from '../components/PlayerHand.vue'
import HandCard from '../components/HandCard.vue'
import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const gameId = ref(route.params.gameId)
const gameData = reactive({})

const playerInfo = ref({})


function joinGame(e) {
  e.preventDefault();
  console.log(playerInfo.value.name)
  axios.post(`http://192.168.2.10:8081/game/${gameId.value}/join`, {
    name: playerInfo.value.name,
    password: playerInfo.value.pin
  })
  .then(response => {
    console.log(`Player ${response.data.id} logged in.`);
    playerInfo.value.id = response.data.id

  })
  .catch(error => {
    console.log(error);
  });
}


const socket = new WebSocket(`ws://192.168.2.10:8081/game/${route.params.gameId}/socket/player`)

socket.onmessage = (event) => {
	console.log(`WS data received: ${event.data}`)
	let updatedData = JSON.parse(event.data)
	Object.assign(gameData, updatedData)
	}

const sendMessage = (username,text) => {
    const messageData = { username: username, message: text};
    // Send the message data to the server using WebSockets
    socket.send(JSON.stringify(messageData))
  }

const updateBet = (story_id, bet) => {
  const update = {
  	player_id: playerInfo.value.id,
  	story_id: story_id ,
  	bet: bet
  };
	console.log(`${update.player_id} voting ${bet} on ${story_id}`)
    socket.send(JSON.stringify(update))
  }

</script>

<template>
  <main>
  	Game: {{gameId}}
  	Player: {{playerInfo.id}}
  	<div v-if="playerInfo.id == undefined">
		<form>
		  <div class="input">
		    <label for="name">You name</label>
		    <input id="name" v-model="playerInfo.name" placeholder="">
		  </div>
		  
		  <div class="input">
		    <label for="playerPin">Pin</label>
		    <input id="playerPin" type="password" v-model="playerInfo.pin" placeholder="***">
		  </div>
		  
		  <button type="submit" @click="joinGame">Join Game</button>
		</form>
	</div>

	<div v-if="playerInfo.id != undefined">
	    <Board :stories=gameData.stories :players=gameData.players />
	    <PlayerHand :stories=gameData.stories @updateBet=updateBet />
    </div>
  </main>
</template>

<style>
</style>

