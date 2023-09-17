<script setup lang="ts">
	import { ref, computed, reactive } from 'vue'
	import axios from 'axios'
	import Board from '../components/Board.vue'
	import { useRoute, useRouter } from 'vue-router';
	const route = useRoute();

	const router = useRouter()
	const inviteLink = ref(`http://localhost:8080/play/${route.params.gameId}`);
	const gameData = reactive({})

	const gameId = ref(route.params.gameId)

	function getGame() {
	  axios.get('http://192.168.2.10:8081/game', {
	    game_id: route.params.gameId
	  })
	  .then(response => {
	  	Object.assign(gameData, response.data)
	    gameId = gameData.id
	    stories = gameData.stories
	    players = gameData.players
	    console.log(gameData)
	  })
	  .catch(error => {
	    console.log(error);
	  });
	}

	function kickPlayer(player)
	{
		console.log(player)
		axios.post(`http://192.168.2.10:8081/game/${gameId.value}/kick/${player.id}`, {})
		.then(response => {
			let playerIndex = gameData.players.indexOf(player);
			gameData.players.splice(playerIndex)
	  	})
	  .catch(error => {
	    console.log(error);
	  });
	}

	const socket = new WebSocket(`ws://192.168.2.10:8081/game/${ route.params.gameId}/socket/dealer`)
    socket.onmessage = (event) => {
    	console.log(event.data)
    	Object.assign(gameData, JSON.parse(event.data))
  	}

	const sendMessage = (username,text) => {
	    const messageData = { username: username, message: text};
	    // Send the message data to the server using WebSockets
	    socket.send(JSON.stringify(messageData))
	  }
</script>

<template>
  <main>
  	<p>Current players:
  	<ul>
  		<li>
  		<span v-for="player in gameData.players" :key="player.id">{{ player.name }}, 
  			<button @click=kickPlayer(player)>Kick</button>
  		</span>
  		</li>
  	</ul>
  	</p>
  	<p>Invite player: </p>
  	<ul>
  		<li>Link: <a href="{{inviteLink}}">{{inviteLink}}</a></li>
  		<li>Code: {{gameId}}</li>
 	</ul>
    <Board :stories=gameData.stories :players=gameData.players />

  </main>
</template>

<style>
</style>

