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
    username: "",
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
    scrollToBottom() {
      let container = this.$el.querySelector("#container");
      container.scrollTop = container.scrollHeight;
    },
    async websocket() {
      this.socket.onclose = (e) => {
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
        // this.$refs.container.scrollIntoView();
        console.log(JSON.parse(e.data));
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
              this.username = data.username;
            }
          });
      } catch (error) {
        console.log("error>>>", error);
      }
    },
    async getAllChats() {
      try {
        await fetch(`/chat/api/threads/${this.id}`)
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
      this.chat_object = chat;
      try {
        await fetch(`/chat/api/chat/${chat.chat_id}`)
          .then((response) => response.json())
          .then((data) => {
            console.log("single chat>>>", data);
            this.chat_id = data.chat_id;
            this.chat_messages = data.chat_list;
          });
        // this.$refs.container.scrollIntoView();
        this.connect();
      } catch (error) {
        console.log("error>>>", error);
      }
    },
    connect() {
      let chat_thread = {
        username: this.username,
        chat_id: this.chat_id,
        function: "connect",
      };
      console.log("chat_thread>>>", chat_thread);
      this.socket.send(JSON.stringify(chat_thread));
    },
    sendMessage() {
      let thread_obj = {
        sender_id: this.id,
        message: this.message,
        sender: this.username,
        function: "message",
      };
      this.socket.send(JSON.stringify(thread_obj));
      console.log("thread_obj>>>", thread_obj);
      this.message = "";
      this.getSingleChat(this.chat_object);
    },
  },
});
