<template>
    <div class="info-container">
      <h1 class="title-text">{{ $t('404_not_found_title') }}</h1>
      <p class="info-text">{{ $t('404_page_not_found') }}</p>
      <div class="d-flex justify-content-center">
            <button type="submit" v-on:click="redirect" class="btn btn-primary"> {{ $t('redirect_to_main') }} </button>
        </div>
    </div>
  </template>
  
<script>
import { useCookies } from "vue3-cookies";
export default {
    name: 'NotFound',
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