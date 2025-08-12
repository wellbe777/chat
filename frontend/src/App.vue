<template>
  <Navigation/>
  <router-view></router-view>
</template>

<script>
import Navigation from './components/Navigation.vue'
export default {
  name: 'App',
  components: {Navigation}
}
</script>


<style>
body {
  animation: fadeInAnimation ease .5s;
  animation-iteration-count: 1;
  animation-fill-mode: forwards;
  width: 100%;
  height: 100%;
  background-color: var(--background-color) !important;
  background-image: linear-gradient(0deg, transparent 24%, var(--background-image-color) 25%, var(--background-image-color) 26%, transparent 27%,transparent 74%, var(--background-image-color) 75%, var(--background-image-color) 76%, transparent 77%,transparent),
      linear-gradient(90deg, transparent 24%, var(--background-image-color) 25%, var(--background-image-color) 26%, transparent 27%,transparent 74%, var(--background-image-color) 75%, var(--background-image-color) 76%, transparent 77%,transparent);
  background-size: 55px 55px;
}

@keyframes fadeInAnimation {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}
</style>
