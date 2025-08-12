<template>
    <div class="auth-container">
    <form class="auth-form" ref="loginRef" @submit.prevent="onSubmit">
        <p class="main-text">{{ $t('login_page') }}</p>
        <div class="alert alert-danger" role="alert" v-if="error">{{ error }}</div>
        
        <div class="form-floating">
            <input type="text" v-model="username"  class="form-control user-input" id="floatingUsername" placeholder="Username" required>
            <label for="floatingUsername" class="label">{{ $t('username') }}</label>
        </div>
        <div class="form-floating">
            <input type="password" v-model="password" class="form-control user-input" id="floatingPassword" placeholder="Password" required>
            <label for="floatingPassword" class="label">{{ $t('password') }}</label>
        </div>
        <div class="d-flex justify-content-center">
            <button type="submit" v-on:click="login" class="btn btn-primary"> {{ $t('login') }} </button>
        </div>
        <a type="button" v-on:click="this.$router.push('/register')" class="underline-text">{{ $t('dont_have_acc') }}</a>
    </form>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Login',
    data() {
        return {
            username: '',
            email: '',
            password: '',
            error: ''
        }
    },
    methods: {
        onSubmit() {
        if (!this.$refs.loginRef.checkValidity()) {
            this.$refs.loginRef.reportValidity();
        }
        },
        async login() {
        this.onSubmit()
        if (!this.username || !this.password) return;
            axios.post("http://localhost:8000/api/login", {
                username: this.username,
                password: this.password,
            })
            .then(() => {
                this.$router.push("/chat");
            })
            .catch((error) =>{
                const resp = error.response
                if (resp.status == 403) {
                    this.error = resp.data.detail
                }
            })
        }
    }
}
</script>