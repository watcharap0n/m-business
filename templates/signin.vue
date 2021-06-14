{% extends "layout.html" %}
{% block content %}

<br>
<br>
<div id="app">
<v-app id="inspire" style="font-family: 'Prompt', sans-serif; background: #F5F5F5">
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
                    {{ images }}
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
                                                hint="ใส่รหัสอย่างน้อย 8 ตัว" counter
                                                type="password">
                                  </v-text-field>

                                  <v-checkbox
                                      style="margin-top: -8px"
                                      v-model="remember"
                                      label="จดจำรหัสผ่าน"
                                      color="info"
                                      value="remember"
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


</v-app>
</div>


<script>

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: {
    validPassword: [
      v => !!v || 'กรุณากรอกรหัสผ่าน',
      v => v && v.length >= 6 || 'กรุณากรอกอย่างน้อย 6 ตัว'
    ],
    validOther: [v => !!v || 'กรุณากรอกช้อมูล'],
    rules: [
      v => !!v || 'กรุณากรอกอีเมล์',
      v => /.+@.+\..+/.test(v) || 'กรุณากรอกอีเมล์',
    ],
    rulesimage: [
      v => !!v || 'กรุณาใส่รูปภาพ',
      value => !value || value.size < 2000000 || 'ขนาดรูปควรน้อยกว่า 2 MB!',
    ],
    images: [
      {src: 'static/images/social.jpg'},
      {src: 'static/images/bot3.png'},
    ],
    fe: {
      email: '',
      username: '',
      password: '',
      confirmPwd: '',
    },
    feDefault: {
      email: '',
      username: '',
      password: '',
      confirmPwd: '',
    },
    emailLG: '',
    passwordLG: '',
    remember: null,
    forgotForm: '',
    tabs: null,
    valid: false,
    validForgot: false,
    validLogin: false,
    tabName: ["ลงชื่อเข้าใช้", "สมัครใช้งาน", "ลืมรหัสผ่าน"],
    imgFile: null,
    alertLogin: false,
    textAlert: '',
    spinBtn: true,
    snackbar: false,
    text: 'รหัสผ่านไม่ตรงกัน!'
  },
  beforeCreate() {
    const path = '/secure/cookie_login';
    axios.get(path)
        .then((res) => {
          if (res.data.email) {
            this.emailLG = res.data.email
            this.passwordLG = res.data.password
          }
        })
        .catch((err) => {
          console.error(err)
        })
  },
  methods: {
    register() {
      let form = this.$refs.form.validate();
      if (this.fe.confirmPwd !== this.fe.password) {
        form = false
        this.snackbar = true
      }
      if (form === true) {
        this.spinBtn = false
        console.log('success')
        let formData = new FormData();
        formData.append('file', this.imgFile);
        formData.append('email', this.fe.email);
        formData.append('username', this.fe.username);
        formData.append('password', this.fe.password);
        const path = '/secure/register';
        axios.post(path, formData)
            .then((res) => {
              this.spinBtn = true
              Swal.fire(
                  'เรียบร้อย',
                  'คุณลงทะเบียนสำเร็จแล้ว',
                  'success'
              ).then(() => {
                this.fe = Object.assign({}, this.feDefault);
                this.imgFile = null
                this.valid = false;
                this.tabs = 0
              })
            })
            .catch((err) => {
              console.error(err);
            })

      } else {
        console.log('error')
      }
    },
    login() {
      let form = this.$refs.formLogin.validate();
      if (form === true) {
        this.spinBtn = false
        let formData = new FormData();
        formData.append('email', this.emailLG)
        formData.append('password', this.passwordLG)
        formData.append('remember', this.remember)
        const path = '/secure/login';
        axios.post(path, formData)
            .then((res) => {
              if (res.data.status === true) {
                window.location = res.data.url;
              } else {
                this.spinBtn = true
                Swal.fire({
                  icon: 'info',
                  title: 'แจ้งเตือน!',
                  text: 'กรุณายืนยันอีเมล์ของคุณ ก่อนเข้าใช้งาน'
                })
              }
            })
            .catch((err) => {
              this.spinBtn = true
              Swal.fire({
                icon: 'error',
                title: 'ผิดพลาด!',
                text: 'คุณกรอกอีเมล์หรือรหัสผ่านไม่ถูกต้อง'
              })
            })
      }
    },
    forGotPwd() {
      let form = this.$refs.formForgot.validate();
      if (form === true) {
        let formData = new FormData();
        formData.append('forgot', this.forgotForm)
        const path = '/secure/forgotpassword';
        axios.post(path, formData)
            .then((res) => {
              Swal.fire({
                icon: 'info',
                title: 'แจ้งเตือน!',
                text: 'กรุณาเข้าอีเมล์เพื่อทำการเปลี่ยนรหัสผ่าน'
              })
            })
            .catch((err) => {
              console.error(err);
            })

      } else {
        console.log('error')
      }
    },
  },

  delimiters: ["[[", "]]"]
})


</script>


{% endblock %}