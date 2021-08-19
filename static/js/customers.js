new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        // datetime
        date: [],
        menu1: false,
        dialogDate: false,

        loaderSpin: true,
        loaderData: false,

        // excel
        dialogExcel: false,
        btnExcel: true,
        spinExcel: false,

        // auth
        userAuth: {
            name: '',
            picture: '',
            email: '',
            uid: '',
        },
        spinAuth: false,

        // table
        page: 1,
        hiddenAPI: true,
        navigation: [
            {
                header: 'ข้อมูลลูกค้า',
                href: 'customers',
                icon: 'mdi-account-supervisor-circle'
            },
            {
                header: 'นำเข้า',
                href: 'imports',
                icon: 'mdi-import'
            },
            {
                header: 'API',
                href: 'api',
                icon: 'mdi-api'
            }
        ],
        headers: [
            {
                text: 'แก้ไข/ลบ',
                value: 'actions',
                width: 80,
                sortable: false,
            },
            {
                text: 'แท็ก',
                value: 'tag',
            },
            {
                text: 'ผลิตภัณฑ์',
                value: 'product',
                align: 'start'
            },
            {
                text: 'อื่นๆ',
                value: 'other',
                align: "center",
            },
            {
                text: 'ข้อมูลลูกค้า',
                value: 'name',
                align: 'center',
                width: 80
            },
            {
                text: 'บริษัท',
                value: 'company',
            },
            {
                text: 'ข้อความ',
                value: 'message'
            },
            {
                text: 'ช่องทาง',
                value: 'channel'
            },
            {
                text: 'โปรไฟล์',
                value: 'profile'
            },
            {
                text: 'คนนำเข้า',
                value: 'username'
            },
            {
                text: 'วัน/เวลา',
                value: 'date',
                align: 'center',
            },

        ],
        editedItem: {
            id: '',
            person_id: '',
            tax_id: '',
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
            person_id: '',
            tax_id: '',
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
        valid: true,
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
        selectedProduct: '',
        selectedChannel: '',
        selectedTag: '',
        products: [],
        channels: [],
        tags: [],
        productMango: ['RealEstate', 'Construction', 'BI Dashboard', 'Project Planning', 'CSM', 'QCM', 'Maintenance', 'Rental', 'MRP'],

        // tags
        itemsTag: [],
        searchTag: null,
        editingTag: null,
        colorsTag: 'pink',
        model: [],
        btnTag: false,
        btnDelete: false,
        spinDelete: true,
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

        // btn or table hidden
        btnHiddenAPI: true,
        btnAPI: true,
    },


    watch: {
        date(val) {
            if (this.date.length > 0) {
                this.$refs.form.reset()
            }
        },
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
            } else if (this.model.length === 0 || this.selected.length === 0) {
                this.btnTag = false
            }
        },
        selected() {
            if (this.selected.length > 0 && this.model.length > 0) {
                this.btnTag = true
            } else if (this.selected.length === 0 || this.model.length === 0) {
                this.btnTag = false
            }
            if (this.selected.length > 0) {
                this.btnDelete = true
            } else if (this.selected.length === 0) {
                this.btnDelete = false
            }
        }

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
        await this.APIImport();
        await this.getTags();
    },

    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'เพิ่มข้อมูล' : 'แก้ไขข้อมูล'
        },
        formBtnAPI() {
            return this.btnHiddenAPI === true ? 'ตรวจสอบเข้า RE' : 'นำส่งเข้า RE'
        },
        dateRangeText() {
            return this.date.join(' ~ ')
        },
    },
    methods: {
        // table
        async initialize() {
            this.btnAPI = true
            this.btnHiddenAPI = true
            this.spinTable = false
            const path = '/api/customer'
            await axios.get(path)
                .then((res) => {
                    this.spinTable = true;
                    this.transaction = res.data.transaction;
                    this.products = res.data.products
                    this.channels = res.data.channels
                    this.tags = res.data.tags
                    this.href = 'customer'
                    this.btnImport = false
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        async APIImport() {
            this.btnAPI = false
            this.btnHiddenAPI = true
            this.spinTable = false
            const path = '/api/import'
            await axios.get(path)
                .then((res) => {
                    this.spinTable = true;
                    this.transaction = res.data.transaction;
                    this.href = 'import'
                    this.btnImport = true
                })
                .catch((err) => {
                    console.log(err)
                })
        },

        // excel
        openDialog() {
            if (this.selected.length === 0) {
                this.btnExcel = false
            } else if (this.selected.length > 0) {
                this.btnExcel = true
                this.spinExcel = true
            }
        },
        submitExcel(selected) {
            this.btnExcel = true
            let data_id = []
            selected.forEach((v) => {
                data_id.push(v.id)
            })
            this.spinExcel = false

            if (this.href === 'customer') {
                this.exportExcel('/api/datafile/customer/excel', data_id)
            }
            if (this.href === 'import') {
                this.exportExcel('/api/datafile/import/excel', data_id)
            }
        },
        exportExcel(path, data_id) {
            axios.post(path, data_id, {
                headers: {
                    'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'Content-Disposition': "attachment; filename=customers.xlsx"
                },
                responseType: 'arraybuffer'
            })
                .then((res) => {
                    // const url = window.URL.createObjectURL(new Blob([res.data[0]]));
                    const link = document.createElement('a');
                    // link.href = url;
                    link.setAttribute('download', 'customers.xlsx');
                    document.body.appendChild(link);
                    link.click();
                    this.spinExcel = true
                    this.dialogExcel = false
                })
                .catch((err) => {
                    this.spinExcel = true
                    console.error(err)
                })
        },

        // sorting
        tableSorting() {
            if (this.date.length === 0 && !this.selectedChannel && !this.selectedProduct && !this.selectedTag) {
                this.$refs.form.validate()
            } else {
                let dict = {
                    date: this.date,
                    channel: this.selectedChannel,
                    product: this.selectedProduct,
                    tag: []
                }
                if (this.selectedTag) {
                    dict.tag = [this.selectedTag]
                }
                if (this.href === 'customer') {
                    this.sendSorting('/api/c/sorting', dict)
                    this.$refs.form.reset()
                }
                if (this.href === 'import') {
                    this.sendSorting('/api/m/sorting', dict)
                    this.$refs.form.reset()
                }
                this.$refs.form.reset()
                this.dialogDate = false
            }
        },
        sortingOnclick(data) {
            let dict = {
                date: [],
                channel: null,
                product: null,
                tag: null
            }
            if (data.channel) {
                dict.channel = data.channel
            } else if (data.product) {
                dict.product = data.product
            } else if (data.tag) {
                dict.tag = [data.tag]
            }
            if (this.href === 'customer') {
                this.sendSorting('/api/c/sorting', dict)
            }
            if (this.href === 'import') {
                this.sendSorting('/api/m/sorting', dict)
            }
        },
        sendSorting(path, data) {
            this.spinTable = false
            axios.post(path, data)
                .then((res) => {
                    this.spinTable = true
                    this.date = []
                    this.transaction = res.data
                })
                .catch((err) => {
                    this.spinTable = true
                    this.date = []
                    console.error(err)
                })
        },
        async ImportRE(selected) {
            if (this.selected.length === 0) {
                this.snackbar = true
                this.text = `กรุณาเลือกข้อมูลเพื่อนำเข้า RE`
                this.colorSb = 'red'
            } else {
                this.transaction = selected
                this.btnHiddenAPI = false
                this.btnDelete = false
                this.page = 2
                this.snackbar = true
                this.text = `รายการทั้งหมด ${this.transaction.length} รายการ`
                this.colorSb = 'primary'
            }
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
                this.selected = []
                this.model = []
            } else if (data === 'api') {
                this.btnAPI = true
                this.btnHiddenAPI = false
                this.btnImport = false
                this.transaction = []
                this.selected = []
                this.model = []
            }
        },
        sendDeleteMultiple() {
            if (this.href === 'customer') {
                this.deleteMultiple('/api/customer/delete/multiple', this.selected)
            } else if (this.href === 'import') {
                this.deleteMultiple('/api/import/delete/multiple', this.selected)
            }
        },
        deleteMultiple(path, selected) {
            this.spinDelete = false
            axios.post(path, selected)
                .then((res) => {
                    this.selected.forEach((data) => {
                        this.transaction.splice(this.transaction.indexOf(data), 1)
                    })
                    this.spinDelete = true
                    this.selected = []
                    console.log(res.data)
                })
                .catch((err) => {
                    this.spinDelete = true
                    this.selected = []
                    console.error(err)
                })
        },
        colorProduct(product) {
            if (product === 'Construction') {
                return 'green accent-1'
            }
            if (product === 'RealEstate') {
                return 'blue lighten-4'
            }
            if (product === 'Project Planning') {
                return 'pink lighten-4'
            }
            if (product === 'Consulting') {
                return 'yellow lighten-4'
            }
        },
        async addTransaction(data) {
            let href = this.href
            if (href === 'customer')
                this.path = '/api/customer'
            if (href === 'import')
                this.path = '/api/import'
            data.uid = this.userAuth.uid
            data.username = this.userAuth.name
            await axios.post(this.path, data)
                .then((res) => {
                    this.spinButton = true;
                    this.transaction.unshift(res.data);
                    this.text = `คุณได้เพิ่มข้อมูล ${this.editedItem.name}`
                    this.colorSb = 'success'
                    this.snackbar = true
                })
                .catch((err) => {
                    this.spinButton = true;
                    console.log(err);
                })
        },
        async editTransaction(data, id) {
            let href = this.href
            if (href === 'customer')
                this.path = `/api/customer/${id}`
            if (href === 'import')
                this.path = `/api/import/${id}`
            if (!data.tag) {
                data.tag = []
            }
            await axios.put(this.path, data)
                .then(() => {
                    this.spinButton = true;
                    this.colorSb = 'primary'
                    this.text = `คุณได้อัพเดทข้อมูล ${this.editedItem.name}`
                    this.snackbar = true
                })
                .catch((err) => {
                    this.spinButton = true;
                    console.log(err);
                })
        }
        ,
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
                    this.colorSb = 'red'
                    this.text = `คุณได้ลบข้อมูล ${this.editedItem.name}`
                    this.snackbar = true
                })
                .catch((err) => {
                    this.spinButton = true;
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
        async getTags() {
            const path = '/api/tag'
            await axios.get(path)
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
                    if (this.href === 'customer') {
                        this.initialize()
                    } else if (this.href === 'import') {
                        this.APIImport()
                    }
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
        }
        ,

    }
    ,
    delimiters: ["[[", "]]"]
})