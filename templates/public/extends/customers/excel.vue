<v-dialog
    v-model="dialogExcel"
    persistent
    max-width="300"
>
  <template v-slot:activator="{ on, attrs }">
    <v-btn
        style="margin-left: 10px; margin-top: -10px"
        color="pink lighten-2"
        dark
        small
        v-bind="attrs"
        v-on="on"
        @click="openExcel(selected)"
    >
      <v-icon>
        mdi-file-excel-outline
      </v-icon>
    </v-btn>
  </template>
  <v-card>
    <v-card-title class="headline">
      ดาวโหลดไฟล์ Excel
    </v-card-title>

    <v-card-text v-if="selected.length === 0">
      กรุณาเลือกข้อมูลลูกค้าเพื่อทำการ Export
    </v-card-text>
    <v-card-text v-else v-for="(i, x) in selected" :key="x">
      ลำดับ : [[x + 1]] ชื่อ : [[i.name]]
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          color="red"
          text
          @click="dialogExcel = false"
      >
        ยกเลิก
      </v-btn>

      <form method="post">
        <v-btn
            color="green darken-1"
            text
            type="submit"
            :loading="!spinExcel"
            :disabled="!btnExcel"
        >
          ตกลง
        </v-btn>
      </form>
    </v-card-actions>
  </v-card>
</v-dialog>
