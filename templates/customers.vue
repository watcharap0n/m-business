{% extends "layout.html" %}
{% block content %}

<br>
<br>
<div id="app">
<v-app id="inspire" style="font-family: 'Prompt', sans-serif; background: #F5F5F5">
  <v-container>
    <v-row class="text-center">
      <v-card class="mx-auto" class="elevation-1">

        <v-bottom-navigation
            v-model="page"
            :background-color="color"
            dark
            flat
            shift
            class="elevation-1"
        >
          <v-btn v-for="(v, i) in navigation" :key="i" @click="changeTransaction(v.href)">
            <span>[[v.header]]</span>
            <v-icon>[[v.icon]]</v-icon>
          </v-btn>

        </v-bottom-navigation>


        <v-card-text>
          <v-data-table v-model="selected" :loading="!spinTable" show-select multi-sort :search="search"
                        :headers="headers"
                        :items="transaction">

            <template v-slot:top>
              <v-toolbar flat>
                <v-text-field
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
                                v-model="editedItem.name"
                                label="Name"
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.product"
                                label="Product"
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.email"
                                label="Email"
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
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.company"
                                label="Company"
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.channel"
                                label="Channel"
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="12"
                              md="12"
                          >
                            <v-textarea
                                v-model="editedItem.message"
                                label="Message"
                            ></v-textarea>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="12"
                              md="12"
                          >
                            <v-combobox
                                v-model="editedItem.tag"
                                label="Tag"
                                multiple
                                dense
                                chips
                            ></v-combobox>
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
  </v-container>
</v-app>
</div>


<script>

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
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
      {
        text: 'Actions',
        value: 'actions',
        sortable: false
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
  },
  created() {
    this.initialize();
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Customer' : 'Edit Customer'
    },
    color() {
      switch (this.page) {
        case 0:
          return 'teal'
        case 1:
          return 'error'
      }
    }
  },
  methods: {
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
    },
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
    },
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
      }
      else{
        this.colorSb = 'error'
        this.text = 'กรุณาเลือกข้อมูลที่จะต้องทำการย้าย!'
        this.snackbar = true

      }
    },
    changeTransaction(data) {
      if (data === 'imports') {
        this.APIImport()
      } else if (data === 'customers') {
        this.initialize()
      }
    },
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
    },
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
    },
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
    },
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
    },
    editItem(item) {
      console.log(this.href)
      this.editedIndex = this.transaction.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogCustomer = true;
    },
    deleteItem(item) {
      this.editedIndex = this.transaction.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },
    async deleteItemConfirm() {
      this.spinButton = false;
      await this.deleteTransaction(this.editedItem.id);
      this.transaction.splice(this.editedIndex, 1);
      this.closeDelete()
    },
    close() {
      this.dialogCustomer = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
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
    },
  },
  delimiters: ["[[", "]]"]
})


</script>


{% endblock %}