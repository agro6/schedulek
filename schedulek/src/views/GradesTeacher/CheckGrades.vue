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


    <button v-if="selectedSubject && selectedGroup" @click="fetchGrades" class="nav-button">Check</button>

    <table v-if="students.length > 0" class="student-table">
      <thead>
        <tr>
          <th>Student Name</th>
          <th>Grades</th>
          <th>Average</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.student }}</td>
          <td>
            <span v-if="student.grades.length > 0">
              <div v-for="(grade, index) in student.grades" :key="index" :class="getGradeClass(grade.wage)">
                {{ grade.grade }}
              </div>
            </span>
          </td>
          <td>{{ calculateAverage(student.grades.map(g => g.grade), student.grades.map(g => g.wage)) }}</td>
        </tr>
      </tbody>
    </table>
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
        grade: '',
        subject: ''
      },
      subjects: {},
      selectedSubject: '',
      selectedGroup: '',
      students: [],
      successMessage: ''
    };
  },
  methods: {
    getGradeClass(wage) {
      return `wage-${wage}`;
    },
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
            grades: []
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
    async fetchGrades() {
      try {
        const response = await fetch(`http://localhost:5000/grades/${this.selectedGroup}/${this.selectedSubject}`);
        if (response.ok) {
          const data = await response.json();

          this.students.forEach((student) => {
            const studentGrades = data.grades
              .filter((grade) => grade.student_id === student.user_id)
              .map((grade) => ({
                grade: grade.grade,
                wage: grade.wage
              }));

            student.grades = studentGrades.length > 0 ? [...studentGrades] : [];
          });
        } else {
          throw new Error('Failed to fetch grades');
        }
      } catch (error) {
        console.error(error);
      }
    },
    calculateAverage(grades, wages) {
      if (grades.length === 0) {
        return '';
      }

      const weightedSum = grades.reduce((total, grade, index) => total + grade * wages[index], 0);
      const sumOfWeights = Object.values(wages).reduce((total, weight) => total + weight, 0);
      const average = weightedSum / sumOfWeights;
      return average.toFixed(2);
    },
    async checkSubjectAndGroup() {
      if (this.selectedSubject && this.selectedGroup) {
        await this.fetchGrades();
      }
    }
  },
  watch: {
    selectedGroup() {
      if (this.selectedGroup) {
        this.fetchStudents();
        this.checkSubjectAndGroup();
      }
    },
    selectedSubject() {
      if (this.selectedSubject && this.selectedGroup) {
        this.checkSubjectAndGroup();
      }
    }
  },
  mounted() {
    this.fetchData();
    this.checkSubjectAndGroup();
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
  margin-top: 200px;
}


.student-table {
  margin: 200px;
  margin-top: 20px;
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
  margin-left: auto; /* Center horizontally */
  margin-right: auto; /* Center horizontally */
}

th,
td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  color: black;
}

th,
td {
  text-align: left;
  padding: 8px;
  background-color: #F7F8FED9;
  width: 100px;
}

.grades-column {
  width: 420px;
}

tr {
  margin-bottom: 10px;
}

th {
  background-color: #52AB98;
  color: white;
}

div {
  height: 20px;
  width: 20px;
  display: table-cell;
  text-align: center;
  color: white;
}

.wage-1 {
  background-color: rgba(216, 16, 16, 0.74);
}

.wage-2 {
  background-color: rgba(197, 93, 93, 0.74);
}

.wage-3 {
  background-color: rgba(179, 131, 29, 0.5));
}

.wage-4 {
  background-color: rgba(46, 163, 36, 0.5);
}

.wage-5 {
  background-color: rgba(9, 138, 20, 0.884);
}
</style>
