<template>
    <div class="info-container">
      <h1 class="title-text">{{$t('homepage')}}</h1>
      <p class="info-text">{{ $t('just_the_home_page') }}</p>
      <div class="d-flex justify-content-center">
            <button type="submit" v-on:click="redirect" class="btn btn-primary"> {{$t('redirect_to_main')}} </button>
        </div>
    </div>
</template>

<script>
import { useCookies } from "vue3-cookies";
export default {
    name: "Home",
    methods: {
        redirect() {
            const { cookies } = useCookies()
            const token = cookies.get('jwt')
            this.$router.push(token ? "/chat" : "/login");
        },
        changeLocale(locale) {
            this.$i18n.locale = locale
        },
    },
};
</script>