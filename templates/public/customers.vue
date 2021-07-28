{% extends "admin/main_layout.html" %}
{% block content %}


  {% include 'public/extends/customers/navigationTop.vue' %}

  <br><br><br>
  <div class="container-fluid">
    <v-card class="mx-auto" class="elevation-1">

      <v-bottom-navigation
          style="background: linear-gradient(to right, #7C4DFF, #304FFE, #448AFF);"
          v-model="page"
          dark
          flat
          shift
          class="elevation-1"
      >
        <v-btn v-for="(v, i) in navigation" :key="i" @click="changeTransaction(v.href)">
          <v-badge
              color="pink lighten-2"
              :content="transaction.length"
          >
            <span>[[v.header]]</span>
          </v-badge>
          <v-icon>[[v.icon]]</v-icon>
        </v-btn>

      </v-bottom-navigation>


      <!--     start table     -->
      <v-data-table v-model="selected" :loading="!spinTable" show-select multi-sort :search="search"
                    :headers="headers"
                    loading-text="Loading... Please wait"
                    class="elevation-5 rounded-xl"
                    height="500"
                    :items="transaction">

        <!--       slot TOP         -->

        <template v-slot:top>

          <v-toolbar flat>

            {% include "public/extends/customers/addCustomer.vue" %}


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

            &nbsp;
            <v-btn
                dark
                color="pink lighten-2"
                :hidden="!btnImport"
                @click="moveImport"
                :loading="spinImport"
            >
              <v-icon left>mdi-application-import</v-icon>
              นำเข้า
            </v-btn>

            <v-spacer></v-spacer>

            <div class="small" style="margin-right: 20px">
              <v-text-field
                  color="pink lighten-2"
                  :loading="!spinTable"
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="ค้นหา"
                  single-line
                  hide-details
              >
              </v-text-field>
            </div>

          </v-toolbar>


          <v-toolbar flat>

            {% include "public/extends/customers/sorting.vue" %}


            {% include "public/extends/customers/excel.vue" %}


            <v-spacer></v-spacer>

            <!-- tag start -->
            <v-btn
                elevation="3"
                :loading="!spinTag"
                :disabled="!btnTag"
                small
                color="#FF648D"
                dark
                @click="tagTransaction(selected)"
            ><i class="fas fa-user-tag"></i>
              Tag Customers
            </v-btn>

            <div class="small" style="margin-left: 10px; margin-right: 20px">
              <v-combobox
                  :loading="!spinTable"
                  v-model="model"
                  :filter="filter"
                  :hide-no-data="!searchTag"
                  :items="itemsTag"
                  :search-input.sync="searchTag"
                  hide-selected
                  label="แท็ก"
                  color="pink lighten-2"
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


            <!--tag end-->


          </v-toolbar>


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
            <div v-if="item.product === 'Construction'">
              <strong style="color: green">[[item.product]]</strong>
            </div>

            <div v-else-if="item.product === 'RealEstate'">
              <strong style="color: blue">[[item.product]]</strong>
            </div>

            <div v-else-if="item.product === 'Project Planning'">
              <strong style="color: deeppink">[[item.product]]</strong>
            </div>

            <div v-else-if="item.product === 'Consulting'">
              <strong style="color: black">[[item.product]]</strong>
            </div>

            <div v-else>
              <strong>[[item.product]]</strong>
            </div>
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
          <div v-if="item.channel === 'Contact'">
            <v-chip outlined color="blue darken-2">
              [[item.channel ]]
            </v-chip>
          </div>

          <div v-else-if="item.channel === 'GetDemo'">
            <v-chip outlined color="pink lighten-2">
              [[item.channel ]]
            </v-chip>
          </div>

          <div v-else-if="item.channel === 'LINE'">
            <v-chip outlined color="green accent-4">
              [[item.channel ]]
            </v-chip>
          </div>

          <div v-else>
            <v-chip outlined>
              [[item.channel ]]
            </v-chip>
          </div>
        </template>

        <template v-slot:item.date="{item}">
          [[ item.date ]]
          <v-divider></v-divider>
          [[ item.time ]]
        </template>

        <template v-slot:item.actions="{item}">
          <v-icon small class="mr-2" color="green lighten-2" @click="editItem(item)">
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
    </v-card>


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


  </div>
  {% block script %}
    <script src="/static/js/customers.js"></script>
  {% endblock %}
{% endblock %}