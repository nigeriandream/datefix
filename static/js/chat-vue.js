var app = new Vue({
  delimiters: ["[[", "]]"],
  el: "#app",
  name: "chat",
  data: {
    message: "Hello Vue!",
    // messages: [
    //   {
    //     message: "Nulla consequat massa quis enim. Donec pede juso, fringilla vell...",
    //     sender: "you",
    //     timeSend: 10000,
    //   },
    //   {
    //     message: "rhoncus ut, imperdiet a, venenatis vitae, justo...",
    //     sender: "you",
    //     timeSend: 10001,
    //   },
    //   {
    //     message: "Image 🤦‍♀️😎💖",
    //     sender: "you",
    //     timeSend: 10002,
    //   },
    //   {
    //     message: "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.",
    //     sender: "friend",
    //     timeSend: 10003,
    //   },
    //   {
    //     message: "Nallum dictom felis eu pede mollis pretium",
    //     sender: "you",
    //     timeSend: 10004,
    //   },
    //   {
    //     message: "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor",
    //     sender: "friend",
    //     timeSend: 10005,
    //   },
    //   {
    //     message: "Nulla consequat massa quis enim. Donec pede juso, fringilla vell...",
    //     sender: "you",
    //     timeSend: 10006,
    //   },
    //   {
    //     message: "Maecenas tempus, tellus eget condimentum rhoncus",
    //     sender: "friend",
    //     timeSend: 10007,
    //   },
    //   {
    //     message: "Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus.",
    //     sender: "you",
    //     timeSend: 10008,
    //   },
    // ],
  },
  methods: {
    greet: function (name) {
      console.log("Hello from " + name + "!");
    },
  },
});
