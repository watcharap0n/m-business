new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        connected: null,
        message: 'Kane',
        status: true,

    },
    created() {
        this.initializeWs()
    },
    methods: {
        initializeWs() {
            this.connected = new WebSocket('ws://localhost:8000/ws');
            this.connected.onmessage = (ev) => {
                this.message = ev.data
            }
            this.connected.onopen = (ev) => {
                console.log(ev)
                console.log("Successfully connected to the echo websocket server...")
            }
        },
        sendMessage (message) {
            console.log(this.connected);
            this.connected.send(message);
        },
    },
    delimiters: ["[[", "]]"]
})