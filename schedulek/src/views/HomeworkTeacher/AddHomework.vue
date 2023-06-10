<template>
  <div class="add-homework-options">
    <div class="subject-group-dropdown">
      <label for="subject">Subject:</label>
      <select v-model="selectedSubject" @change="selectSubject">
        <option value="" disabled selected hidden>Select a subject</option>
        <option v-for="subject in Object.keys(subjects)" :value="subject" :key="subject">{{ subject }}</option>
      </select>

      <label for="group">Group:</label>
      <select v-if="selectedSubject" v-model="selectedGroup">
        <option value="" disabled selected hidden>Select a group</option>
        <option v-for="group in subjects[selectedSubject]" :value="group" :key="group">{{ group }}</option>
      </select>
    </div>

    <div v-if="selectedGroup" class="homework-details">
      <label for="deadlineDate">Deadline Date:</label>
        <input type="date" v-model="form.deadlineDate">

      <label for="lessonHour">Lesson Hour:</label>
      <input type="text" v-model="form.lessonHour">

      <label for="isToUpload">Is to Upload:</label>
      <input type="checkbox" v-model="form.isToUpload">

      <label for="summary">Summary:</label>
      <textarea v-model="form.summary"></textarea>
    </div>

    <button v-if="selectedGroup" @click="submitHomework">Submit</button>

    <div v-if="successMessage" class="popup">
      {{ successMessage }}
    </div>
  </div>
</template>



<script>
import { useUserStore } from '../../stores/UserStore.js';

export default {
  setup() {
    const userStore = useUserStore();

    return {
      userStore
    };
  },
  data() {
    return {
      form: {
        deadlineDate: '',
        lessonHour: '',
        isToUpload: false,
        summary: '',
        teacher_id: this.userStore.loggedUserId
      },
      subjects: {},
      selectedSubject: '',
      selectedGroup: '',
      successMessage: ''
    };
  },
    computed: {
      defaultDeadlineDate() {
        return '2022-01-03';
      }
    },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(`http://localhost:5000/teacher_subjects/${this.userStore.loggedUserId}`);
        if (response.ok) {
          const data = await response.json();
          this.subjects = data.subjects;
        } else {
          throw new Error('Failed to fetch data');
        }
      } catch (error) {
        console.error(error);
      }
    },
    async selectSubject() {
      this.selectedGroup = '';
    },
    async submitHomework() {
      try {
        const response = await fetch(`http://localhost:5000/students_from_group/${this.selectedGroup}`);
        if (response.ok) {
          const data = await response.json();
          const students = data.students;
          const requests = students.map(student => {
            return fetch(`http://localhost:5000/homework`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                studentId: student.user_id,
                subject: this.selectedSubject,
                deadline_date: this.form.deadlineDate,
                lesson_number: this.form.lessonHour,
                is_to_upload: this.form.isToUpload,
                summary: this.form.summary,
                teacher_id: this.form.teacher_id
              })
            });
          });

          const responses = await Promise.all(requests);
        console.log(this.form);
          if (responses.every(response => response.ok)) {
            this.successMessage = 'Homework added successfully';
            this.selectedGroup = '';
            this.form = {
              deadlineDate: '',
              lessonHour: '',
              isToUpload: false,
              summary: '',
            };
          } else {
            throw new Error('Failed to add homework');
          }

          setTimeout(() => {
            this.successMessage = '';
          }, 5000);
        } else {
          throw new Error('Failed to fetch students');
        }
      } catch (error) {
        console.error(error);
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};

</script>

<style scoped>
.add-homework-options {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.subject-group-dropdown {
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
}

label {
  font-weight: bold;
}

input[type="date"],
input[type="text"],
textarea {
  width: 200px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.popup {
  background-color: #4caf50;
  color: white;
  padding: 10px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}


.add-grades-options {
  display: flex;
  flex-direction: row;
  margin-left: 40px;
  margin-top: 20px;
  gap: 20px;
}

select {
  width: 300px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #2B6777;
  border-radius: 20px;
  width: 170px;
  height: 57px;
  font-style: normal;
  font-weight: 600;
  font-size: 17px;
  color: white;
  text-decoration: none;
  align-items: center;
  border: 0px;
  outline: 0px;
  appearance: none;
}

select::-ms-expand {
  display: none;
}

table {
  margin-top: 20px;
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>
