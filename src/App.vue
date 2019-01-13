<template>
    <div id="app" >
        <div class="nav-bar">
            <div class="nav-left">
                <nav>
                <router-link class="nav-left-link" to="/map">Map</router-link>
                <router-link class="nav-left-link" to="/analytics">Analytics</router-link>
                </nav>
            </div>
            <div class="nav-right">
                <nav>
                <router-link class="nav-right-link" to="/login">Login</router-link>
                <router-link class="nav-right-link" to="/accountmanager">Account Manager</router-link>
                </nav>
            </div>
        </div>
        <router-view/>
    </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
.nav-bar {
    background: linear-gradient(-90deg, #84CF6A, #16C0B0);
    height: 60px;
    margin-bottom: 15px;
    overflow: hidden;
  }
.nav-left {
    float: left;
    margin-left: 20px;
    width: 70%;
    height: 60px;
    padding: 12px;
    text-align: left;
}
.nav-left-link {
    padding: 15px;
    font-size: 25px;
    font-weight: bold;
    color: white;
    text-decoration: none;
}
.nav-left-link:hover {
    text-decoration: underline;
    color:#2c3e50;
}
.nav-right {
    float: right;
    margin-right: 10px;
}
.nav-right-link {
    color: white;
    text-decoration: none;
    padding: 5px;
}
.nav-right-link:hover {
    text-decoration: underline;
    color:#2c3e50;
}
</style>
