{% extends "layout.html" %}
{% block content %}

<div id="app">
<v-app id="inspire" style="font-family: 'Prompt', sans-serif; background: #F5F5F5">
  <!-- contents -->
  <br><br>
  <v-container>
    <v-card>
      <v-card-title class="success white--text text-h5">
        <v-icon dark>
          mdi-robot
        </v-icon>
        &nbsp;
        Dataset Train Bot

        <v-spacer></v-spacer>


        <v-dialog
            v-model="dialogIntent"
            persistent
            max-width="500"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                :hidden="!hiddenIntent"
                color="warning"
                dark
                v-bind="attrs"
                v-on="on"
            >
              <v-icon left>
                mdi-pencil
              </v-icon>
              Create Intent
            </v-btn>
          </template>
          <v-card>

            <v-toolbar flat color="success" dark>
              Name Intent
            </v-toolbar>

            <v-card-text>
              <div class="mb-2">
                <v-text-field
                    v-model="nameIntent"
                    label="Name Intent"
                    clearable
                ></v-text-field>
              </div>


            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="red darken-1"
                  text
                  @click="dialogIntent = false"
              >
                Disagree
              </v-btn>
              <v-btn
                  color="green darken-1"
                  text
                  :loading="!spinIntent"
                  @click="addIntent"
              >
                Agree
              </v-btn>
            </v-card-actions>
          </v-card>

        </v-dialog>


      </v-card-title>


      <v-row
          class="pa-4"
          justify="space-between"
      >
        <v-col cols="5">
          <v-treeview
              :active.sync="active"
              :load-children="getIntents"
              :items="itemsIntent"
              :open.sync="open"
              activatable
              color="warning"
              open-on-click
              transition
          >
            <template v-slot:prepend="{ item }">
              <v-icon v-if="!item.children" color="warning">
                mdi-book
              </v-icon>
            </template>

            <template v-slot:append="{item}">

              <div v-if="!item.children">
                <v-dialog
                    v-model="dialogDeleteIntent"
                    persistent
                    max-width="290"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        class="mx-2"
                        fab
                        dark
                        x-small
                        color="red"
                        v-bind="attrs"
                        v-on="on"
                    >
                      <v-icon dark>
                        mdi-delete
                      </v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="text-h5">
                      are you sure ?
                    </v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                          color="green darken-1"
                          text
                          @click="dialogDeleteIntent = false"
                      >
                        Disagree
                      </v-btn>
                      <v-btn
                          color="red darken-1"
                          text
                          @click="deleteIntent(item)"
                      >
                        Agree
                      </v-btn>
                    </v-card-actions>
                  </v-card>

                </v-dialog>

              </div>


            </template>

          </v-treeview>
        </v-col>

        <v-divider vertical></v-divider>

        <v-col
            class="d-flex text-center"
        >
          <v-scroll-y-transition mode="out-in">
            <div
                v-if="!selectedIntent"
                class="text-h6 grey--text text--lighten-1 font-weight-light"
                style="align-self: center;"
            >
              Select a Intent
            </div>

            <v-card
                class="pt-6 mx-auto"
                flat
                max-width="400"
            >
              <v-card-text>
                <div class="mb-2">

                  <h3 class="text-h5 ">
                    Question ? (Training Set)
                  </h3>

                  <v-text-field
                      v-model="question"
                      :append-outer-icon="question ? 'mdi-send' : ''"
                      filled
                      clear-icon="mdi-close-circle"
                      clearable
                      label="Create Question"
                      type="text"
                      @click:append-outer="sendQuestion"
                  ></v-text-field>


                  <div v-if="!selectedIntent">
                    <h2>No Data</h2>
                  </div>
                  <v-combobox
                      v-else
                      v-model="selectedIntent.question"
                      :item="selectedIntent.question"
                      label="Trainset"
                      chips
                      multiple
                      readonly
                  >
                    <template v-slot:selection="{ item }">
                      <v-chip
                          class="ma-2"
                          close
                          @click:close="removeQuestion(item)"
                      >
                        [[item]]
                      </v-chip>
                    </template>
                  </v-combobox>
                </div>

              </v-card-text>
              <v-divider></v-divider>


              <h3 class="text-h5 ">
                Anwser
              </h3>
              <v-row
                  class="text-left"
                  tag="v-card-text"
              >
                <v-text-field
                    v-model="answer"
                    :append-outer-icon="answer ? 'mdi-send' : ''"
                    filled
                    clear-icon="mdi-close-circle"
                    clearable
                    label="Create Answer"
                    type="text"
                    @click:append-outer="sendAnswer"
                ></v-text-field>


                <div v-if="!selectedIntent">
                  <h2>No Data</h2>
                </div>
                <v-combobox
                    v-else
                    v-model="selectedIntent.answer"
                    :item="selectedIntent.answer"
                    label="Trainset"
                    chips
                    multiple
                    readonly
                >
                  <template v-slot:selection="{ item }">
                    <v-chip
                        class="ma-2"
                        close
                        @click:close="removeAnswer(item)"
                    >
                      [[item]]
                    </v-chip>
                  </template>
                </v-combobox>


              </v-row>
            </v-card>
          </v-scroll-y-transition>
        </v-col>
      </v-row>

    </v-card>
  </v-container>
