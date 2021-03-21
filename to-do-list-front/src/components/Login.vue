<template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header">
                    <div class="card-header-title font-size-lg text-capitalize font-weight-normal">Login</div>
                </div>
                <div class="scroll-area-sm-dis">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="text-center">
                            <div>
                                <label class="widget-heading">Username:</label>
                                <div class="control">
                                    <input type="txt" class="input is-large" id="username" v-model="username">
                                </div>
                            </div>
                            <div class="field">
                                <label class="widget-heading">Password:</label>
                                <div class="control">
                                    <input type="password" class="input is-large" id="password" v-model="password">
                                </div>
                            </div>
                            <div class="control">
                                <a class="btn btn-info" @click="authenticate">Login</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-block text-center card-footer">
                    <router-link class="btn btn-txt" to="/signup">Sign Up</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import md5 from 'js-md5'
    export default {
        data() {
            return {
                username: '',
                password: ''
            }
        },
        methods: {
            authenticate () {
                this.$store.dispatch('login', { username: this.username, password: md5(this.password) })
                    .then(() => this.$router.push('/'))
            },
        }
    };
</script>

<style>
.scroll-area-sm-dis {
    height: 12em;
    overflow-x: hidden
}
</style>