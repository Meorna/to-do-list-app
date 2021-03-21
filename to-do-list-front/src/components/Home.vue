<template>
    <div class="row d-flex justify-content-center">
        <div class="col-md-10 mt-4">
            <div class="card-hover-shadow-2x mb-3 card">
                <div class="card-header-tab card-header">
                    <div class="card-header-title font-size-lg text-capitalize font-weight-normal">{{$store.getters.getUserData.username}}</div>
                </div>
                <div class="scroll-area-sm">
                    <div style="position: static;" class="ps ps--active-y">
                        <div class="ps-content">
                            <ul class=" list-group list-group-flush" v-for="(todolist,index) in todolists"  v-bind:index="index" v-bind:key="todolist.index">
                                <li class="list-group-item">
                                    <div class="todo-indicator bg-gradient"></div>
                                    <div class="widget-content p-0 ml-4">
                                        <div class="widget-content-wrapper">
                                            <div class="widget-content-left">
                                                <div class="widget-heading">{{ todolist.name }}
                                                </div>
                                                <div class="widget-subheading"><i>{{new Date(todolist.created_at).toDateString() }}</i></div>
                                            </div>
                                            <div class="widget-content-right">
                                                <router-link class="border-0 btn-transition btn btn-outline-info" :to="{path : '/tasks/' + index}"><font-awesome-icon icon="eye"/></router-link>
                                                <button class="border-0 btn-transition btn btn-outline-warning" v-b-modal.edit-list-modal v-on:click="editListId(index)"><font-awesome-icon icon="pencil-alt"/></button>
                                                <button class="border-0 btn-transition btn btn-outline-danger" v-on:click="deleteList(index)"><font-awesome-icon icon="trash"/></button>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="d-block text-center card-footer">
                    <button class="btn btn-txt" v-b-modal.add-list-modal><font-awesome-icon class="font" icon="plus"/> &nbsp;Add List</button>
                </div>
            </div>
        </div>
        <b-modal ref="addListModal"
                id="add-list-modal"
                title="Add a new list"
                hide-footer>
            <b-form @submit="onSubmitAddList" @reset="onResetAddList" class="w-100">
                <b-form-group id="form-title-add-group"
                            label="Title:"
                            label-for="form-title-add-input">
                    <b-form-input id="form-title-add-input"
                                type="text"
                                v-model="addListForm.name"
                                required
                                placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-button pill type="submit" variant="info" class="ml-4 mr-4">Submit</b-button>
                <b-button pill type="reset" variant="danger" class="ml-4">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="editListModal"
                id="edit-list-modal"
                title="Edit a list"
                hide-footer>
            <b-form @submit="onSubmitEditList" @reset="onResetEditList" class="w-100">
                <b-form-group id="form-title-edit-group"
                            label="Title:"
                            label-for="form-title-edit-input">
                    <b-form-input id="form-title-edit-input"
                                type="text"
                                v-model="editListForm.name"
                                required
                                placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-button pill type="submit" variant="info" class="ml-4 mr-4">Submit</b-button>
                <b-button pill type="reset" variant="danger" class="ml-4">Reset</b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                todolists: [],
                addListForm: {
                    name: '',
                    created_at: ''
                },
                editListForm: {
                    id: '',
                    name: ''
                },
            };
        },
        methods: {
            getTodolists() {
                const path = 'http://0.0.0.0:5001/lists';
                const auth = 'Bearer: ' + this.$store.getters.getJwtToken;
                axios.get(path, {headers: {Authorization: auth}})
                    .then((res) => {               
                        this.todolists = res.data.data;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },
            addList(payload) {
            const path = 'http://0.0.0.0:5001/lists';
            const auth = 'Bearer: ' + this.$store.getters.getJwtToken;
            axios.put(path, payload, {headers: {Authorization: auth}})
                .then(() => {
                    console.log("Add list in api")
                    this.getTodolists();
                })
                .catch((error) => {
                    console.log(error);
                    this.getTodolists();
                });
            },
            deleteList(todolist_id) {
                const path = 'http://0.0.0.0:5001/lists/' + todolist_id;
                const auth = 'Bearer: ' + this.$store.getters.getJwtToken;
                axios.delete(path, {headers: {Authorization: auth}})
                    .then(() => {
                        this.getTodolists();
                        console.log("Delete list " + todolist_id + " in api");
                    })
                    .catch((error) => {
                        console.error(error);
                        this.getTodolists();
                    });
            },
            editList(payload) {
                const path = 'http://0.0.0.0:5001/lists/' + this.editListForm.id;
                const auth = 'Bearer: ' + this.$store.getters.getJwtToken;
                axios.patch(path, payload, {headers: {Authorization: auth}})
                .then(() => {
                    console.log("Edit list " + payload.name + " in api")
                    this.getTodolists();
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getTodolists();
                });
            },
            initFormAddList() {
                this.addListForm.name = '';
            },
            onSubmitAddList(evt) {
                evt.preventDefault();
                this.$refs.addListModal.hide();
                const payload = {
                    name: this.addListForm.name,
                    created_at: new Date()
                };
                this.addList(payload);
                this.initFormAddList();
            },
            onResetAddList(evt) {
                evt.preventDefault();
                this.initFormAddList();
            },
            editListId(todolist_id) {
                this.editListForm.id = todolist_id;
            },
            initFormEditList() {
                this.editListForm.name = '';
            },
            onSubmitEditList(evt) {
                evt.preventDefault();
                this.$refs.editListModal.hide();
                const payload = {
                    name: this.editListForm.name,
                };
                this.editList(payload);
                this.initFormEditList();
            },
            onResetEditList(evt) {
                evt.preventDefault();
                this.initFormEditList();
            },
        },
        created() {
            this.getTodolists();
        },
    };
</script>

<style>
body {
    font-size: 1.5rem !important;
    background-image: linear-gradient(to top, #37ecba 0%, #72afd3 100%);
    background-size: 100% 300%;
}

.row {
    margin-right: auto !important;
    margin-left: auto !important;
}

.card {
    box-shadow: 0 0.46875rem 2.1875rem rgba(4, 9, 20, 0.03), 0 1rem 1.5rem rgba(4, 9, 20, 0.03), 0 0.25rem 0.53125rem rgba(4, 9, 20, 0.05), 0 0.125rem 0.1875rem rgba(4, 9, 20, 0.03);
    border-radius: 1em !important;
}

.card-header.card-header-tab .card-header-title {
    font-family: URW Chancery L, cursive !important;
    font-size: 3rem !important;
    text-align: center !important;
}

.scroll-area-sm {
    height: 28em;
    overflow-x: hidden
}

.ps-content {
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.list-group {
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    border-top: 1px solid rgba(0, 0, 0, 0.125);
}

.todo-indicator {
    position: absolute;
    width: 4px;
    height: 60%;
    border-radius: 0.3rem;
    left: 0.625rem;
    top: 20%;
    opacity: .6;
    transition: opacity .2s
}

.bg-gradient {
    background-image: linear-gradient(to top, #37ecba 0%, #72afd3 100%) !important
}

.widget-content .widget-content-wrapper {
    display: flex;
    align-items: center
}

.widget-heading {
    font-family: URW Chancery L, cursive !important;
    font-size: 2rem !important; 
}

.widget-subheading {
    color: #858a8e;
    font-size: 10px
}

.widget-content .widget-content-right {
    margin-left: auto
}

.btn-outline-warning:hover {
    color: #fff !important;
}

.btn-txt {
    font-family: URW Chancery L, cursive !important;
    font-size: 3rem !important;
}


.font {
   font-size: 2rem !important; 
}

.modal-title {
    font-family: URW Chancery L, cursive !important;
    font-size: 3rem !important;
}

.modal-content {
    border-radius: 1em !important;
}

.d-block {
   font-family: URW Chancery L, cursive !important;
    font-size: 2rem !important;

}
</style>