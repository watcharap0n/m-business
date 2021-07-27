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
        small
    >
      <v-icon>
        mdi-calendar-month
      </v-icon>
    </v-btn>
  </template>

  <v-card>
    <v-card-title class="headline grey lighten-2">
      Month
    </v-card-title>

    <v-card-text>
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
                  label="Date"
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
            >
              <v-spacer></v-spacer>
              <v-btn
                  text
                  color="primary"
                  @click="menu1 = false"
              >
                ยกเลิก
              </v-btn>
              <v-btn
                  text
                  color="primary"
                  @click="$refs.menu1.save(date)"
              >
                ตกลง
              </v-btn>
            </v-date-picker>
          </v-menu>
        </v-col>
      </v-row>

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
          color="primary"
          text
          @click="tableSorting"
      >
        ตกลง
      </v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
