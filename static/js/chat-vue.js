var app = new Vue({
  delimiters: ["[[", "]]"],
  el: "#app",
  name: "chat",
  data: {
    messages: [
      {
        message: "Nulla consequat massa quis enim. Donec pede juso, fringilla vell...",
        sender: "you",
        timeSend: 10000,
      },
      {
        message: "rhoncus ut, imperdiet a, venenatis vitae, justo...",
        sender: "you",
        timeSend: 10001,
      },
      {
        message: "Image 🤦‍♀️😎💖",
        sender: "you",
        timeSend: 10002,
      },
      {
        message: "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.",
        sender: "friend",
        timeSend: 10003,
      },
      {
        message: "Nallum dictom felis eu pede mollis pretium",
        sender: "you",
        timeSend: 10004,
      },
      {
        message: "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor",
        sender: "friend",
        timeSend: 10005,
      },
      {
        message: "Nulla consequat massa quis enim. Donec pede juso, fringilla vell...",
        sender: "you",
        timeSend: 10006,
      },
      {
        message: "Maecenas tempus, tellus eget condimentum rhoncus",
        sender: "friend",
        timeSend: 10007,
      },
      {
        message: "Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus.",
        sender: "you",
        timeSend: 10008,
      },
    ],
    chat_threads: [],
    chat_messages: [],
    chat_id: "",
    message: "",
    // url: "",
    socket: {},
  },
  async created() {
    await this.getAllChats();
    await this.getSingleChat();
    // const url = "wss://echo.websocket.org/";
    const url = window.location.href.replace("http", "ws");
    this.socket = new WebSocket(url);
    await this.websocket();
    // console.log(window.location.pathname.split("/", 3));
  },
  methods: {
    async getAllChats() {
      // let user_id = this.$route.params.id;
      try {
        await fetch(`/chat/api/threads/1`)
          .then((response) => response.json())
          .then((data) => {
            console.log("data>>>", data);
            this.chat_threads = data.chat_threads;
          });
      } catch (error) {
        console.error(error);
      }
    },
    async getSingleChat() {
      // let user_id = this.$route.params.id;
      try {
        await fetch(`/chat/api/chat/1`)
          .then((response) => response.json())
          .then((data) => {
            console.log("data>>>", data);
            this.chat_id = data.chat_id;
            this.chat_messages = data.chat_list;
          });
      } catch (error) {
        console.error(error);
      }
    },
    async websocket() {
      // // const url = "ws://127.0.0.1:8000/chat/";
      // const url = "wss://echo.websocket.org/";
      // const socket = new WebSocket(url);
      this.socket.onclose = (e) => {
        console.log("WebSocket Disconnected", e);
      };

      this.socket.onopen = (e) => {
        console.log("WebSocket Connected", e);
        // this.socket.send(JSON.stringify({ chat_id: 1, username: "Louisane", function: "connect" }));
      };

      this.socket.onerror = (e) => {
        console.log("WebSocket Error", e);
      };

      this.socket.onmessage = (e) => {
        this.messages.push(JSON.parse(e.data));
        console.log("WebSocket received message", e);
      };
    },

    sendMessage() {
      // const url = "wss://echo.websocket.org/";
      // const socket = new WebSocket(url);
      // send message from the form
      this.socket.onopen();
      let outgoingMessage = {
        // chat_id: this.chat_id,
        message: this.message,
        timeSend: Date.now(),
        sender: "you",
      };
      // console.log(outgoingMessage);
      this.socket.send(JSON.stringify(outgoingMessage));
      this.message = "";
    },
  },
});
