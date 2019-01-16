<template>
    <div id="app" >
        <div class="nav-bar">
            <div class="nav-logo">
                <div class="logo">
                    <img class="logo" src="./assets/RSLogo.png">
                </div>
                <div class="logo_name">
                    Route <br />Scouts
                </div>
            </div>
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
        <div class="router-view-wrapper">
            <div class="router-view">
                <router-view />
            </div>
        </div>
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
}
.nav-bar {
    background: #84CF6A;
    height: 60px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    overflow: hidden;
  }
.nav-logo {
    float: left;
    margin-left: 10px;
    width:30%;
    height: 55px;
    padding: 5px;
    text-align: left;
}
.logo {
    float: left;
    width: 60px;
    height: auto;
}
.logo_name {
    float: left;
    color: white;
    font-size: 15px;
    padding: 5px;
    text-align: left;
    height: 50;
    font-weight: bold;
}
.nav-left {
    float: left;
    margin-left: 20px;
    width: 40%;
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
.router-view-wrapper {
    position: fixed;
    top: 60px;
    width: 100%;
    bottom: 0;
    left: 0;
    text-align: center;
}

</style>
