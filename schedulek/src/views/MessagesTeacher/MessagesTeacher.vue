<template>
  <div>
    <div>
      Messages
    </div>
    <button @click="showForm = true" class="nav-button">Compose Message</button>
    <button @click="fetchMessages" class="nav-button">Show Messages</button>


    <div v-if="showForm" class="compose-form">
      <label for="title">Title:</label>
      <input type="text" v-model="form.title">

      <label for="message">Message:</label>
      <textarea v-model="form.message"></textarea>

      <label for="recipient">Recipient:</label>
      <select v-model="form.user_id">
        <option v-for="student in students" :key="student.user_id" :value="student.user_id">
          {{ student.full_name }}
        </option>
      </select>

      <button @click="sendMessage">Send</button>
    </div>
<div v-else>
    <div>Received</div>
    <div  class="container">
      <div v-for="message in received" :key="message.id" class="card">
        <div class="header">
          <div class="content">
            <span class="title">{{ message.from }} - {{ message.title }}</span>
            <p class="message">{{ message.date }} - {{ message.message }}</p>
          </div>
        </div>
      </div>
    </div>

    <div>Sent</div>
    <div class="container">
      <div v-for="message in sent" :key="message.id" class="card">
        <div class="header">
          <div class="content">
            <span class="title">{{ message.title }} - {{ message.to }}</span>
            <p class="message">{{ message.date }} - {{ message.message }}</p>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../../stores/UserStore.js';

export default {
  name: 'MessagesPage',
  props: {
    studentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      received: [],
      sent: [],
      showForm: false,
      form: {
        title: '',
        message: '',
        user_id: '',
        logged_user_id: ''
      },
      students: []
    };
  },
  async created() {
    try {
      const userStore = useUserStore();
      this.form.logged_user_id = userStore.loggedUserId;

      const response1 = await fetch(`http://localhost:5000/messages/${this.form.logged_user_id}`);
      const data1 = await response1.json();
      this.received = data1.received;
      this.sent = data1.sent;

      const response = await fetch(`http://localhost:5000/all-students`);
      const data = await response.json();
      this.students = data.students;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
      fetchMessages() {

        fetch(`http://localhost:5000/messages/${this.form.logged_user_id}`)
          .then(response => response.json())
          .then(data => {
            this.received = data.received;
            this.sent = data.sent;
            this.showForm = false;
          })
          .catch(error => {
            console.error(error);
          });
      },
    async sendMessage() {
      try {
        const response = await fetch(`http://localhost:5000/add-message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        if (response.ok) {
          this.form.title = '';
          this.form.message = '';
          this.form.user_id = '';
          console.log('Message sent successfully!');
        } else {
          throw new Error('Failed to send message');
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.nav-button{
  display: flex;
  justify-content: center;
  background: #2B6777;
  border-radius: 20px;
  width: 210px;
  height: 77px;
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  color: white;
  text-decoration: none;
  margin-right: 20px;
  align-items: center;
}

.compose-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.compose-form label {
  font-weight: bold;
}

.compose-form input[type="text"],
.compose-form textarea {
  width: 200px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.compose-form button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  /* Add a fixed height to the card */
  height: 100px;
  overflow: hidden;
  position: relative;
  text-align: left;
  border-radius: 0.5rem;
  max-width: 300px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  background-color: #fff;
}

.header {
  padding: 1.25rem 1rem 1rem 1rem;
}

.title {
  color: #066e29;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.5rem;
}

.message {
  margin-top: 0.5rem;
  color: #595b5f;
  font-size: 0.875rem;
  line-height: 1.25rem;
}
</style>
