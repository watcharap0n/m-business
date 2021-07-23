new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        loaderSpin: true,
        loaderData: false,

        // auth
        userAuth: {
            name: '',
            picture: '',
            email: '',
            uid: '',
        },
        spinAuth: false,

        // table
        page: 0,
        navigation: [
            {
                header: 'Customers',
                href: 'customers',
                icon: 'mdi-account-supervisor-circle'
            },
            {
                header: 'Imports',
                href: 'imports',
                icon: 'mdi-import'
            },
        ],
        headers: [
            {
                text: 'Actions',
                value: 'actions',
                sortable: false,
            },
            {
                text: 'Tag',
                value: 'tag',
            },
            {
                text: 'Product',
                value: 'product',
                align: 'start'
            },
            {
                text: 'User Info',
                value: 'name',
                align: 'center'
            },
            {
                text: 'Company',
                value: 'company',
            },
            {
                text: 'Message',
                value: 'message'
            },
            {
                text: 'Channel',
                value: 'channel'
            },
            {
                text: 'Profile',
                value: 'profile'
            },
            {
                text: 'Assign',
                value: 'username'
            },
            {
                text: 'Data/Time',
                value: 'date',
                align: 'center',
            },

        ],
        editedItem: {
            id: '',
            name: '',
            tag: [],
            product: '',
            email: '',
            email_private: '',
            profile: '',
            picture: '',
            userId: '',
            other: '',
            tel: '',
            company: '',
            channel: '',
            message: '',
            username: '',
            uid: '',
        },
        defaultItem: {
            id: '',
            name: '',
            tag: [],
            product: '',
            email: '',
            email_private: '',
            profile: '',
            picture: '',
            userId: '',
            other: '',
            tel: '',
            company: '',
            channel: '',
            message: '',
            username: '',
            uid: '',
        },
        search: '',
        transaction: [],
        selected: [],
        spinButton: true,
        imgError: false,
        spinTable: false,
        dialogCustomer: false,
        dialogDelete: false,
        editedIndex: -1,
        snackbar: false,
        btnImport: false,
        spinImport: false,
        timeout: 2000,
        colorSb: '',
        text: '',
        path: '',
        href: '',
        isProfile: false,
        productMango: ['RealEstate', 'Construction', 'BI Dashboard', 'Project Planning', 'CSM', 'QCM', 'Maintenance', 'Rental', 'MRP'],

        // tags
        itemsTag: [],
        searchTag: null,
        editingTag: null,
        colorsTag: 'pink',
        model: [],
        btnTag: false,
        spinTag: true,

        sheet: false,
        tiles: [
            {img: 'keep.png', title: 'Keep'},
            {img: 'inbox.png', title: 'Inbox'},
            {img: 'hangouts.png', title: 'Hangouts'},
            {img: 'messenger.png', title: 'Messenger'},
            {img: 'google.png', title: 'Google+'},
        ],

        // Appbar
        navigatorAppbar: false,
        selectedList: 0,
        itemsAppbar: [
            {text: 'DataTable', icon: 'mdi-database'},
            {text: 'Intents', icon: 'mdi-account'},
        ],
    },


    watch: {
        model(val, prev) {
            if (val.length === prev.length) return
            this.model = val.map(v => {
                if (typeof v === 'string') {
                    v = {
                        text: v,
                        color: this.colorsTag
                    }
                    this.addTag(v)
                    this.nonce++
                }
                return v
            })
            if (this.model.length > 0 && this.selected.length > 0) {
                this.btnTag = true
            } else if (this.model.length === 0) {
                this.btnTag = false
            }

        },
    },

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
    async created() {
        await this.initialize();
        await this.getTags();
    },

    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'New Customer' : 'Edit Customer'
        },
    },
    methods: {
        // table
        async initialize() {
            this.spinTable = false
            const path = '/api/customer'
           await axios.get(path)
                .then((res) => {
                    this.spinTable = true;
                    this.transaction = res.data;
                    this.href = 'customer'
                    this.btnImport = false
                })
                .then((err) => {
                    console.log(err)
                })
        },
        async APIImport() {
            this.spinTable = false
            const path = '/api/import'
           await axios.get(path)
                .then((res) => {
                    this.spinTable = true;
                    this.transaction = res.data;
                    this.href = 'import'
                    this.btnImport = true
                })
                .then((err) => {
                    console.log(err)
                })
        },
        async moveImport() {

            if (this.selected.length > 0) {
                this.spinImport = true
                const path = '/api/move/customer'
                this.selected.forEach((data) => {
                    data.username = this.userAuth.name
                    data.uid = this.userAuth.uid
                    this.transaction.splice(this.transaction.indexOf(data), 1)
                })
                await axios.post(path, this.selected)
                    .then((res) => {
                        this.spinImport = false
                        this.text = `คุณได้ทำการย้ายข้อมูลไปหน้า customers แล้ว!`
                        this.colorSb = 'success'
                        this.snackbar = true
                        this.selected = []
                    })
                    .catch((err) => {
                        this.text = 'เกิดข้อผิดพลาด'
                        this.selected = []
                    })
            } else {
                this.colorSb = 'error'
                this.text = 'กรุณาเลือกข้อมูลที่จะต้องทำการย้าย!'
                this.snackbar = true

            }
        },
      async changeTransaction(data) {
            if (data === 'imports') {
               await this.APIImport()
                this.selected = []
                this.model = []
            } else if (data === 'customers') {
               await this.initialize()
            }
        },
        colorProduct(product) {
            if (product === 'Construction') {
                return 'green accent-1'
            }
            if (product === 'RealEstate') {
                return 'light-blue accent-1'
            }
            if (product === 'Project Planning') {
                return 'red accent-1'
            }
        },
        async addTransaction(data) {
            let href = this.href
            if (href === 'customer')
                this.path = '/api/customer'
            if (href === 'import')
                this.path = '/api/import'
            this.editedItem.uid = this.userAuth.uid
            this.editedItem.username = this.userAuth.name
            await axios.post(this.path, data)
                .then((res) => {
                    this.spinButton = true;
                    this.transaction.unshift(res.data);
                    this.text = `คุณได้เพิ่มข้อมูล ${this.editedItem.name}`
                    this.colorSb = 'success'
                    this.snackbar = true
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        async editTransaction(data, id) {
            let href = this.href
            if (href === 'customer')
                this.path = `/api/customer/${id}`
            if (href === 'import')
                this.path = `/api/import/${id}`
            await axios.put(this.path, data)
                .then(() => {
                    this.spinButton = true;
                    this.colorSb = 'primary'
                    this.text = `คุณได้อัพเดทข้อมูล ${this.editedItem.name}`
                    this.snackbar = true
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        async deleteTransaction(id) {
            let href = this.href
            if (href === 'customer')
                this.path = `/api/customer/${id}`
            if (href === 'import')
                this.path = `/api/import/${id}`
            await axios.delete(this.path)
                .then((res) => {
                    this.selected = []
                    this.spinButton = true;
                    console.log(res.data);
                    this.colorSb = 'red'
                    this.text = `คุณได้ลบข้อมูล ${this.editedItem.name}`
                    this.snackbar = true
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        editItem(item) {
            this.editedIndex = this.transaction.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogCustomer = true;
        },
        deleteItem(item) {
            this.editedIndex = this.transaction.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },
        async deleteItemConfirm() {
            this.spinButton = false;
            await this.deleteTransaction(this.editedItem.id);
            this.transaction.splice(this.editedIndex, 1);
            this.closeDelete()
        },
        close() {
            this.dialogCustomer = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },
        closeDelete() {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },
        async save() {
            if (this.editedIndex > -1) {
                this.spinButton = false;
                let data = Object.assign(this.transaction[this.editedIndex], this.editedItem);
                await this.editTransaction(data, data.id);
            } else {
                this.spinButton = false;
                await this.addTransaction(this.editedItem);
            }
            this.close()
        },


        // tags
        getTags() {
            const path = '/api/tag'
            axios.get(path)
                .then((res) => {
                    this.itemsTag = res.data
                })
                .catch((err) => {
                    console.error(err)
                })
        },
        filter(item, queryText, itemText) {
            const hasValue = val => val != null ? val : ''
            const text = hasValue(itemText)
            const query = hasValue(queryText)
            return text.toString()
                .toLowerCase()
                .indexOf(query.toString().toLowerCase()) > -1
        },
        edit(index, item) {
            if (!this.editingTag) {
                this.editingTag = item
                this.editingIndexTag = index

            } else {
                this.setTag(item.id, this.editingTag)
                this.editingTag = null
                this.editingIndexTag = -1
            }
        },
        addTag(item) {
            const path = `/api/tag?tag=${item.text}`
            axios.get(path)
                .then(() => {
                    this.getTags()
                    console.log('success')
                })
                .catch((err) => {
                    console.error(err)
                })
        },
        setTag(id, item) {
            const path = `/api/tag/${item}?id-query=${id}`;
            axios.put(path)
                .then(() => {
                    console.log('success')
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        toRemove(index, item) {
            this.itemsTag.splice(this.itemsTag.indexOf(item), 1)
            this.removeTag(item.id)
        },
        removeTag(id) {
            console.log(id)
            const path = `/api/tag?id-query=${id}`;
            axios.delete(path)
                .then(() => {
                    this.getTags()
                    console.log('success')
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        tagTransaction(selected) {
            this.spinTag = false
            let data = {id: selected, tag: this.model, href: this.href}
            const path = '/api/tag'
            axios.post(path, data)
                .then((res) => {
                    this.spinTag = true
                    this.initialize()
                })
                .catch((err) => {
                    console.error(err)
                })
        },
        logout() {
            return window.location = '/secure/logout'
        },

        //appBar
        redirectPage(item) {
            console.log(item)
            if (item.text === 'DataTable')
                window.location = '/customers'
            if (item.text === 'Intents')
                window.location = '/intents'
        },

    },
    delimiters: ["[[", "]]"]
})