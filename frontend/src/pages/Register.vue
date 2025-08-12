<template>
    <div class="auth-container">
    <form class="auth-form" ref="registerRef" @submit.prevent="onSubmit">
        <p class="main-text">{{ $t('register_page') }}</p>
        <div class="alert alert-danger" role="alert" v-if="error">{{ error }}</div>
        <div class="form-floating">
            <input type="text" v-model="username"  class="form-control user-input" id="floatingUsername" placeholder="Username" autocomplete="new-password" required>
            <label for="floatingUsername" class="label">{{ $t('username') }}</label>
        </div>
        <div class="form-floating">
            <input type="email" v-model="email" class="form-control user-input" id="floatingEmail" placeholder="Email" autocomplete="new-password" required>
            <label for="floatingEmail" class="label">{{ $t('email') }}</label>
        </div>
        <div class="form-floating">
            <input type="password" v-model="password" class="form-control user-input" id="floatingPassword" placeholder="Password" autocomplete="new-password" required>
            <label for="floatingPassword" class="label">{{ $t('password') }}</label>
        </div>
        <div class="d-flex justify-content-center">
            <button type="submit" v-on:click="register" class="btn btn-primary"> {{ $t('register') }} </button>
        </div>
        <a type="button" v-on:click="this.$router.push('/login')" class="underline-text">{{ $t('already_have_acc') }}</a>
    </form>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Register',
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
        if (!this.$refs.registerRef.checkValidity()) {
            this.$refs.registerRef.reportValidity();
        }
        },
        async register() {
        if (!this.username || !this.email || !this.password) return; 
            axios.post("http://localhost:8000/api/register", {
                username: this.username,
                email: this.email,
                password: this.password,
            })
            .then(() => {
                this.$router.push("/login");
            })
            .catch((error) =>{
                const resp = error.response
                if (resp.status == 400) {
                    const data = resp.data
                    if (data.email && data.email[0]) {
                        this.error = data.email[0]
                    }
                    else if (data.username && data.username[0]) {
                        this.error = data.username[0]
                    } else {
                        this.error = t('unhandled_error')
                    }
                } else {
                        this.error = t('unhandled_error')
                }
            })
        }
    }
}
</script>