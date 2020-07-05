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
        console.log("WebSocket received message", e);
        this.getSingleChat(this.chat_object);
        console.log(JSON.parse(e.data));
        let data = JSON.parse(e.data);
        if (
          data.username !== this.loggedInUser &&
          data.function === "connect"
        ) {
          this.status = data.status;
          console.log(this.status);
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
      let chat_thread = {
        username: this.loggedInUser,
        chat_id: chat.chat_id,
        function: "connect",
      };
      console.log("chat_thread>>>", chat_thread);
      this.socket.send(JSON.stringify(chat_thread));
      this.getSingleChat(chat);
    },
    disconnect() {
      let chat_thread = {
        username: this.loggedInUser,
        chat_id: this.chat_id,
        function: "disconnect",
      };
      console.log("chat_thread>>>", chat_thread);
      this.socket.send(JSON.stringify(chat_thread));
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
      this.getSingleChat(this.chat_object);
    },
  },
  watch: {
    status(newValue, oldValue) {
      console.log("value:", newValue, oldValue);
      this.status = newValue;
    },
  },
});
