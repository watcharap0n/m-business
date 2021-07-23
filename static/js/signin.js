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
                          this.remember = true
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
                                  this.$refs.form.reset();
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