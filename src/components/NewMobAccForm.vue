<!-- NOT CURRENTLY IN USE. Remains of the account manager stuff from before -->
<template>
<div>
        <h3>Create New Account:</h3>
        <form class="new-account-form" @submit.prevent="onSubmit">
        <p v-if="errors.length">
            <b>Please correct the following error(s):</b>
            <ul>
                <li :v-for="error in errors">{{ error }}</li>
            </ul>
        </p>
        <p>
            <label for="crewName">Crew Name:</label>
            <input id="crewName" v-model="crewName">
        </p>
        <p>
            <label>Crew Lead:</label><br>
            <label for="crewLeadFirst">First Name:</label>
            <input id="crewLeadFirst" v-model="crewLeadFirst">
            <label for="crewLeadLast">Last Name:</label>
            <input id="crewLeadLast" v-model="crewLeadLast">
            <label for="crewLeadID">ID:</label>
            <input id="crewLeadID" v-model="crewLeadID">
        </p>
        <p>
          <label for="crewSize">Number of members:</label>
          <input type="number" id="crewSize" v-model="crewSize" value="0" />
        </p>
        <p>
            <label for="crewTools">Tools and Supplies:</label>
            <textarea id="crewTools" v-model="crewTools"></textarea>
        </p>
        <p>
        <input type="submit" value="Submit">
        </p>
        </form>
      </div>
</template>

<script>
export default {
  name: 'mobileAccountForm',
  data () {
    return {
      msg: '' ,
      errors: [] 
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.new-account-form {
  text-align: left;
}
</style>
