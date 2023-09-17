<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'

import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
const router = useRouter()

const jira_host = ref('jira.com');
const jira_jql = ref('Sprint = Current_Sprint() AND status = Open()');
const jira_login = ref('Gimli');
const jira_password = ref('****');
const planner_system = ref('tshirt');
const conflict_resolution = ref('manual')

function startGame(e) {
  e.preventDefault();
  axios.put('http://192.168.2.10:8081/game', {
    planner_system: planner_system.value,
    jira_url: jira_host.value[0],
    stories: [
      {jira_id: "IMG-3", summary: "test1"},
      {jira_id: "IMG-4", summary: "test2"}
    ]
  })
  .then(response => {
    console.log(`starting game ${response.data.id}`);
    router.push({ name: 'deal', params: { gameId: response.data.id }  })
  })
  .catch(error => {
    console.log(error);
  });
}

function joinGame(e) {
  e.preventDefault();
  router.push({ name: 'play', params: { gameId: game_id.value }  })
}

</script>

<template>

  <div>
  </div>


  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
    </template>
    <template #heading>New game</template>

    <div>
      <form>
        <div class="input">
          <label for="jira_host">Planner system</label>
          <input id="jira_host" v-model="jira_host" placeholder="jira.com">
        </div>

        <div class="input">
          <label for="jira_jql">JQL Query</label>
          <input id="jira_jql" v-model="jira_jql" placeholder="Sprint = Current_Sprint() AND status = Open()">
        </div>
        
        <div class="input">
          <label for="jira_login">Jira login</label>
          <input id="jira_login" v-model="text" placeholder="">
        </div>
        
        <div class="input">
          <label for="jira_password">Jira password*</label>
          <input id="jira_password" type="password" v-model="text" placeholder="***">
        </div>
        
        <div class="input">
          <label for="planner_system">Planner system</label>
          <select id="planner_system" v-model="planner_system">
            <option value='tshirt'>Tshirt</option>
            <option disabled value='log'>Log</option>
            <option disabled value='days'>Days</option>
          </select>
        </div>

        <div class="input">
          <label for="conflict_resolution">Conflict resolutions</label>
          <select id="conflict_resolution" v-model="conflict_resolution">
            <option value='manual'>Manual</option>
            <option disabled value='majority'>Majority</option>
            <option disabled value='highest'>Highest</option>
          </select>
        </div>

        <button type="submit" @click="startGame">Start</button>
      </form>
    </div>
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <ToolingIcon />
    </template>
    <template #heading>Join a game</template>

    <form>
      <div class="input">
        <label for="game_id">Game ID</label>
        <input id="game_id" v-model="game_id" placeholder="">
      </div>

      <div class="input" style="display: None;">
        <label for="player_name">Your name</label>
        <input id="player_name" v-model="player_name" placeholder="Legolas">
      </div>
      
      <div class="input" style="display: None;">
        <label for="player_pin">Your pin</label>
        <input id="player_pin" type="password" v-model="player_pin" placeholder="***">
      </div>
      
      <button type="submit" @click="joinGame">Join</button>
    </form>
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <EcosystemIcon />
    </template>
    <template #heading>Ecosystem</template>
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <CommunityIcon />
    </template>
    <template #heading>Community</template>
    See project source code: <a her="https://github.com/lerignoux/poker-planner">Github</a>
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <SupportIcon />
    </template>
    <template #heading>Support Me</template>

    As an independent project, Poker planner relies on community backing for its sustainability. You can help
    us by offering a beer or sending a bitcoin :p.

    Thanks:
    *  <a href="https://www.flaticon.com/free-icons/user" title="user icons">icons created by Freepik - Flaticon</a>
  </WelcomeItem>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
}

.input {
  label {
    min-width: 20%;
  }
  input {
    width: 100%;
    background-color: #555555;
    border: 0;
  }
  display: flex;
  flex-direction: row;
  margin:2px;
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
