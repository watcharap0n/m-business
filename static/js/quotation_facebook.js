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
            profile: '',
            picture: '',
            channel: 'FACEBOOK'
        },
        valid: false,
        spinBtn: true,
        dialog: true,
        spinFB: true,
    },
    delimiters: ["[[", "]]"],

    created() {
        this.statusChangeCallback()

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
                console.log('vue')
            });
        },
        async statusChangeCallback() {
            await FB.getLoginStatus((response) => {
                this.spinFB = false
                console.log(response)
                if (response.authResponse) {
                    this.dialog = false
                }
                if (response.status === 'connected') {
                    this.dialog = false
                    this.facebookLogin()
                } else {
                    this.dialog = true
                }
            });  // See the onlogin handler
        },
        async facebookLogin() {
            await FB.login((response) => {
                FB.api('/me', {"fields": "id,name,email,picture"}, ((res) => {
                    console.log(res)
                    this.dialog = false
                    this.formElement.userId = res.id
                    this.formElement.profile = res.name
                    this.formElement.email_private = res.email
                    this.formElement.picture = res.picture.data.url
                    console.log(this.formElement)
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