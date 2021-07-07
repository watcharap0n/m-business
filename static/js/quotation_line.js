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
            channel: 'LINE'
        },
        valid: false,
        spinBtn: true,
    },
    delimiters: ["[[", "]]"],
    created() {
        liff.init({liffId: '1655208213-RpzrYv49'}, () => {
                if (liff.isLoggedIn()) {
                    liff.getProfile()
                        .then((profile) => {
                            console.log(liff.getContext());
                            this.formElement.userId = profile.userId
                            this.formElement.profile = profile.displayName
                            this.formElement.picture = profile.pictureUrl
                            this.formElement.email_private = liff.getDecodedIDToken
                        })
                }
                else {
                    liff.login();
                }
            }
        )
    },
    methods: {
        onSubmit() {
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
                    .catch((err) =>{
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