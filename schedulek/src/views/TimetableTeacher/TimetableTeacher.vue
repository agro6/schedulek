<template>
  <div>
  <label for="weeks">Choose a week:</label>

  <select  id="weeks-dropdown" v-model="chosenWeek" @click ="check">
    <option v-for="week in weeks" :key="week" :value="week" >{{ week[0] }} - {{ week.slice(-1)[0] }}</option>
  </select>

  <div class="table-container">
    <table class="my-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Monday</th>
          <th>Tuesday</th>
          <th>Wednesday</th>
          <th>Thursday</th>
          <th>Friday</th>
          <!-- <th v-for="date in orderedDates" :key="date">{{ date }}</th> -->
        </tr>
      </thead>
      <tbody>
        <template v-for="(value, key) in timetable" :key="key">
          <tr>
            <td>{{ convertHour(key) }}</td>
            <td v-for="date in chosenWeek" :key="date">{{ value[date] || '' }}</td>
          </tr>
        </template>
      </tbody>
    </table>
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
  name: 'TimetableTeacher',
  props: {
    studentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      timetable: [],
      weeks: [],
      chosenWeek: [],
      mappedHours: [],
    }
  },
  async created() {
    try {
      const response = await fetch(`http://localhost:5000/teacher_lessons_table/${this.userStore.loggedUserId}`);
      const data = await response.json();
      this.timetable = data.timetable;
      console.log(this.timetable);
      const responseHrs = await fetch(`http://localhost:5000/lessons_hours`);
      const hours_data = await responseHrs.json();
      this.mappedHours = hours_data.hours;
      console.log(this.mappedHours);
    } catch (error) {
      console.error(error);
    }
    this.createWeeks()
    this.setDefaultWeek()
    console.log(this.weeks)
},
  computed: {
    orderedDates() {
      const allDates = Object.values(this.timetable).reduce(
        (dates, obj) => [...dates, ...Object.keys(obj)],
        []
      );

      const uniqueDates = [...new Set(allDates)].sort();

      return uniqueDates;
    },
  },
  methods: {
     createWeeks() {
      let x = 0
      for (let index = 0; index < this.orderedDates.length / 5; index++) {
        this.weeks[index] = this.orderedDates.slice(x, x+5)
        x += 5
      }
    },
    setDefaultWeek() {
      this.chosenWeek = this.weeks[0]
    },
    convertHour(key) {
      for (let i = 0; i < this.mappedHours.length; i++){
        if (key == this.mappedHours[i][0]) {
          const temp = this.mappedHours[i][1]
          if (temp <= 12 && temp >= 9) {
            return String(temp) + ' AM'
          }
          else{
            return String(temp) + ' PM'
          }
        }
      }
    }

  }

}
</script>

<style scoped>
.table-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 40px;

}

.my-table {
  border-collapse: collapse;
  width: 1000px;
  margin-top: 40px;
  table-layout: fixed;
}

.my-table th,
.my-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.my-table th {
  background-color: #52AB98;
  font-weight: bold;
  color: white;
}

.my-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.my-table tbody tr:hover {
  background-color: #e6e6e6;
}
#weeks-dropdown{
  width: 310px;
  height: 57px;
  border-radius: 20px;
  border: none;
  text-align: center;
  font-size: 1.2em;
  font-weight: 500;
}
label{
  margin-left: 40px;
  margin-right: 20px;
  font-size: 20px;
  font-weight: 600;
}

</style>