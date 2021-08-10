<v-dialog
    persistent
    v-model="dialogCustomer"
    max-width="650"
>
  <template v-slot:activator="{ on, attrs }">
    <v-btn
        style="margin-left: 10px"
        color="pink lighten-2"
        v-bind="attrs"
        v-on="on"
        dark
        :hidden="!btnHiddenAPI"
    >
      <v-icon left>mdi-account-circle</v-icon>
      เพิ่มข้อมูล
    </v-btn>
  </template>


  <v-card>
    <v-toolbar class="elevation-1" flat color="pink lighten-2" dark>
      <v-card-title>
        <v-icon medium style="margin-right: 10px">mdi-account-circle
        </v-icon>
        <h4>[[ formTitle ]]</h4>
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
                label="ชื่อ"
                outlined
                color="pink lighten-2"
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
                color="pink lighten-2"
                :items="productMango"
                label="ผลิตภัณฑ์"
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
                label="อีเมล"
                color="pink lighten-2"
                prepend-inner-icon="mdi-email"
                outlined
                dense
            ></v-text-field>
          </v-col>

          <v-col
              cols="12"
              sm="6"
              md="6"
          >

            <v-text-field
                v-model="editedItem.person_id"
                label="เลขที่บัตรประชาชน"
                color="pink lighten-2"
                prepend-inner-icon="mdi-account-outline"
                outlined
                dense
            ></v-text-field>

          </v-col>

          <v-col
              cols="12"
              sm="6"
              md="6"
          >

            <v-text-field
                v-model="editedItem.tax_id"
                label="เลขที่เสียภาษี"
                color="pink lighten-2"
                prepend-inner-icon="mdi-account-box"
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
                label="เบอร์ติดต่อ"
                color="pink lighten-2"
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
                label="บริษัท"
                color="pink lighten-2"
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
                label="ช่องทาง"
                color="pink lighten-2"
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
                label="ข้อความ"
                color="pink lighten-2"
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
                color="pink lighten-2"
                dense
                chips
                small-chips
                label="แท็ก"
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