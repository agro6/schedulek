<template>
  <div class="logged-info">
    <div class="inline light-text">
       Logged
    </div>
    <div class="inline light-text">
      {{ userStore.type }}
    </div>
    <div>
            {{ userStore.last_name }} {{ userStore.name }}
        </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/UserStore.js'

export default {
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
      users: [],
  }
  },
  methods: {},
  async created() {
    try {
      const response = await fetch(`http://localhost:5000/users`);
      const data = await response.json();
      this.users = data;
      console.log(this.userStore.type)
    } catch (error) {
      console.error(error);
    }
  }
}
</script>

<style>
.logged-info{
  font-size: 0.5em;
  text-align: right;
  margin-left: 70px;
}
.inline{
  display:inline;
}
.light-text{
  font-weight: 20;
}
</style>