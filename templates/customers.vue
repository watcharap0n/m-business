{% extends "layout.html" %}
{% block content %}

<div id="app">
<v-app id="inspire" style="font-family: 'Prompt', sans-serif; background: #F5F5F5">

  <!--  app-bar start  -->


  <v-card class="overflow-hidden">
    <v-app-bar
        :style="{background: `${showColor}`}"
        absolute
        dark
        dense
    >

      <v-app-bar-title>Mango BOT</v-app-bar-title>

      <v-switch
          style="margin-top: 25px; margin-left: 15px"
          v-model="$vuetify.theme.dark"
          inset
          label="Change Theme Dark"
      ></v-switch>

      <v-spacer></v-spacer>

      [[userAuth.name]]
      &nbsp;
      <v-menu
          bottom
          left
          transition="slide-y-transition"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              icon
              v-bind="attrs"
              v-on="on"
          >
            <v-avatar>
              <img
                  :loading="!spinAuth"
                  :src="[[userAuth.picture]]"
                  alt="John"
              >
            </v-avatar>
          </v-btn>
        </template>

        <v-list>
          <v-list-item @click="isProfile = true">
            <v-card
                class="mx-auto"
                max-width="434"
                tile
            >
              <v-avatar
                  class="profile"
                  color="grey"
                  size="250"
                  tile
              >
                <v-img :src="userAuth.picture">
                  <v-row
                      align="end"
                      class="fill-height"
                  >
                    <v-col
                        align-self="start"
                        class="pa-0"
                        cols="12"
                    >
                    </v-col>
                    <v-col class="py-0">
                      <v-list-item
                          color="rgba(0, 0, 0, .4)"
                          dark
                      >
                        <v-list-item-content>
                          <v-list-item-title class="text-h6">
                            [[userAuth.name]]
                          </v-list-item-title>
                          <v-list-item-subtitle>Email: [[userAuth.email]]</v-list-item-subtitle>
                          <v-spacer></v-spacer>
                          <v-btn text color="red" @click="logout">
                            <strong>Logout</strong>
                          </v-btn>
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                  </v-row>
                </v-img>
              </v-avatar>
            </v-card>
          </v-list-item>
        </v-list>
      </v-menu>
      &nbsp;&nbsp;

    </v-app-bar>


    <!--  app-bar end    -->

    <v-sheet
        id="scrolling-techniques"
        class="overflow-y-auto"
        max-height="1500"
    >
      <br><br><br>

      <v-container>
        <v-row class="text-center">

          <v-card class="mx-auto" class="elevation-1">

            <v-bottom-navigation
                v-model="page"
                :style="{background: `${showColor}`}"
                dark
                flat
                shift
                class="elevation-1"
            >
              <v-btn v-for="(v, i) in navigation" :key="i" @click="changeTransaction(v.href)">
                <v-badge
                    color="#FF648D"
                    :content="transaction.length"
                >
                  <span>[[v.header]]</span>
                </v-badge>
                <v-icon>[[v.icon]]</v-icon>
              </v-btn>

            </v-bottom-navigation>


            <!--     start table     -->

            <v-card-text>
              <v-data-table v-model="selected" :loading="!spinTable" show-select multi-sort :search="search"
                            :headers="headers"
                            :items="transaction">

                <!--       slot TOP         -->

                <template v-slot:top>
                  <v-toolbar flat>
                    <v-text-field
                        :loading="!spinTable"
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                    >
                    </v-text-field>
                    <v-spacer></v-spacer>

                    <v-btn
                        color="indigo accent-1"
                        class="mb-2"
                        :hidden="!btnImport"
                        @click="moveImport"
                        :loading="spinImport"
                    >
                      <v-icon left>mdi-application-import</v-icon>
                      Imports
                    </v-btn>

                    &nbsp;

                    <v-dialog
                        persistent
                        v-model="dialogCustomer"
                        max-width="650"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            color="green accent-1"
                            class="mb-2"
                            v-bind="attrs"
                            v-on="on"
                        >
                          <v-icon left>mdi-account-circle</v-icon>
                          Add Customer
                        </v-btn>
                      </template>
                      <v-card>
                        <v-toolbar class="elevation-1" flat color="green accent-1">
                          <v-card-title>
                            <v-icon medium style="margin-right: 10px">mdi-account-circle
                            </v-icon>
                            <h3>[[ formTitle ]]</h3>
                          </v-card-title>
                        </v-toolbar>
                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col
                                  cols="12"
                                  sm="6"
                                  md="4"
                              >
                                <v-text-field
                                    prepend-inner-icon="mdi-account"
                                    v-model="editedItem.name"
                                    label="Name"
                                    outlined
                                    dense
                                ></v-text-field>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="6"
                                  md="4"
                              >
                                <v-select
                                    prepend-inner-icon="mdi-post-outline"
                                    v-model="editedItem.product"
                                    :items="productMango"
                                    label="Product"
                                    outlined
                                    dense
                                ></v-select>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="6"
                                  md="4"
                              >
                                <v-text-field
                                    v-model="editedItem.email"
                                    label="Email"
                                    prepend-inner-icon="mdi-email"
                                    outlined
                                    dense
                                ></v-text-field>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="6"
                                  md="4"
                              >
                                <v-text-field
                                    v-model="editedItem.tel"
                                    label="Tel"
                                    prepend-inner-icon="mdi-card-account-phone"
                                    outlined
                                    dense
                                ></v-text-field>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="6"
                                  md="4"
                              >
                                <v-text-field
                                    prepend-inner-icon="mdi-office-building"
                                    v-model="editedItem.company"
                                    label="Company"
                                    outlined
                                    dense
                                ></v-text-field>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="6"
                                  md="4"
                              >
                                <v-text-field
                                    v-model="editedItem.channel"
                                    prepend-inner-icon="mdi-access-point-check"
                                    label="Channel"
                                    outlined
                                    dense
                                ></v-text-field>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="12"
                                  md="12"
                              >
                                <v-textarea
                                    prepend-inner-icon="mdi-android-messages"
                                    v-model="editedItem.message"
                                    label="Message"
                                    outlined
                                    dense
                                ></v-textarea>
                              </v-col>
                              <v-col
                                  cols="12"
                                  sm="12"
                                  md="12"
                              >
                                <v-autocomplete
                                    prepend-inner-icon="mdi-tag"
                                    v-model="editedItem.tag"
                                    :items="itemsTag"
                                    outlined
                                    dense
                                    chips
                                    small-chips
                                    label="Tags"
                                    multiple
                                ></v-autocomplete>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                              color="error"
                              text
                              @click="close"
                          >
                            ยกเลิก
                          </v-btn>
                          <v-btn
                              color="success"
                              text
                              @click="save"
                              :loading="!spinButton"
                          >
                            บันทึก
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>


                    <v-dialog v-model="dialogDelete" max-width="500px">
                      <v-card>
                        <v-card-title class="text-h5">คุณแน่ใจว่าจะลบข้อมูล ?</v-card-title>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="success" text @click="closeDelete">ยกเลิก</v-btn>
                          <v-btn color="error" text @click="deleteItemConfirm"
                                 :loading="!spinButton">ตกลง
                          </v-btn>
                          <v-spacer></v-spacer>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-toolbar>


                  <!-- tag start -->

                  <v-toolbar flat>
                    <v-btn
                        elevation="3"
                        :loading="!spinTag"
                        :disabled="!btnTag"
                        medium
                        small
                        color="#FF648D"
                        dark
                        @click="tagTransaction(selected)"
                    ><i class="fas fa-user-tag"></i>
                    </v-btn>

                    <div class="small" style="margin-left: 10px; margin-top: 23px; margin-right: 20px">
                      <v-combobox
                          :loading="!spinTable"
                          v-model="model"
                          :filter="filter"
                          :hide-no-data="!searchTag"
                          :items="itemsTag"
                          :search-input.sync="searchTag"
                          hide-selected
                          label="แท็ก"
                          multiple
                          dense
                          small-chips

                      >
                        <template v-slot:no-data>
                          <v-list-item>
                            <v-icon color="green">mdi-arrow-right-thick</v-icon>
                            <span class="subheading">สร้าง</span>&nbsp;&nbsp;
                            <v-chip
                                style="color: white"
                                color="pink lighten-2"
                                label
                                small
                            >
                              [[ searchTag ]]
                            </v-chip>
                          </v-list-item>
                        </template>
                        <template v-slot:selection="{ attrs, item, parent, selected, index}">
                          <v-chip
                              v-if="index < 2"
                              v-if="item === Object(item)"
                              v-bind="attrs"
                              color="pink lighten-2"
                              :input-value="selected"
                              label
                              small
                              close
                              close-icon="mdi-delete"
                              @click:close="parent.selectItem(item)"
                          >
                      <span class="pr-2" style="color: white">
                        [[ item.text ]]
                      </span>
                          </v-chip>
                          <span v-if="index === 1"
                                class="grey--text caption">(+[[ model.length - 1 ]] แท็กอื่นๆ)
                    </span>
                        </template>

                        <template v-slot:item="{ index, item }">
                          <v-text-field
                              v-if="editingTag === item"
                              v-model="editingTag.text"
                              autofocus
                              flat
                              background-color="transparent"
                              hide-details
                              solo
                              @keyup.enter="edit(index, item)"
                          ></v-text-field>
                          <v-chip
                              v-else
                              color="pink lighten-2"
                              dark
                              label
                              small
                          >
                            [[ item.text ]]
                          </v-chip>
                          <v-spacer></v-spacer>
                          <v-list-item-action @click.stop>
                            <v-row>
                              <v-col>
                                <v-btn
                                    icon
                                    @click.stop.prevent="edit(index, item)"
                                >
                                  <v-icon color="teal">[[ editingTag !== item ? 'mdi-pencil' : 'mdi-check' ]]</v-icon>
                                </v-btn>
                              </v-col>
                              <v-col>
                                <v-btn
                                    icon
                                    @click.stop.prevent="toRemove(index, item)"
                                >
                                  <v-icon color="red">mdi-delete</v-icon>
                                </v-btn>
                              </v-col>
                            </v-row>
                          </v-list-item-action>
                        </template>
                      </v-combobox>

                    </div>


                  </v-toolbar>


                  <!--tag end-->


                </template>

                <template v-slot:item.tag="{item}">
                  <v-chip v-for="i in item.tag" :key="i.length">
                    #[[i ]]
                  </v-chip>
                </template>

                <template v-slot:item.name="{item}">
                  <div style="margin-top: 15px; margin-bottom: 15px">
                    <v-row>
                      <v-col>
                        <strong>[[item.name ]]</strong>
                        <span>[[item.email ]]</span>
                        <span>[[item.tel ]]</span>
                      </v-col>
                    </v-row>
                  </div>
                </template>

                <template v-slot:item.product="{item}">
                  <v-chip class="ma-2" :color="colorProduct(item.product)" label>
                    [[item.product ]]
                  </v-chip>
                </template>

                <template v-slot:item.message="{item}">
                  <v-list-group
                      color="#7A8FC0"
                      v-if="item.message"
                      :value="false"
                      prepend-icon="mdi-message"
                  >
                    <v-list-item-content>
                      [[item.message]]
                    </v-list-item-content>
                  </v-list-group>
                  <div v-else></div>
                </template>

                <template v-slot:item.channel="{item}">
                  <v-chip outlined>
                    [[item.channel ]]
                  </v-chip>
                </template>

                <template v-slot:item.date="{item}">
                  [[ item.date ]]
                  <v-divider></v-divider>
                  [[ item.time ]]
                </template>

                <template v-slot:item.actions="{item}">
                  <v-icon small class="mr-2" color="light-blue lighten-1" @click="editItem(item)">
                    mdi-pencil
                  </v-icon>
                  <v-icon small color="red" @click="deleteItem(item)">
                    mdi-delete
                  </v-icon>
                </template>

                <template v-slot:no-data>
                  <v-btn
                      color="green accent-1"
                      @click="initialize"
                  >
                    Reset
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-row>


        <v-snackbar
            dark
            :color="colorSb"
            v-model="snackbar"
            :timeout="timeout"
        >
          [[text ]]

          <template v-slot:action="{ attrs }">
            <v-btn
                dark
                text
                v-bind="attrs"
                @click="snackbar = false"
            >
              ปิด
            </v-btn>
          </template>
        </v-snackbar>

        <!--    end table     -->


        <!-- start stepper create webhook  -->
        <br>
        <br>
        <v-row>

          <v-col cols="2">
            <v-card
                class="mx-auto"
                max-width="500"
            >
              <v-list>
                <v-list-item-group v-model="modelList">
                  <v-list-item
                      v-for="(item, i) in items"
                      :key="i"
                      @click="listModel(item.text)"
                  >
                    <v-list-item-icon>
                      <v-icon v-text="item.icon"></v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title v-text="item.text"></v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-col>

          <v-col cols="10">


            <div :hidden="!showWebhook">
              <v-toolbar
                  :style="{background: `${showColor}`}"
                  dark
              >
                <v-icon>mdi-account</v-icon>
                <v-toolbar-title class="font-weight-light">
                  Create Webhook
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn
                    color="green accent-1"
                    fab
                    dark
                    small
                    @click="isEditing = !isEditing"
                >
                  <v-icon v-if="isEditing">
                    mdi-close
                  </v-icon>
                  <v-icon v-else>
                    mdi-pencil
                  </v-icon>
                </v-btn>
              </v-toolbar>
              <v-card-text>
                <v-form v-model="validWebhook" ref="formWebhook"
                        lazy-validation>
                  <v-text-field
                      required
                      :rules="rules"
                      v-model="ACCESS_TOKEN"
                      :disabled="!isEditing"
                      label="Channel Access Token"
                  ></v-text-field>

                  <v-text-field
                      required
                      :rules="rules"
                      v-model="SECRET_LINE"
                      :disabled="!isEditing"
                      label="Channel secret"
                  ></v-text-field>

                  <v-subheader>
                    <strong> Your Webhook URL: </strong> &nbsp;&nbsp; [[webhook]]
                  </v-subheader>

                </v-form>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    :loading="!spinWebhook"
                    :disabled="!isEditing"
                    :hidden="!validWebhook"
                    color="success"
                    @click="saveWebhook"
                >
                  Save
                </v-btn>
              </v-card-actions>
              <v-snackbar
                  v-model="hasSaved"
                  :timeout="2000"
                  absolute
                  bottom
                  left
              >
                Your Create Webhook!
              </v-snackbar>
            </div>

            <!--            start intent-->

            <div :hidden="!showIntent">


              <v-card>
                <v-card-title dark :style="{background: `${showColor}`}">
                  <v-icon dark>
                    mdi-robot
                  </v-icon>
                  &nbsp;
                  Dataset Train Bot

                  <v-spacer></v-spacer>
                  <v-dialog
                      v-model="dialogAcesstoken"
                      persistent
                      max-width="500"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                          color="green accent-1"
                          :hidden="!hiddenAccess"
                          v-bind="attrs"
                          v-on="on"
                      >
                        <v-icon left>
                          mdi-pencil
                        </v-icon>
                        Channel Access Token
                      </v-btn>
                    </template>
                    <v-card>

                      <v-toolbar flat color="success" dark>
                        Access Token
                      </v-toolbar>

                      <v-card-text>
                        <div class="mb-2">
                          <v-form v-model="validAccess" ref="formAccess">
                            <v-textarea
                                v-model="nameAccestoken"
                                :rules="rules"
                                label="Your Access Token"
                                clearable
                            ></v-textarea>
                          </v-form>
                        </div>


                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="red darken-1"
                            text
                            @click="dialogAcesstoken = false"
                        >
                          Disagree
                        </v-btn>
                        <v-btn
                            color="green darken-1"
                            text
                            :disabled="!validAccess"
                            :loading="!spinIntent"
                            @click="formAccessToken"
                        >
                          Agree
                        </v-btn>
                      </v-card-actions>
                    </v-card>

                  </v-dialog>


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
                        :hidden="!treeHidden"
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
                                :loading="!spinIntent"
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
                              :loading="!spinIntent"
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


            </div>

            <!--  end intent  -->


            <!--  start  color-->
            <div :hidden="!showMyColor">
              <v-row>

                <v-col
                    class="d-flex justify-center"
                >
                  <v-color-picker v-model="color"></v-color-picker>
                </v-col>

                <v-col
                    cols="12"
                    md="4"
                >
                  <v-sheet
                      class="pa-4"
                  >

                    <pre>[[ showColor ]]</pre>


                    <v-btn
                        color="green accent-1"
                        @click="saveColor"
                    >
                      บันทึกจดจำค่าสี

                    </v-btn>
                  </v-sheet>
                </v-col>
              </v-row>
            </div>
            <!-- end color -->

          </v-col>
        </v-row>
        <br><br><br><br>
        <!-- end stepper create webhook -->
      </v-container>
    </v-sheet>
  </v-card>
