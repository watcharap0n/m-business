{% extends 'LINE/layout/layout.html' %}
{% block content %}


  <v-contatiner>
    <div class="d-flex flex-column justify-space-between align-center subheading pt-4">
      <v-img width="200" src="/static/images/mango-profile.jpg">
      </v-img>
    </div>


    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card>
          <v-form ref="form" lazy-validation v-model="valid">
            <v-card-text>
              <v-text-field
                  outlined
                  clearable
                  v-model="formElement.name"
                  :rules="validOther"
                  label="ชื่อผู้ติดต่อ"
                  required
              ></v-text-field>

              <v-text-field
                  outlined
                  clearable
                  v-model="formElement.company"
                  :rules="validOther"
                  label="บริษัท"
                  required
              ></v-text-field>

              <v-text-field
                  outlined
                  clearable
                  v-model="formElement.email"
                  :rules="validEmail"
                  label="อีเมล"
                  required
              ></v-text-field>

              <v-select
                  outlined
                  clearable
                  v-model="formElement.product"
                  :items="products"
                  :rules="validSelect"
                  label="ผลิตภัณฑ์"
                  required
              ></v-select>


              <v-text-field
                  outlined
                  clearable
                  v-model="formElement.tel"
                  :rules="validTel"
                  label="เบอร์ที่สะดวกให้เจ้าหน้าที่ติดต่อกลับ"
                  type="tel"
                  required
              ></v-text-field>

              <v-textarea
                  outlined
                  v-model="formElement.message"
                  clearable
                  autocomplete="email"
                  label="ข้อมูลที่ท่านต้องการทราบเพิ่มเติม"
              ></v-textarea>
              <v-card-actions>
                <v-btn block
                       :disabled="!valid"
                       :loading="!spinBtn"
                       color="success"
                       class="mr-4"
                       @click="onSubmit"
                >
                  ยืนยัน
                </v-btn>
              </v-card-actions>
            </v-card-text>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-contatiner>




  {% block script %}
    <script src="/static/js/quotation_line.js"></script>
  {% endblock %}

{% endblock %}