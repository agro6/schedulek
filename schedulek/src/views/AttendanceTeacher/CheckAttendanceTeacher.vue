<template>
  <div class="check-options">
    <div class="date-dropdown-style">
    <select v-model="chosenDate">
      <option value="" disabled selected hidden>Date</option>
      <option value="2022-01-03">2022-01-03</option>
      <option value="2022-01-04">2022-01-04</option>
      <option value="2022-01-05">2022-01-05</option>
    </select>
    </div>
    
    <div class="lesson-dropdown-style">
      <select v-model="chosenLesson">
        <option value="" disabled selected hidden>Lesson</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
      </select>
    </div>

    <div class="class-dropdown-style">
      <select v-model="chosenClass">
        <option value="" disabled selected hidden>Class</option>
        <option value="1a">1a</option>
        <option value="1b">1b</option>
        <option value="2a">2a</option>
      </select>
    </div>

  </div>

</template>

<script>
export default {
  data() {
    return {
      chosenDate: '',
      chosenLesson: '',
      chosenClass: ''
    }
  }

}
</script>

<style scoped>
.check-options{
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
  border:0px;
  outline:0px;
  appearance: none;
}
select::-ms-expand {
    display: none;
}


</style>