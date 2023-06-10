<template>
  <div class="add-grades-options">
    <div class="subject-dropdown-style">
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

    <table v-if="students.length > 0">
      <thead>
        <tr>
          <th>Student Name</th>
          <th>Grade</th>
          <th>Wage</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.student }}</td>
          <td><input type="number" v-model="student.grade" min="1" max="5"></td>
          <td><input type="number" v-model="student.wage" min="0"></td>
        </tr>
      </tbody>
    </table>

    <button v-if="students.length > 0" @click="submitGrades">Submit</button>

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
        studentId: '',
        wage: '',
        grade: '',
        subject: '',
        teacher_id: this.userStore.loggedUserId
      },
      subjects: {},
      selectedSubject: '',
      selectedGroup: '',
      students: [],
      successMessage: ''
    };
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
    async fetchStudents() {
      try {
        const response = await fetch(`http://localhost:5000/students_from_group/${this.selectedGroup}`);
        if (response.ok) {
          const data = await response.json();
          this.students = data.students.map(student => ({
            ...student,
            grade: '',
            wage: ''
          }));
        } else {
          throw new Error('Failed to fetch students');
        }
      } catch (error) {
        console.error(error);
      }
    },
    selectSubject() {
      this.selectedGroup = '';
      this.students = [];
    },
    async submitGrades() {
      try {
        const requests = this.students
          .filter(student => student.grade !== '' || student.wage !== '')
          .map(student => {
            return fetch(`http://localhost:5000/grades`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                studentId: student.user_id,
                wage: student.wage,
                grade: student.grade,
                subject: this.selectedSubject,
                teacher_id: this.userStore.loggedUserId
              })
            });
          });

        const responses = await Promise.all(requests);

        if (responses.every(response => response.ok)) {
          this.successMessage = 'Grades added successfully';
          this.students = [];
        } else {
          throw new Error('Failed to add grades');
        }
        setTimeout(() => {
          this.successMessage = '';
        }, 5000);
      } catch (error) {
        console.error(error);
      }
    }
  },
  watch: {
    selectedGroup() {
      if (this.selectedGroup) {
        this.fetchStudents();
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.popup {
  background-color: #4CAF50;
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
