<template>
  <div class="background">
    <div class="logout-square">
      <div class="logout-info">
        <div class="bye">Logged out!</div>
        <div class="info">You have successfully logged out from Schedulek</div>
      </div>
      <div class="submit">
        <button @click="getback">Return to login menu</button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      email: '',
      password: '',
      user: []
    }
  },
  methods: {
    getback() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.background {
  width: 100%;
  height: 100%;
  background-color: #2B6777;
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 180px);
}

.logout-square {
  background-color: #C8D8E4;
  width: 50%;
  height: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 80px;

}

button {
  background-color: #52AB98;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 10px;
  width: 250px;
  height: 50px;
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  color: white;
  text-decoration: none;
}

.logout-info {
  margin: 30px;
  text-align: center;
  font-weight: 600;

}

.bye {
  margin: 10px;
  font-weight: 600;
  font-size: 2.3em;
}

.info {
  color: #8F8C8C8C;
}

</style>