</v-app>
</div>


<script>
const pause = ms => new Promise(resolve => setTimeout(resolve, ms))

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    hiddenIntent: false,
    nameIntent: '',
    dialogIntent: false,
    dialogDeleteIntent: false,
    question: '',
    answer: '',
    active: [],
    open: [],
    users: [],
    spinIntent: true,
    dataAppend: {
      id: '',
      uid: '',
      name: '',
      question: [],
      answer: [],
    }
  },
  computed: {
    itemsIntent() {
      return [
        {
          name: 'Your Intents',
          children: this.users,
        },
      ]
    },
    selectedIntent() {
      if (!this.active.length) return undefined
      const id = this.active[0]
      return this.users.find(user => user.id === id)
    },
  },
  methods: {
    async getIntents(item) {
      await pause(1500)
      const path = '/intent/data'
      return axios.get(path)
          .then((res) => {
            item.children.push(...res.data)
            this.hiddenIntent = true
          })
          .catch((err) => console.error(err))
    },
    addIntent() {
      this.spinIntent = false
      this.dataAppend.name = this.nameIntent
      console.log(this.dataAppend)
      const path = '/intent/add'
      axios.post(path, this.dataAppend)
          .then((res) => {
            this.spinIntent = true
            this.users.push(res.data)
            this.dialogIntent = false
          })
          .catch((err) => console.error(err))
    },
    deleteIntent(item) {
      const path = `/intent/delete_intent/${item.id}`
      axios.delete(path)
          .then((res) => {
            console.log(res.data)
            this.users.splice(this.users.indexOf(item), 1)
            this.dialogDeleteIntent = false
          })
          .catch((err) => console.error(err))

    },
    async sendQuestion() {
      this.selectedIntent.question.push(this.question)
      await this.updateIntent()
    },
    async sendAnswer() {
      this.selectedIntent.answer.push(this.answer)
      await this.updateIntent()
    },
    async removeAnswer(item) {
      this.selectedIntent.answer.splice(this.selectedIntent.answer.indexOf(item), 1)
      await this.updateIntent();
    },
    async removeQuestion(item) {
      this.selectedIntent.question.splice(this.selectedIntent.question.indexOf(item), 1)
      await this.updateIntent();
    },
    async updateIntent() {
      const path = '/intent/update_intent'
      await axios.post(path, this.selectedIntent)
          .then((res) => {
            this.question = ''
            this.answer = ''
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
    }
  },

  delimiters: ["[[", "]]"]
})


</script>


{% endblock %}