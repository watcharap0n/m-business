{% extends 'FACEBOOK/layout/layout.html' %}
{% block content %}


  <v-contatiner>


    <v-dialog
        transition="dialog-bottom-transition"
        max-width="600"
        persistent
        v-model="dialog"
    >
      <v-card>
        <v-card-title class="text-h5">
          Please Login your Facebook!
        </v-card-title>

        <v-card-text>

        </v-card-text>


        <v-card-actions>


          <div @click="facebookLogin" class="fb-login-button" scope="public_profile,email"
               data-scope="public_profile,email"
               data-width="" data-size="large"
               data-button-type="continue_with"
               data-layout="rounded" data-auto-logout-link="false" data-use-continue-as="true"></div>


        </v-card-actions>
      </v-card>
    </v-dialog>


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
    <script src="/static/js/quotation_facebook.js"></script>
  {% endblock %}

{% endblock %}