</v-app>
</div>


<script>
const pause = ms => new Promise(resolve => setTimeout(resolve, ms))
new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    // start var table
    page: 0,
    navigation: [
      {
        header: 'Customers',
        href: 'customers',
        icon: 'mdi-account-supervisor-circle'
      },
      {
        header: 'Imports',
        href: 'imports',
        icon: 'mdi-import'
      },
    ],
    headers: [
      {
        text: 'Actions',
        value: 'actions',
        sortable: false,
        width: 80
      },
      {
        text: 'Tag',
        value: 'tag',
        width: 100,
      },
      {
        text: 'Product',
        value: 'product',
        width: 155,
        align: 'start'
      },
      {
        text: 'User Info',
        value: 'name',
        align: 'center'
      },
      {
        text: 'Company',
        value: 'company',
      },
      {
        text: 'Message',
        value: 'message'
      },
      {
        text: 'Channel',
        value: 'channel'
      },
      {
        text: 'Data/Time',
        value: 'date',
        align: 'center',
      },

    ],
    editedItem: {
      tag: [],
      product: '',
      name: '',
      email: '',
      tel: '',
      company: '',
      channel: '',
      message: '',
    },
    defaultItem: {
      tag: [],
      product: '',
      name: '',
      email: '',
      tel: '',
      company: '',
      channel: '',
      message: '',
    },
    search: '',
    transaction: [],
    selected: [],
    spinButton: true,
    imgError: false,
    spinTable: false,
    dialogCustomer: false,
    dialogDelete: false,
    editedIndex: -1,
    snackbar: false,
    btnImport: false,
    spinImport: false,
    timeout: 2000,
    colorSb: '',
    text: '',
    path: '',
    href: '',
    isProfile: false,
    productMango: ['RealEstate', 'Construction', 'BI Dashboard', 'Project Planning', 'CSM', 'QCM', 'Maintenance', 'Rental', 'MRP'],

    //  end var table


    // start tag

    itemsTag: [],
    searchTag: null,
    editingTag: null,
    colorsTag: 'pink',
    model: [],
    btnTag: false,
    spinTag: true,
    // end tags


    // start webhook
    hasSaved: false,
    isEditing: null,
    ACCESS_TOKEN: '',
    SECRET_LINE: '',
    validWebhook: false,
    webhook: '',
    spinWebhook: true,
    rules: [v => !!v || 'require!'],


    //end webhook

    // socket auth

    userAuth: {
      name: '',
      picture: '',
      email: '',
      uid: '',
    },
    spinAuth: false,


    // item location

    items: [
      {
        icon: 'mdi-inbox',
        text: 'Webhook',
      },
      {
        icon: 'mdi-star',
        text: 'Train BOT',
      },
      {
        icon: 'mdi-format-color-fill',
        text: 'Color'
      }
    ],
    modelList: 0,
    showWebhook: true,
    showIntent: false,
    showMyColor: false,
    // end location


    // color
    types: ['hex', 'hexa', 'rgba', 'hsla', 'hsva'],
    type: 'hex',
    hex: '#000000',
    hexa: '#FF00FFFF',
    rgba: {r: 255, g: 0, b: 255, a: 1},
    hsla: {h: 300, s: 1, l: 0.5, a: 1},
    hsva: {h: 300, s: 1, v: 1, a: 1},
    //end color


    // start intent
    treeHidden: false,
    hiddenIntent: false,
    hiddenAccess: true,
    nameIntent: '',
    nameAccestoken: '',
    validAccess: false,
    dialogIntent: false,
    dialogDeleteIntent: false,
    dialogAcesstoken: false,
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
      access_token: '',
    }



    // end intent
  },
  watch: {
    model(val, prev) {
      if (val.length === prev.length) return
      this.model = val.map(v => {
        if (typeof v === 'string') {
          v = {
            text: v,
            color: this.colorsTag
          }
          this.addTag(v)
          this.nonce++
        }
        return v
      })
      if (this.model.length > 0 && this.selected.length > 0) {
        this.btnTag = true
      } else if (this.model.length === 0) {
        this.btnTag = false
      }

    },

    selected() {
      if (this.selected.length === 0) {
        this.btnTag = false

      } else if (this.selected.length > 0 && this.model.length > 0) {
        this.btnTag = true
      }
    },
  },
  beforeCreate() {
    const path = '/secure/socket_auth'
    axios.get(path)
        .then((res) => {
          let user = this.userAuth
          user.name = res.data.name
          user.picture = res.data.picture
          user.email = res.data.email
          user.uid = res.data.uid
        })
  }
  ,
  created() {
    this.getColorCookie();
    this.initialize();
    this.getTags();
  }
  ,
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Customer' : 'Edit Customer'
    },
    color: {
      get() {
        return this[this.type]
      },
      set(v) {
        this[this.type] = v
      },
    },
    showColor() {
      if (typeof this.color === 'string') return this.color

      return JSON.stringify(Object.keys(this.color).reduce((color, key) => {
        color[key] = Number(this.color[key].toFixed(2))
        return color
      }, {}), null, 2)
    },

    // start intent

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


  }
  ,
  mounted() {
    window.addEventListener('keyup', function (event) {
      if (event.key === 'Enter')
        console.log('this is Enter')
    }) // function KeyBoard
  },
  methods: {
    //test


    // start method table

    initialize() {
      this.spinTable = false
      const path = '/api/customer'
      axios.get(path)
          .then((res) => {
            this.spinTable = true;
            this.transaction = res.data;
            this.href = 'customer'
            this.btnImport = false
          })
          .then((err) => {
            console.log(err)
          })
    }
    ,
    APIImport() {
      this.spinTable = false
      const path = '/api/import'
      axios.get(path)
          .then((res) => {
            this.spinTable = true;
            this.transaction = res.data;
            this.href = 'import'
            this.btnImport = true
          })
          .then((err) => {
            console.log(err)
          })
    }
    ,
    async moveImport() {
      if (this.selected.length > 0) {
        this.spinImport = true
        const path = '/api/move/customer'
        await axios.post(path, this.selected)
            .then((res) => {
              this.selected.forEach((data) => {
                this.transaction.splice(this.transaction.indexOf(data), 1)
              })
              this.spinImport = false
              this.text = `คุณได้ทำการย้ายข้อมูลไปหน้า customers แล้ว!`
              this.colorSb = 'success'
              this.snackbar = true
              this.selected = []
            })
            .catch((err) => {
              console.log(err);
            })
      } else {
        this.colorSb = 'error'
        this.text = 'กรุณาเลือกข้อมูลที่จะต้องทำการย้าย!'
        this.snackbar = true

      }
    }
    ,
    changeTransaction(data) {
      if (data === 'imports') {
        this.APIImport()
      } else if (data === 'customers') {
        this.initialize()
      }
    }
    ,
    colorProduct(product) {
      if (product === 'Construction') {
        return 'green accent-1'
      }
      if (product === 'RealEstate') {
        return 'light-blue accent-1'
      }
      if (product === 'Project Planning') {
        return 'red accent-1'
      }
    }
    ,
    async addTransaction(data) {
      let href = this.href
      if (href === 'customer')
        this.path = '/api/customer'
      if (href === 'import')
        this.path = '/api/import'
      await axios.post(this.path, data)
          .then((res) => {
            this.spinButton = true;
            this.transaction.unshift(res.data);
            this.text = `คุณได้เพิ่มข้อมูล ${this.editedItem.name}`
            this.colorSb = 'success'
            this.snackbar = true
          })
          .catch((err) => {
            console.log(err);
          })
    }
    ,
    async editTransaction(data, id) {
      let href = this.href
      if (href === 'customer')
        this.path = `/api/customer/${id}`
      if (href === 'import')
        this.path = `/api/import/${id}`
      await axios.put(this.path, data)
          .then(() => {
            this.spinButton = true;
            this.colorSb = 'primary'
            this.text = `คุณได้อัพเดทข้อมูล ${this.editedItem.name}`
            this.snackbar = true
          })
          .catch((err) => {
            console.log(err);
          })
    }
    ,
    async deleteTransaction(id) {
      let href = this.href
      if (href === 'customer')
        this.path = `/api/customer/${id}`
      if (href === 'import')
        this.path = `/api/import/${id}`
      await axios.delete(this.path)
          .then((res) => {
            this.spinButton = true;
            console.log(res.data);
            this.colorSb = 'red'
            this.text = `คุณได้ลบข้อมูล ${this.editedItem.name}`
            this.snackbar = true
          })
          .catch((err) => {
            console.log(err);
          })
    }
    ,
    editItem(item) {
      console.log(this.href)
      this.editedIndex = this.transaction.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogCustomer = true;
    }
    ,
    deleteItem(item) {
      this.editedIndex = this.transaction.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    }
    ,
    async deleteItemConfirm() {
      this.spinButton = false;
      await this.deleteTransaction(this.editedItem.id);
      this.transaction.splice(this.editedIndex, 1);
      this.closeDelete()
    }
    ,
    close() {
      this.dialogCustomer = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    }
    ,
    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    }
    ,
    async save() {
      if (this.editedIndex > -1) {
        this.spinButton = false;
        let data = Object.assign(this.transaction[this.editedIndex], this.editedItem);
        await this.editTransaction(data, data.id);
      } else {
        this.spinButton = false;
        await this.addTransaction(this.editedItem);
      }
      this.close()
    }
    ,

    //  end method table


    // start method tags

    getTags() {
      const path = '/api/tag'
      axios.get(path)
          .then((res) => {
            this.itemsTag = res.data
          })
          .catch((err) => {
            console.error(err)
          })
    }
    ,


    filter(item, queryText, itemText) {
      const hasValue = val => val != null ? val : ''
      const text = hasValue(itemText)
      const query = hasValue(queryText)
      return text.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
    }
    ,

    edit(index, item) {
      if (!this.editingTag) {
        this.editingTag = item
        this.editingIndexTag = index

      } else {
        this.setTag(item.id, this.editingTag)
        this.editingTag = null
        this.editingIndexTag = -1
      }
    }
    ,

    addTag(item) {
      const path = `/api/tag?tag=${item.text}`
      axios.get(path)
          .then(() => {
            this.getTags()
            console.log('success')
          })
          .catch((err) => {
            console.error(err)
          })
    }
    ,

    setTag(id, item) {
      const path = `/api/tag/${item}?id-query=${id}`;
      axios.put(path)
          .then(() => {
            console.log('success')
          })
          .catch((error) => {
            console.error(error)
          })
    }
    ,

    toRemove(index, item) {
      this.itemsTag.splice(this.itemsTag.indexOf(item), 1)
      this.removeTag(item.id)
    }
    ,

    removeTag(id) {
      console.log(id)
      const path = `/api/tag?id-query=${id}`;
      axios.delete(path)
          .then(() => {
            this.getTags()
            console.log('success')
          })
          .catch((error) => {
            console.error(error)
          })
    }
    ,

    tagTransaction(selected) {
      this.spinTag = false
      let data = {'id': selected, 'tag': this.model}
      const path = '/api/tag'
      axios.post(path, data)
          .then((res) => {
            this.spinTag = true
            this.initialize()
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err)
          })
    },


    // end tag

    // start webhook

    saveWebhook() {
      this.spinWebhook = false
      let form = this.$refs.formWebhook.validate();
      if (form === true) {
        let data = {ACCESS_TOKEN: this.ACCESS_TOKEN, SECRET_LINE: this.SECRET_LINE}
        const path = '/callback/save'
        axios.post(path, data)
            .then((res) => {
              this.webhook = res.data.webhook
              this.hasSaved = true;
              this.spinWebhook = true
            })
            .catch((err) => {
              console.error(err)
            })
      }
    }
    ,

    // end webhook

    logout() {
      return window.location = '/secure/logout'
    }
    ,

    // start intent

    formAccessToken() {
      this.hiddenAccess = false
      this.dialogAcesstoken = false
      this.treeHidden = true
    },
    async getIntents(item) {
      await pause(1500)
      let data = {'access_token': this.nameAccestoken}
      const path = `/intent/data/?access_token=${this.nameAccestoken}`
      return axios.post(path, data)
          .then((res) => {
            item.children.push(...res.data)
            this.hiddenIntent = true
          })
          .catch((err) => console.error(err))
    },
    addIntent() {
      this.spinIntent = false
      this.dataAppend.name = this.nameIntent
      this.dataAppend.uid = this.userAuth.uid
      this.dataAppend.access_token = this.nameAccestoken
      console.log(this.dataAppend)
      const path = '/intent/add'
      axios.post(path, this.dataAppend)
          .then((res) => {
            this.nameIntent = ''
            this.spinIntent = true
            this.users.push(res.data)
            this.dialogIntent = false
          })
          .catch((err) => console.error(err))
    },
    deleteIntent(item) {
      this.spinIntent = false
      const path = `/intent/delete_intent/${item.id}`
      axios.delete(path)
          .then((res) => {
            console.log(res.data)
            this.users.splice(this.users.indexOf(item), 1)
            this.dialogDeleteIntent = false
            this.spinIntent = true
          })
          .catch((err) => console.error(err))

    },
    async sendQuestion() {
      this.spinIntent = false
      this.selectedIntent.question.push(this.question)
      await this.updateIntent()
      this.spinIntent = true
    },
    async sendAnswer() {
      this.spinIntent = false
      this.selectedIntent.answer.push(this.answer)
      await this.updateIntent()
      this.spinIntent = true
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
    },


    // end intent

    // listModel
    listModel(data) {
      if (data === 'Webhook') {
        this.showIntent = false
        this.showMyColor = false
        this.showWebhook = true
      } else if (data === 'Train BOT') {
        this.showWebhook = false
        this.showMyColor = false
        this.showIntent = true
      } else if (data === 'Color') {
        this.showWebhook = false
        this.showIntent = false
        this.showMyColor = true
      }
    },

    async saveColor() {
      let data = {color: this.showColor, uid: this.userAuth.uid}
      const path = `/api/auth_color`;
      await axios.post(path, data)
          .then((res) => {
            this.text = 'บันทึกค่าสีเรียบร้อยแล้ว'
            this.snackbar = true
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err)
          })
    },
    getColorCookie() {
      const path = '/api/color_cookie'
      axios.get(path)
          .then((res) => {
            this.hex = res.data
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err)
          })
    },
  },


  delimiters: ["[[", "]]"]
})


</script>


{% endblock %}