// const pause = ms => new Promise(resolve => setTimeout(resolve, ms))
new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        loaderSpin: true,
        loaderData: false,
        userAuth: {
            name: '',
            picture: '',
            email: '',
            uid: '',
        },

        items: [
            {
                icon: 'mdi-inbox',
                text: 'Webhook',
            },
            {
                icon: 'mdi-star',
                text: 'สอนบอทแมงโก้'
            },
            {
                icon: 'mdi-star',
                text: 'สอนบอท',
            },
        ],
        modelList: 0,
        showWebhook: true,
        showIntent: false,
        showBotMango: false,

        spinAuth: false,
        hasSaved: false,
        isEditing: null,
        ACCESS_TOKEN: '',
        SECRET_LINE: '',
        validWebhook: false,
        webhook: '',
        spinWebhook: true,
        rules: [v => !!v || 'require!'],

        treeHidden: false,
        hiddenIntent: false,
        hiddenAccess: true,
        nameIntent: '',
        nameAccestoken: '',
        mangoAccess: '',
        validAccess: false,
        dialogIntent: false,
        dialogDeleteIntent: false,
        dialogAcesstoken: false,
        question: '',
        answer: '',
        active: [],
        open: [],
        users: [],
        spinIntent: true,
        dataAppend: {
            id: '',
            uid: '',
            name: '',
            question: [],
            answer: [],
            access_token: '',
        },

        navigatorAppbar: false,
        selectedList: 1,
        itemsAppbar: [
            {text: 'DataTable', icon: 'mdi-database'},
            {text: 'Intents', icon: 'mdi-account'},
        ],

        //chatbot

    },
    delimiters: ["[[", "]]"],

    beforeCreate() {
        const path = '/secure/socket_auth'
        axios.get(path)
            .then((res) => {
                this.loaderSpin = false
                this.loaderData = true
                let user = this.userAuth
                user.name = res.data.name
                user.picture = res.data.picture
                user.email = res.data.email
                user.uid = res.data.uid
            })
    },
    computed: {
        itemsIntent() {
            return [
                {
                    name: 'Intents',
                    children: this.users,
                },
            ]
        },
        selectedIntent() {
            if (!this.active.length) return undefined
            const id = this.active[0]
            return this.users.find(user => user.id === id)
        }
    },
    methods: {
        saveWebhook() {
            this.spinWebhook = false
            let form = this.$refs.formWebhook.validate();
            if (form === true) {
                let data = {ACCESS_TOKEN: this.ACCESS_TOKEN, SECRET_LINE: this.SECRET_LINE}
                const path = '/callback/save'
                axios.post(path, data)
                    .then((res) => {
                        this.webhook = res.data.webhook
                        this.hasSaved = true;
                        this.spinWebhook = true
                    })
                    .catch((err) => {
                        console.error(err)
                    })
            }
        },

        logout() {
            return window.location = '/secure/logout'
        },

        // start intent
        formAccessToken() {
            this.hiddenAccess = false
            this.dialogAcesstoken = false
            this.treeHidden = true
        },
        async intents(item) {
            const pause = ms => new Promise(resolve => setTimeout(resolve, ms))
            await pause(1500)
            if (this.showIntent === true) {
                let data = {'access_token': this.nameAccestoken}
                return this.getIntents(data, item)
            } else if (this.showBotMango === true) {
                return this.getIntents(null, item)
            }
        },

        getIntents(data, item) {
            const path = `/intent/data`
            return axios.post(path, data)
                .then((res) => {
                    item.children.push(...res.data)
                    this.hiddenIntent = true
                })
                .catch((err) => console.error(err))
        },

        createIntent() {
            console.log()
            if (this.showIntent === true) {
                this.spinIntent = false
                this.dataAppend.name = this.nameIntent
                this.dataAppend.uid = this.userAuth.uid
                this.dataAppend.access_token = this.nameAccestoken
                this.addIntent(this.dataAppend)
            } else if (this.showBotMango === true) {
                this.spinIntent = false
                this.dataAppend.name = this.nameIntent
                this.dataAppend.uid = this.userAuth.uid
                this.dataAppend.access_token = null
                console.log(this.dataAppend)
                this.addIntent(this.dataAppend)
            }
        },
        addIntent(data) {
            const path = '/intent/add'
            axios.post(path, data)
                .then((res) => {
                    this.nameIntent = ''
                    this.spinIntent = true
                    this.users.push(res.data)
                    this.dialogIntent = false
                })
                .catch((err) => console.error(err))
        },
        deleteIntent(item) {
            this.spinIntent = false
            const path = `/intent/delete_intent/${item.id}`
            axios.delete(path)
                .then((res) => {
                    console.log(res.data)
                    this.users.splice(this.users.indexOf(item), 1)
                    this.dialogDeleteIntent = false
                    this.spinIntent = true
                })
                .catch((err) => console.error(err))

        },
        async sendQuestion() {
            this.spinIntent = false
            this.selectedIntent.question.push(this.question)
            await this.updateIntent()
            this.spinIntent = true
        },
        async sendAnswer() {
            this.spinIntent = false
            this.selectedIntent.answer.push(this.answer)
            await this.updateIntent()
            this.spinIntent = true
        },
        async removeAnswer(item) {
            this.selectedIntent.answer.splice(this.selectedIntent.answer.indexOf(item), 1)
            await this.updateIntent();
        },
        async removeQuestion(item) {
            this.selectedIntent.question.splice(this.selectedIntent.question.indexOf(item), 1)
            await this.updateIntent();
        },
        async updateIntent() {
            const path = '/intent/update_intent'
            await axios.post(path, this.selectedIntent)
                .then((res) => {
                    this.question = ''
                    this.answer = ''
                    console.log(res.data)
                })
                .catch((err) => {
                    console.log(err)
                })
        },

        // listModel
        listModel(data) {
            if (data === 'Webhook') {
                this.active = []
                this.open = []
                this.users = []
                this.hiddenIntent = false
                this.nameAccestoken = ''
                this.mangoAccess = ''
                this.showIntent = false
                this.showWebhook = true
                this.showBotMango = false
            } else if (data === 'สอนบอท') {
                this.active = []
                this.open = []
                this.users = []
                this.hiddenIntent = false
                this.nameAccestoken = ''
                this.mangoAccess = ''
                this.showWebhook = false
                this.showIntent = true
                this.showBotMango = false
            } else if (data === 'สอนบอทแมงโก้') {
                this.active = []
                this.open = []
                this.users = []
                this.hiddenIntent = false
                this.nameAccestoken = ''
                this.mangoAccess = 'mango'
                this.showWebhook = false
                this.showIntent = false
                this.showBotMango = true
            }
        },

        redirectPage(item) {
            console.log(item)
            if (item.text === 'DataTable')
                window.location = '/customers'
            if (item.text === 'Intents')
                window.location = '/intents'
        },
    }
})