<v-dialog
    v-model="dialogDate"
    width="500"
    persistent
>
  <template v-slot:activator="{ on, attrs }">
    <v-btn
        style="margin-left: 10px; margin-top: -10px"
        color="pink lighten-2"
        dark
        v-bind="attrs"
        v-on="on"
        :hidden="!btnHiddenAPI"
        small
    >
      <v-icon>
        mdi-calendar-month
      </v-icon>
    </v-btn>
  </template>

  <v-card>
    <v-card-title class="headline grey lighten-2">
      ข้อมูลในการกรอง
    </v-card-title>

    <v-card-text>
      <v-form ref="form"
              v-model="valid">
        <v-row>
          <v-col cols="12">
            <v-menu
                ref="menu1"
                v-model="menu1"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    v-model="dateRangeText"
                    label="วันที่"
                    hint="YYYY/MM/DD format"
                    persistent-hint
                    prepend-icon="mdi-calendar"
                    v-bind="attrs"
                    v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                  v-model="date"
                  range
                  color="pink lighten-2"
              >
                <v-spacer></v-spacer>
                <v-btn
                    text
                    color="error"
                    @click="menu1 = false"
                >
                  ยกเลิก
                </v-btn>
                <v-btn
                    text
                    color="success"
                    @click="$refs.menu1.save(date)"
                >
                  ตกลง
                </v-btn>
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12">
            <v-select
                color="pink lighten-2"
                :items="products"
                v-model="selectedProduct"
                label="ผลิตภัณฑ์"
            ></v-select>
          </v-col>

          <v-col cols="12">
            <v-select
                color="pink lighten-2"
                v-model="selectedChannel"
                :items="channels"
                label="ช่องทาง"
            ></v-select>
          </v-col>

          <v-col cols="12">
            <v-select
                color="pink lighten-2"
                v-model="selectedTag"
                :items="tags"
                label="แท็ก"
            ></v-select>
          </v-col>

        </v-row>
      </v-form>
    </v-card-text>
    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          color="red"
          text
          @click="dialogDate = false"
      >
        ยกเลิก
      </v-btn>
      <v-btn
          color="success"
          text
          @click="tableSorting"
      >
        ตกลง
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
