<v-card>
  <v-card-title dark
                style="background: linear-gradient(to right, #7C4DFF, #304FFE, #448AFF);">
    <v-icon dark>
      mdi-robot
    </v-icon>
    &nbsp;
    ชุดข้อมูลสอนบอทแมงโก้

    <v-spacer></v-spacer>

    <v-dialog
        v-model="dialogIntent"
        persistent
        max-width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            :hidden="!hiddenIntent"
            color="green accent-1"
            v-bind="attrs"
            v-on="on"
        >
          <v-icon left>
            mdi-pencil
          </v-icon>
          สร้าง Intent
        </v-btn>
      </template>
      <v-card>

        <v-toolbar flat
                   style="background: linear-gradient(90deg, rgba(252,117,149,1) 0%, rgba(255,16,117,1) 77%, rgba(255,67,118,1) 100%);"
                   dark>
          ชื่อ Intent
        </v-toolbar>

        <v-card-text>
          <div class="mb-2">
            <v-text-field
                v-model="nameIntent"
                label="ชื่อ Intent"
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
              @click="createIntent"
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
          :load-children="intents"
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
                      :loading="!spinIntent"
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
          เลือก Intent
        </div>

        <v-card
            class="pt-6 mx-auto"
            flat
            max-width="400"
        >
          <v-card-text>
            <div class="mb-2">

              <h3 class="text-h5 ">
                สร้างคำถาม (สิงที่จะสอน)
              </h3>

              <v-text-field
                  v-model="question"
                  :append-outer-icon="question ? 'mdi-send' : ''"
                  filled
                  clear-icon="mdi-close-circle"
                  clearable
                  label="คำถาม"
                  type="text"
                  :loading="!spinIntent"
                  @keyup.enter="sendQuestion"
                  @click:append-outer="sendQuestion"
              ></v-text-field>


              <div v-if="!selectedIntent">
                <h2>No Data</h2>
              </div>
              <v-combobox
                  v-else
                  v-model="selectedIntent.question"
                  :item="selectedIntent.question"
                  label="คำถามที่สอนไป"
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
            คำตอบ (สิ่งที่ให้บอทตอบ)
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
                label="คำตอบ"
                type="text"
                :loading="!spinIntent"
                @keyup.enter="sendAnswer"
                @click:append-outer="sendAnswer"
            ></v-text-field>


            <div v-if="!selectedIntent">
              <h2>No Data</h2>
            </div>
            <v-combobox
                v-else
                v-model="selectedIntent.answer"
                :item="selectedIntent.answer"
                label="คำตอบทั้งหมด"
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