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
  },
  async mounted() {
    await this.getAllChats();
    await this.getSingleChat();
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
            this.chat_messages = data.chat_messages;
          });
      } catch (error) {
        console.error(error);
      }
    },
  },
});
