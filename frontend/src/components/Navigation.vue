<template>
<nav class="navbar navbar-light bg-transparent">
  <div class="container-fluid">
      <div class="d-flex justify-content-start">
        <button class="btn btn-primary" type="submit" v-on:click="changeLanguage">{{current_emoji}}</button>
      </div>
      <form class="d-flex justify-content-end">
          <p v-if="isChatPage" class="caption-text" style="margin: 14px 14px 0 0">{{$t('welcome', {username: username})}}</p>
          <button v-if="isChatPage" class="btn btn-primary" type="submit" v-on:click="logout">{{$t('logout')}}</button>
      </form>
  </div>
</nav>
</template>


<script>
import { useCookies } from "vue3-cookies";
import { ref, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
export default {
  name: "Navigation",
  data() {
    return {
        current_emoji: '🇬🇧'
    }
  },
  setup() {
    const route = useRoute();
    const isChatPage = ref(false);
    const username = ref("unknown");
    const { cookies } = useCookies()
    watchEffect(() => {
        isChatPage.value = route.path === '/chat';
        username.value = atob(cookies.get('signature'))
    });
    return { isChatPage, username };
  },
  created() {
      this.$i18n.locale = localStorage.getItem('currentLanguage') || 'ru'
      this.current_emoji = this.$i18n.locale == "en" && '🇬🇧' || '🇷🇺'
  },
  methods: {
    changeLanguage() {
      this.$i18n.locale = this.$i18n.locale == "en" && 'ru' || 'en'
      this.current_emoji = this.$i18n.locale == "en" && '🇬🇧' || '🇷🇺'
      localStorage.setItem('currentLanguage', this.$i18n.locale)
    },
    logout() {
        document.cookie = 'jwt=; path=/; Partitioned; expires=Thu, 01 Jan 1970 00:00:00 UTC; secure; samesite=None;'
        document.cookie = 'signature=; path=/; Partitioned; expires=Thu, 01 Jan 1970 00:00:00 UTC; secure; samesite=None;'
        this.$router.push("/")
    }
  },
}
</script>

<style scoped>

.caption-text {
  font-size: 1.2rem;
  color: #fff;
}

@media (max-width: 992px) {
    .navbar-collapse {
        display: flex;
        justify-content: space-between;
    }
}
</style>
