/**
 * Minified by jsDelivr using Terser v3.14.1.
 * Original file: /npm/vue-scrollto@2.18.1/vue-scrollto.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
!(function (e, n) {
  "object" == typeof exports && "undefined" != typeof module
    ? (module.exports = n())
    : "function" == typeof define && define.amd
    ? define(n)
    : ((e = e || self)["vue-scrollto"] = n());
})(this, function () {
  "use strict";
  function e(n) {
    return (e =
      "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
        ? function (e) {
            return typeof e;
          }
        : function (e) {
            return e &&
              "function" == typeof Symbol &&
              e.constructor === Symbol &&
              e !== Symbol.prototype
              ? "symbol"
              : typeof e;
          })(n);
  }
  function n() {
    return (n =
      Object.assign ||
      function (e) {
        for (var n = 1; n < arguments.length; n++) {
          var t = arguments[n];
          for (var o in t)
            Object.prototype.hasOwnProperty.call(t, o) && (e[o] = t[o]);
        }
        return e;
      }).apply(this, arguments);
  }
  var t = 4,
    o = 0.001,
    r = 1e-7,
    i = 10,
    u = 11,
    f = 1 / (u - 1),
    a = "function" == typeof Float32Array;
  function c(e, n) {
    return 1 - 3 * n + 3 * e;
  }
  function l(e, n) {
    return 3 * n - 6 * e;
  }
  function s(e) {
    return 3 * e;
  }
  function d(e, n, t) {
    return ((c(n, t) * e + l(n, t)) * e + s(n)) * e;
  }
  function v(e, n, t) {
    return 3 * c(n, t) * e * e + 2 * l(n, t) * e + s(n);
  }
  function y(e) {
    return e;
  }
  var p = function (e, n, c, l) {
      if (!(0 <= e && e <= 1 && 0 <= c && c <= 1))
        throw new Error("bezier x values must be in [0, 1] range");
      if (e === n && c === l) return y;
      for (var s = a ? new Float32Array(u) : new Array(u), p = 0; p < u; ++p)
        s[p] = d(p * f, e, c);
      function m(n) {
        for (var a = 0, l = 1, y = u - 1; l !== y && s[l] <= n; ++l) a += f;
        var p = a + ((n - s[--l]) / (s[l + 1] - s[l])) * f,
          m = v(p, e, c);
        return m >= o
          ? (function (e, n, o, r) {
              for (var i = 0; i < t; ++i) {
                var u = v(n, o, r);
                if (0 === u) return n;
                n -= (d(n, o, r) - e) / u;
              }
              return n;
            })(n, p, e, c)
          : 0 === m
          ? p
          : (function (e, n, t, o, u) {
              var f,
                a,
                c = 0;
              do {
                (f = d((a = n + (t - n) / 2), o, u) - e) > 0
                  ? (t = a)
                  : (n = a);
              } while (Math.abs(f) > r && ++c < i);
              return a;
            })(n, a, a + f, e, c);
      }
      return function (e) {
        return 0 === e ? 0 : 1 === e ? 1 : d(m(e), n, l);
      };
    },
    m = {
      ease: [0.25, 0.1, 0.25, 1],
      linear: [0, 0, 1, 1],
      "ease-in": [0.42, 0, 1, 1],
      "ease-out": [0, 0, 0.58, 1],
      "ease-in-out": [0.42, 0, 0.58, 1],
    },
    w = !1;
  try {
    var b = Object.defineProperty({}, "passive", {
      get: function () {
        w = !0;
      },
    });
    window.addEventListener("test", null, b);
  } catch (e) {}
  var g = {
      $: function (e) {
        return "string" != typeof e ? e : document.querySelector(e);
      },
      on: function (e, n, t) {
        var o =
          arguments.length > 3 && void 0 !== arguments[3]
            ? arguments[3]
            : { passive: !1 };
        n instanceof Array || (n = [n]);
        for (var r = 0; r < n.length; r++)
          e.addEventListener(n[r], t, !!w && o);
      },
      off: function (e, n, t) {
        n instanceof Array || (n = [n]);
        for (var o = 0; o < n.length; o++) e.removeEventListener(n[o], t);
      },
      cumulativeOffset: function (e) {
        var n = 0,
          t = 0;
        do {
          (n += e.offsetTop || 0),
            (t += e.offsetLeft || 0),
            (e = e.offsetParent);
        } while (e);
        return { top: n, left: t };
      },
    },
    h = [
      "mousedown",
      "wheel",
      "DOMMouseScroll",
      "mousewheel",
      "keyup",
      "touchmove",
    ],
    L = {
      container: "body",
      duration: 500,
      easing: "ease",
      offset: 0,
      force: !0,
      cancelable: !0,
      onStart: !1,
      onDone: !1,
      onCancel: !1,
      x: !1,
      y: !0,
    };
  function S(e) {
    L = n({}, L, e);
  }
  var O = (function () {
      var n,
        t,
        o,
        r,
        i,
        u,
        f,
        a,
        c,
        l,
        s,
        d,
        v,
        y,
        w,
        b,
        S,
        O,
        T,
        E,
        x,
        A,
        C,
        D,
        P = function (e) {
          f && ((E = e), (T = !0));
        };
      function j(e) {
        if (T) return F();
        A || (A = e),
          (C = e - A),
          (D = Math.min(C / o, 1)),
          (D = x(D)),
          H(t, w + O * D, v + S * D),
          C < o ? window.requestAnimationFrame(j) : F();
      }
      function F() {
        T || H(t, b, y),
          (A = !1),
          g.off(t, h, P),
          T && l && l(E, n),
          !T && c && c(n);
      }
      function H(e, n, t) {
        d && (e.scrollTop = n),
          s && (e.scrollLeft = t),
          "body" === e.tagName.toLowerCase() &&
            (d && (document.documentElement.scrollTop = n),
            s && (document.documentElement.scrollLeft = t));
      }
      return function (A, C) {
        var D =
          arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {};
        if (
          ("object" === e(C)
            ? (D = C)
            : "number" == typeof C && (D.duration = C),
          !(n = g.$(A)))
        )
          return console.warn(
            "[vue-scrollto warn]: Trying to scroll to an element that is not on the page: " +
              A
          );
        (t = g.$(D.container || L.container)),
          (o = D.duration || L.duration),
          (r = D.easing || L.easing),
          (i = D.hasOwnProperty("offset") ? D.offset : L.offset),
          (u = D.hasOwnProperty("force") ? !1 !== D.force : L.force),
          (f = D.hasOwnProperty("cancelable")
            ? !1 !== D.cancelable
            : L.cancelable),
          (a = D.onStart || L.onStart),
          (c = D.onDone || L.onDone),
          (l = D.onCancel || L.onCancel),
          (s = void 0 === D.x ? L.x : D.x),
          (d = void 0 === D.y ? L.y : D.y);
        var F = g.cumulativeOffset(t),
          H = g.cumulativeOffset(n);
        if (
          ("function" == typeof i && (i = i(n, t)),
          (w = (function (e) {
            var n = e.scrollTop;
            return (
              "body" === e.tagName.toLowerCase() &&
                (n = n || document.documentElement.scrollTop),
              n
            );
          })(t)),
          (b = H.top - F.top + i),
          (v = (function (e) {
            var n = e.scrollLeft;
            return (
              "body" === e.tagName.toLowerCase() &&
                (n = n || document.documentElement.scrollLeft),
              n
            );
          })(t)),
          (y = H.left - F.left + i),
          (T = !1),
          (O = b - w),
          (S = y - v),
          !u)
        ) {
          var M =
              "body" === t.tagName.toLowerCase()
                ? document.documentElement.clientHeight || window.innerHeight
                : t.offsetHeight,
            N = w,
            V = N + M,
            $ = b - i,
            k = $ + n.offsetHeight;
          if ($ >= N && k <= V) return void (c && c(n));
        }
        if ((a && a(n), O || S))
          return (
            "string" == typeof r && (r = m[r] || m.ease),
            (x = p.apply(p, r)),
            g.on(t, h, P, { passive: !0 }),
            window.requestAnimationFrame(j),
            function () {
              (E = null), (T = !0);
            }
          );
        c && c(n);
      };
    })(),
    T = [];
  function E(e) {
    var n = (function (e) {
      for (var n = 0; n < T.length; ++n) if (T[n].el === e) return T[n];
    })(e);
    return n || (T.push((n = { el: e, binding: {} })), n);
  }
  function x(e) {
    var n = E(this).binding;
    if (n.value) {
      if ((e.preventDefault(), "string" == typeof n.value)) return O(n.value);
      O(n.value.el || n.value.element, n.value);
    }
  }
  var A = {
      bind: function (e, n) {
        (E(e).binding = n), g.on(e, "click", x);
      },
      unbind: function (e) {
        !(function (e) {
          for (var n = 0; n < T.length; ++n)
            if (T[n].el === e) return T.splice(n, 1), !0;
        })(e),
          g.off(e, "click", x);
      },
      update: function (e, n) {
        E(e).binding = n;
      },
      scrollTo: O,
      bindings: T,
    },
    C = function (e, n) {
      n && S(n),
        e.directive("scroll-to", A),
        (e.prototype.$scrollTo = A.scrollTo);
    };
  return (
    "undefined" != typeof window &&
      window.Vue &&
      ((window.VueScrollTo = A),
      (window.VueScrollTo.setDefaults = S),
      window.Vue.use(C)),
    (A.install = C),
    A
  );
});
//# sourceMappingURL=/sm/86a08586651296024bb85e4d41ebe16e9d37ed32704b6d173a2db307be70fcc0.map
