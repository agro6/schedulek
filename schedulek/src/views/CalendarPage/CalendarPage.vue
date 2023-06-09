<template>
  <div class="schedule">
  <div class="table-container">
<table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Hour</th>
          <th>Subject</th>
          <th>Homework</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="(day, index) in schedule" :key="index">
          <tr :class="{'date-row': index === 0 || day.date !== schedule[index - 1].date}">
            <td>{{ day.date }}</td>
            <td></td>
            <td></td>
            <td></td>
          </tr>
          <tr v-for="lesson in day.lessons" :key="lesson.id">
            <td></td>
            <td>{{ convertHour(lesson.lesson_number) }}</td>
            <td>{{ lesson.subject }}</td>
            <td>{{ getHomeworkSummary(lesson.lesson_number, day.date) }}</td>
          </tr>
        </template>
      </tbody>
    </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CalendarPage',
  props: {
    studentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      schedule: [],
    mappedHours: [],
    homework: []
    };
  },
  async created() {
    try {
        const response = await fetch(`http://localhost:5000/lessons/11`);
        const data = await response.json();
        this.schedule = this.processScheduleData(data.lessons);
          const responseHrs = await fetch(`http://localhost:5000/lessons_hours`);
          const hours_data = await responseHrs.json();
          this.mappedHours = hours_data.hours;
          console.log(this.mappedHours);
        const homeworkResponse = await fetch(`http://localhost:5000/homework/11`);
        const homeworkData = await homeworkResponse.json();
        this.homework = homeworkData.homework;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    processScheduleData(lessons) {
      const schedule = [];
      let currentDate = null;
      let currentDay = null;

      lessons.forEach((lesson) => {
        if (lesson.date !== currentDate) {
          currentDate = lesson.date;
          currentDay = { date: currentDate, lessons: [] };
          schedule.push(currentDay);
        }
        currentDay.lessons.push(lesson);
      });

      return schedule;
    },
    getHomeworkSummary(lessonNumber, date) {
        if (this.homework && this.homework.length > 0) {
          const homework = this.homework.find(
            hw =>
              hw.lesson_number === lessonNumber &&
              hw.deadline_date === date
          );
          return homework ? homework.summary : '-';
        } else {
          return '-';
        }
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
};
</script>


<style scoped>
.table-container {
  margin-top: 20px;
  margin-left: 40px;
  margin-right: 230px;
  overflow-y:auto;
  height: calc(100vh - 370px);
  padding-right: 150px;
  width: 1000px;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  text-align: left;
  padding: 8px;
  background-color: white;
  font-weight: 600;
}

th {
  background-color: #FBEDF9;
  font-weight: 600;
}

/* width */
::-webkit-scrollbar {
  width: 20px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #D9D9D9;
  border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #2B6777;
  border-radius: 10px;
}

.date-row {
  background-color: #FBEDF9;
}

</style>
