<template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header">
                    <div class="card-header-title font-size-lg text-capitalize font-weight-normal">Sign Up</div>
                </div>
                <div class="scroll-area-sm-dis">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="text-center">
                            <div>
                                <label class="widget-heading">Username:</label>
                                <div class="control">
                                    <input type="txt" class="input is-large" id="username" v-model="username" required>
                                </div>
                            </div>
                            <div class="field">
                                <label class="widget-heading">Password:</label>
                                <div class="control">
                                    <input type="password" class="input is-large" id="password" v-model="password" required>
                                </div>
                            </div>
                            <div class="control">
                                <a class="btn btn-info" @click="signup">Sign up</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-block text-center card-footer">
                    <router-link class="btn btn-txt" to="/login">Login</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import md5 from 'js-md5'
    import axios from 'axios';

    export default {
        data() {
            return {
                username: '',
                password: '',
            }
        },
        methods: {
            signup() {
                const path = 'http://0.0.0.0:5001/account';
                var user = { username: this.username, password: md5(this.password) };
                axios({method: 'post', url: path, data: user})
                    .then(() => {               
                        this.$store.dispatch('login', { username: this.username, password: md5(this.password) })
                            .then(() => this.$router.push('/'))
                    })
                    .catch((error) => {
                        console.error(error.message);
                    });
            }
        }
    };
</script>