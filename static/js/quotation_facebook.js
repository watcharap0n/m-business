new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        products: ['Construction', 'RealEstate', 'Project Planning', 'Other'],
        validCheck: [v => !!v || 'กรุณาคลิกเพื่อไปต่อ'],
        validSelect: [v => !!v || 'กรุณาเลือกผลิตภัณฑ์'],
        validEmail: [
            v => !!v || 'กรุณากรอกอีเมล',
            v => /.+@.+\..+/.test(v) || 'กรุณากรอกอีเมลให้ถูกต้อง',
        ],
        validTel: [
            v => !!v || 'กรุณากรอกเบอร์โทร',
            v => (v && v.length <= 10) || 'เบอร์โทรกรอกไม่ครบ',
        ],
        validOther: [v => !!v || 'กรุณากรอกข้อมูลให้ครบถ้วน'],
        name: '',
        formElement: {
            name: '',
            email: '',
            company: '',
            tel: '',
            product: '',
            other: '',
            message: '',
            userId: '',
            email_private: '',
            displayName: '',
            picture: '',
            channel: ''
        },
        valid: false,
        spinBtn: true,
        dialog: true,
    },
    delimiters: ["[[", "]]"],

    created() {
        this.statusChangeCallback();

        window.fbAsyncInit = function () {
            FB.init({
                appId: '529836688014346',
                cookie: true,
                xfbml: true,
                version: 'v11.0'
            });
            FB.AppEvents.logPageView();
        };


    },
    methods: {
        checkLoginState() {
            FB.getLoginStatus((response) => {   // See the onlogin handler
                console.log(response)
                statusChangeCallback(response)
                console.log(response)
            });
        },
        statusChangeCallback() {
            FB.getLoginStatus((response) => {
                console.log(response)
                if (response.status === 'connected') {
                    this.dialog = false
                    this.facebookLogin()
                } else {
                    this.dialog = true
                }
            });  // See the onlogin handler
        },
        facebookLogin() {
            FB.login((response) => {
                FB.api('/me', ((res) => {
                    this.dialog = false
                    this.formElement.userId = res.id
                    this.formElement.displayName = res.name
                    this.formElement.channel = 'FACEBOOK'
                }))
                FB.api('/me/permissions', ((res) => {
                    console.log(res.data)
                }))
            },)
        },
        onSubmit() {
            console.log(this.name)
            let validate = this.$refs.form.validate()
            if (validate === true) {
                this.spinBtn = false
                const path = '/quotation/data/quotation'
                axios.post(path, this.formElement)
                    .then(() => {
                        this.spinBtn = true
                        this.popUp()
                        this.$refs.form.reset()
                    })
                    .catch((err) => {
                        this.spinBtn = true
                        console.error(err)
                    })
            }
        },
        popUp() {
            Swal.fire("ข้อมูลบันทึกเรียบร้อย!", "เจ้าหน้าที่ได้รับข้อมูลของท่านแล้ว\nและจะดำเนินการติดต่อกลับให้เร็วที่สุด", "success").then(() => {
                liff.closeWindow();
            })
        },
    }
})