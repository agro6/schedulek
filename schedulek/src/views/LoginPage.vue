<template>
  <div class ="background">
    <div class ="login-square">
      <div class ="welcome-info">
        <div class ="welcome">Welcome to Schedulek!</div>
        <div class="info">Sign in to access your course details</div>
      </div>
      <form @submit.prevent = "handleSubmit">
      <div>
        <input type = "email" required v-model = "email" placeholder="Email">
      </div>
      <div>
        <input type = "password" required v-model = "password" placeholder="Password">
      </div>
      <div class="submit">
        <div v-if="errMsg" class="login-error">{{ errMsg }}</div>
        <button>Log in</button>
      </div>
    </form>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/UserStore.js';
import {getAuth, signInWithEmailAndPassword} from "firebase/auth";

export default {
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      email: '',
      password: '',
      user: [],
      showError: false,
      errMsg: ''
    };
  },
  methods: {
    async handleSubmit() {
      const auth = getAuth();
      signInWithEmailAndPassword(auth, this.email, this.password)
        .then(async () => {
          console.log("Logged in");
          const response = await fetch(`http://localhost:5000/user_info?email=` + this.email);
          const data = await response.json();
          this.user = data;
          this.verifyUser();
          this.pushUser();
        })
        .catch((error) => {
          console.log(error.code);
          switch (error.code) {
            case 'auth/invalid-email':
              this.errMsg = "Invalid email"
              break
            case 'auth/user-not-found':
              this.errMsg = "There is no account with that email"
              break
            case 'auth/wrong-password':
              this.errMsg = "Incorrect password"
              break
            default:
              this.errMsg = "Email or password is incorrect"
          }
        }
      );
    },
    pushUser() {
      if(this.userStore.type == 'student') {
        this.$router.push('/calendar');
      }
      else if(this.userStore.type == 'teacher') {
        this.$router.push('/timetable/teacher');
      }
    },
    verifyUser() {
      if (this.user["result"] == "not found") {
        this.showError = true;
        console.log(this.user);
      }
      else {
        this.userStore.storeEmail(this.email);
        this.userStore.storeType(this.user.type);
        this.userStore.storeLoggedUserId(this.user.id);
        this.userStore.storeName(this.user.name);
        this.userStore.storeLastName(this.user.last_name);
      }
    }
  }
}
</script>

<style>
.background{
  background-color: #2B6777;
  width: 100%;
  height: calc(100vh - 180px);
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-square{
  background-color: #C8D8E4;
  width: 50%;
  height: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  
}
.form{
  background-color: #2B6777;
}
form{
  display: flex;
  flex-direction: column;
  gap: 20px;
}
input{
  border: 0px;
  border-radius: 10px;
  width: 350px;
  height: 40px;
  font-size: 20px;
  padding-left: 10px;
}
::placeholder{
  color: #C0BDB6;
}
button {
  background-color: #52AB98;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 10px;
  width: 150px;
  height: 50px;
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  color: white;
  text-decoration: none;
}
.welcome-info{
  margin: 30px;
  text-align: center;
  font-weight: 600;
  
}
.welcome{
  margin: 10px;
  font-weight: 600;
  font-size: 2.3em;
}
.info{
  color: #8F8C8C8C;
}
.submit{
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}
.login-error{
  color: red;
}
</style>