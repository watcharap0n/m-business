{% extends "admin/main_layout.html" %}
{% block content %}
  <br>
  <br>
  <!-- contents -->
  <div class="jumbotron">
    <v-container>
      <template>
        <v-row no-gutters>
          <v-col cols="12" md="6">
            <v-card class="mx-auto">
              <v-carousel hide-delimiters>
                <v-carousel-item v-for="(image,i) in images" :key="i" :src="image.src">
                  <div class="display-3">
                  </div>
                </v-carousel-item>
              </v-carousel>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-text>
                <div class="text-center">
                  <v-row no-gutters>
                    &nbsp;
                    <v-col cols="12" md="12">
                      <v-avatar size="100">
                        <img src="static/images/iconbot.jpg" alt="logo">
                      </v-avatar>
                      <h3>MANGO BOT</h3>
                    </v-col>

                    <v-col cols="12" md="12">

                      <v-tabs centered v-model=tabs>
                        <v-tab v-for="i in tabName">
                          <h5>[[i]]</h5>
                        </v-tab>
                      </v-tabs>

                      <v-tabs-items v-model="tabs">
                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-container>

                                <v-form v-model="validLogin" ref="formLogin"
                                        lazy-validation>

                                  <v-text-field v-model="emailLG" label="อีเมล์"
                                                required :rules="rules">
                                  </v-text-field>

                                  <v-text-field v-model="passwordLG"
                                                :rules="validPassword" label="รหัสผ่าน"
                                                type="password">
                                  </v-text-field>

                                  <v-checkbox
                                      style="margin-top: -8px"
                                      v-model="remember"
                                      label="จดจำรหัสผ่าน"
                                      color="info"
                                      hide-details
                                  ></v-checkbox>

                                  <v-btn :disabled="!validLogin" @click="login" :loading="!spinBtn" rounded
                                         color="#5fa55a" large dark>
                                    <h6>เข้าสู่ระบบ</h6>
                                  </v-btn>

                                </v-form>

                              </v-container>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>

                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-container>
                                <v-form v-model="valid" ref="form" lazy-validation>

                                  <v-text-field v-model="fe.username"
                                                label="ชื่อผู้ใช้" :rules="validOther" required
                                                clearable>
                                  </v-text-field>

                                  <v-text-field v-model="fe.email" label="อีเมล์"
                                                required clearable :rules="rules">
                                  </v-text-field>

                                  <v-text-field v-model="fe.password" label="รหัสผ่าน"
                                                type="password" :rules="validPassword" required
                                                clearable>
                                  </v-text-field>

                                  <v-text-field v-model="fe.confirmPwd" label="ยืนยันรหัสผ่าน"
                                                type="password" :rules="validPassword" required
                                                clearable>
                                  </v-text-field>

                                  <v-file-input v-model="imgFile" :rules="rulesimage"
                                                required
                                                accept="image/png, image/jpeg, image/bmp"
                                                prepend-icon="mdi-camera-plus"
                                                label="อัพโหลดรูปโปรไฟล์">
                                  </v-file-input>

                                  <v-btn rounded color="#01b4bc" large dark
                                         :loading="!spinBtn" :disabled="!valid"
                                         @click="register">
                                    <h6>สมัคร</h6>
                                  </v-btn>

                                </v-form>
                              </v-container>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>

                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-container>

                                <v-form v-model="validForgot" ref="formForgot"
                                        lazy-validation>
                                  <v-text-field v-model="forgotForm"
                                                label="กรอกอีเมล์" required clearable
                                                :rules="rules">
                                  </v-text-field>

                                  <v-btn rounded color="#fa8925" large dark
                                         @click="forGotPwd">
                                    <h6>ลืมรหัสผ่าน</h6>
                                  </v-btn>
                                </v-form>


                              </v-container>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>

                      </v-tabs-items>


                    </v-col>

                  </v-row>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </template>
      <v-snackbar
          v-model="snackbar"
          timeout="2000"
          color="red"
      >
        [[text]]
        <template v-slot:action="{ attrs }">
          <v-btn
              dark
              text
              v-bind="attrs"
              @click="snackbar = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </div>


  {% block script %}
    <script type="module" src="/static/js/signin.js"></script>
  {% endblock %}


{% endblock %}