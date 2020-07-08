var app = new Vue({
  delimiters: ["[[", "]]"],
  el: "#app",
  name: "chat",
  data: {
    messages: [],
    chat_threads: [],
    chat_messages: [],
    chat_object: {},
    chat_id: "",
    message: "",
    user: "",
    id: "",
    loggedInUser: "",
    loading: true,
    status: "",
    messageStatus: "",
    approving: false,
  },
  async mounted() {
    this.id = this.$refs.userID.value;
    // await this.createThread();
    await this.getUser();
    await this.getAllChats();
    const url = window.location.href.replace("http", "ws");
    this.socket = new WebSocket(url);
    this.websocket();
  },
  beforeDestroy() {
    this.disconnect(this.chat_object);
  },
  methods: {
    async websocket() {
      this.socket.onclose = (e) => {
        this.disconnect();
        console.log("WebSocket Disconnected", e);
      };

      this.socket.onopen = (e) => {
        console.log("WebSocket Connected", e);
      };

      this.socket.onerror = (e) => {
        console.log("WebSocket Error", e);
      };

      this.socket.onmessage = (e) => {
        this.chat_messages.push(JSON.parse(e.data));
        this.getSingleChat(this.chat_object);
        console.log(JSON.parse(e.data));
        let data = JSON.parse(e.data);
        if (
          data.username !== this.loggedInUser &&
          data.function === "connect"
        ) {
          this.status = data.status;
        }
        if (
          data.username !== this.loggedInUser &&
          data.function === "message"
        ) {
          this.messageStatus = data.status;
          console.log(this.messageStatus);
        }
      };
    },
    async createThread() {
      try {
        await fetch(`/chat/api/create/2`)
          .then((response) => response.json())
          .then((data) => {
            console.log("thread>>>", data);
          });
      } catch (error) {
        console.log("error>>>", error);
      }
    },
    async getUser() {
      try {
        await fetch(`/chat/api/user/${this.id}`)
          .then((response) => response.json())
          .then((data) => {
            console.log("user>>>", data);
            if (data !== "None") {
              this.user = data;
              this.loggedInUser = data.username;
            }
          });
      } catch (error) {
        console.log("error>>>", error);
      }
    },
    async getAllChats() {
      try {
        await fetch(`/chat/api/threads`)
          .then((response) => response.json())
          .then((data) => {
            console.log("all chats>>>", data);
            this.chat_threads = data.chat_threads;
          });
      } catch (error) {
        console.log("error>>>", error);
      }
    },
    async getSingleChat(chat) {
      try {
        await fetch(`/chat/api/chat/${chat.chat_id}`)
          .then((response) => response.json())
          .then((data) => {
            console.log("single chat>>>", data);
            this.chat_id = data.chat_id;
            this.chat_messages = data.chat_list;
          });
        this.loading = false;
      } catch (error) {
        console.log("error>>>", error);
      }
    },
    connect(chat) {
      this.chat_object = chat;
      let connect_thread = {
        username: this.loggedInUser,
        chat_id: chat.chat_id,
        function: "connect",
      };
      console.log("connect_thread>>>", connect_thread);
      this.socket.send(JSON.stringify(connect_thread));
    },
    disconnect() {
      let disconnect_thread = {
        username: this.loggedInUser,
        chat_id: this.chat_id,
        function: "disconnect",
      };
      console.log("disconnect_thread>>>", disconnect_thread);
      this.socket.send(JSON.stringify(disconnect_thread));
    },
    sendMessage() {
      let thread_obj = {
        sender_id: this.id,
        message: this.message,
        sender: this.loggedInUser,
        function: "message",
      };
      this.socket.send(JSON.stringify(thread_obj));
      console.log("thread_obj>>>", thread_obj);
      this.message = "";
    },
    jilt() {
      let jilt_thread = {
        username: this.loggedInUser,
        chat_id: this.chat_id,
        function: "jilt",
      };
      console.log("jilt_thread>>>", jilt_thread);
      this.socket.send(JSON.stringify(jilt_thread));
      this.$refs.close.click();
    },
    accept() {
      let accept_thread = {
        username: this.loggedInUser,
        chat_id: this.chat_id,
        function: "accept",
      };
      console.log("accept_thread>>>", accept_thread);
      this.socket.send(JSON.stringify(accept_thread));
      this.$refs.close.click();
    },
  },
  watch: {
    status(newValue, oldValue) {
      this.connect(this.chat_object);
      console.log("value:", newValue, oldValue);
      this.status = newValue;
    },
  },
});
