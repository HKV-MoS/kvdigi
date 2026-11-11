/* Lernstand für abu-tools.ch
   Meldet gelöste Aufgaben an die Lehrperson (Supabase) und erzeugt einen Abschluss-Code für kv digital.
   Einbinden:  <script src="lernstand.js?v=1"></script>
   Starten:    Lernstand.start({tool, titel, total, kuerzel, ziel, alle, stats})
   Melden:     Lernstand.melden(aufgabe, ok, {n, g, t})
*/
(function () {
  "use strict";
  var API = "https://eebmnyxqlubirwyykofo.supabase.co/rest/v1/rpc/";
  var APIKEY = "sb_publishable_kaEkMADZLvc-Jok0dlxkBA_u3cbNaQt";
  var SPEICHER = "abu_lernstand_v1";
  var CODE_ABC = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";

  function rpc(fn, daten) {
    return fetch(API + fn, { method: "POST", headers: { "apikey": APIKEY, "Content-Type": "application/json" }, body: JSON.stringify(daten) })
      .then(function (r) {
        return r.text().then(function (t) {
          var j = null; try { j = JSON.parse(t); } catch (e) {}
          if (!r.ok) throw new Error((j && j.message) || ("Fehler " + r.status));
          return j;
        });
      });
  }
  function lesen(k, ersatz) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : ersatz; } catch (e) { return ersatz; } }
  function schreiben(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function vorname(s) { return String(s || "").trim().replace(/\s+/g, " ").replace(/(^|[\s-])(\p{Ll})/gu, function (m, a, b) { return a + b.toLocaleUpperCase("de-CH"); }); }
  function nameOk(s) { return /^[\p{L}][\p{L} .'’-]{0,29}$/u.test(s); }

  /* Prüfzeichen für den Abschluss-Code (FNV-1a). Schützt nicht vor Profis, aber vor Abtippen und Ändern. */
  function pruef(text) {
    var h = 0x811c9dc5, s = "abu-tools·lernstand·26|" + text;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    var out = "";
    for (var j = 0; j < 4; j++) { out += CODE_ABC[h % 32]; h = Math.floor(h / 32); }
    return out;
  }
  function abschlussCode(kuerzel, richtig, total, name) {
    return kuerzel + " " + richtig + "/" + total + " · " + name + " · " + pruef(kuerzel + "|" + richtig + "|" + total + "|" + name.toLowerCase());
  }
  function codePruefen(code) {
    var m = String(code || "").trim().match(/^([A-Z0-9]{2,8})\s+(\d+)\/(\d+)\s*·\s*(.+?)\s*·\s*([A-Z0-9]{4})$/);
    if (!m) return null;
    return { kuerzel: m[1], richtig: +m[2], total: +m[3], name: m[4], echt: pruef(m[1] + "|" + m[2] + "|" + m[3] + "|" + m[4].toLowerCase()) === m[5] };
  }

  var CSS = '' +
    '.ls-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:14px;line-height:1.4;border:1px solid var(--line,#d4dedb);border-radius:10px;padding:8px 12px;margin:12px 0 4px;background:var(--surface,#fff);color:var(--ink,#17302b)}' +
    '.ls-bar.ls-bitte{background:var(--mid-soft,#fbf0d6);border-color:var(--mid,#9a6b00)}' +
    '.ls-bar .ls-sp{flex:1}' +
    '.ls-bar b{font-weight:700}' +
    '.ls-bar input{font:inherit;font-size:15px;padding:5px 8px;border:1px solid var(--line,#d4dedb);border-radius:8px;background:var(--bg,#eef2f1);color:var(--ink,#17302b);width:150px}' +
    '.ls-bar button,.ls-dlg button{font:inherit;font-size:14px;font-weight:600;border-radius:8px;padding:5px 11px;cursor:pointer;border:1px solid var(--brand,#0b3d36);background:var(--surface,#fff);color:var(--brand,#0b3d36)}' +
    '.ls-bar button.ls-voll,.ls-dlg button.ls-voll{background:var(--brand,#0b3d36);color:var(--surface,#fff)}' +
    '.ls-bar .ls-link{border:0;background:none;padding:2px 4px;text-decoration:underline;font-weight:500;color:var(--muted,#5b6e69)}' +
    '.ls-stat{font-size:13px;color:var(--muted,#5b6e69)}.ls-stat.ls-ok{color:var(--ok,#1f7a4d)}.ls-stat.ls-warn{color:var(--bad,#b03a2e)}' +
    '.ls-klein{flex-basis:100%;font-size:12.5px;color:var(--muted,#5b6e69)}' +
    '.ls-fehler{flex-basis:100%;font-size:13px;color:var(--bad,#b03a2e);font-weight:600}' +
    '.ls-dlg{position:fixed;inset:0;background:rgba(10,40,45,.5);display:flex;align-items:center;justify-content:center;z-index:50;padding:16px}' +
    '.ls-dlg>div{background:var(--surface,#fff);color:var(--ink,#17302b);border-radius:12px;padding:18px 20px;max-width:460px;width:100%;box-shadow:0 8px 30px rgba(0,0,0,.25)}' +
    '.ls-dlg h3{margin:0 0 8px;font-size:18px}.ls-dlg p{margin:0 0 10px;font-size:14.5px}' +
    '.ls-code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:18px;font-weight:700;background:var(--brand-soft,#e3eeeb);border-radius:8px;padding:10px 12px;margin:6px 0 12px;word-break:break-word;user-select:all}' +
    '.ls-row{display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap}';

  var L = {
    cfg: null, el: null, st: null, warteschlange: [], timer: null, status: "",
    start: function (cfg) {
      this.cfg = cfg;
      if (!document.getElementById("ls-css")) { var s = document.createElement("style"); s.id = "ls-css"; s.textContent = CSS; document.head.appendChild(s); }
      this.st = lesen(SPEICHER, {}) || {};
      var k = null;
      try { k = new URLSearchParams(location.search).get("k"); } catch (e) {}
      if (k) { k = k.trim().toUpperCase(); if (k !== this.st.k) { this.st.k = k; this.st.kname = ""; schreiben(SPEICHER, this.st); this._neu = true; this.klassePruefen(); } }
      this.warteschlange = lesen(SPEICHER + "_q_" + cfg.tool, []) || [];
      this.el = document.createElement("div"); this.el.className = "ls-bar";
      if (cfg.ziel && cfg.ziel.parentNode) cfg.ziel.parentNode.insertBefore(this.el, cfg.ziel.nextSibling);
      else document.body.insertBefore(this.el, document.body.firstChild);
      this.zeichne();
      if (this.warteschlange.length) this.senden();
    },
    angemeldet: function () { return !!(this.st.k && this.st.name); },
    klassePruefen: function () {
      var self = this;
      return rpc("lern_klasse_info", { p_klasse: this.st.k }).then(function (j) {
        if (j && j.code) { self.st.kname = j.name; self.st.kfehler = false; if (self._neu && self.st.name) { self._neu = false; schreiben(SPEICHER, self.st); self.zeichne(); self.nachtragen(); return; } }
        else { self.st.kfehler = true; }
        schreiben(SPEICHER, self.st); self.zeichne();
      }).catch(function () {});
    },
    zeichne: function (fehler, offen) {
      var s = this.st, el = this.el, self = this; if (!el) return;
      el.className = "ls-bar";
      var klassenTxt = s.k ? "Klasse <b>" + esc(s.kname || s.k) + "</b>" : "";
      if (this.angemeldet() && !offen) {
        el.innerHTML = '<span>✓ <b>' + esc(s.name) + '</b> · ' + klassenTxt + '</span>' +
          '<span class="ls-stat ' + (this.status === "ok" ? "ls-ok" : this.status === "warn" ? "ls-warn" : "") + '">' +
          (this.status === "ok" ? "Lernstand gespeichert" : this.status === "warn" ? "Offline, wird nachgesendet" : this.status === "send" ? "wird gesendet …" : "Ihre Lehrperson sieht Ihren Lernstand") + '</span>' +
          '<span class="ls-sp"></span><button type="button" class="ls-code-btn">Abschluss-Code</button><button type="button" class="ls-link ls-aendern">ändern</button>' +
          (s.kfehler ? '<span class="ls-fehler">Den Klassencode ' + esc(s.k) + ' gibt es nicht. Fragen Sie Ihre Lehrperson.</span>' : "");
        el.querySelector(".ls-aendern").onclick = function () { self.zeichne(null, true); };
        el.querySelector(".ls-code-btn").onclick = function () { self.codeDialog(); };
        return;
      }
      if (!s.k && !offen && s.name) {
        el.innerHTML = '<span>Angemeldet als <b>' + esc(s.name) + '</b>, ohne Klasse</span><span class="ls-sp"></span>' +
          '<button type="button" class="ls-code-btn">Abschluss-Code</button><button type="button" class="ls-link ls-aendern">Klasse eintragen</button>';
        el.querySelector(".ls-aendern").onclick = function () { self.zeichne(null, true); };
        el.querySelector(".ls-code-btn").onclick = function () { self.codeDialog(); };
        return;
      }
      if (!s.k && !offen) {
        el.innerHTML = '<span class="ls-stat">Lernstand für Ihre Lehrperson</span><span class="ls-sp"></span><button type="button" class="ls-link ls-aendern">Anmelden</button>';
        el.querySelector(".ls-aendern").onclick = function () { self.zeichne(null, true); };
        return;
      }
      el.className = "ls-bar ls-bitte";
      var mitKlasse = !s.k || offen;
      el.innerHTML = '<span>' + (s.k && !offen ? klassenTxt + ': Tragen Sie Ihren Vornamen ein, damit Ihre Lehrperson sieht, was Sie gelöst haben.' : 'Für Ihre Lehrperson anmelden:') + '</span>' +
        (mitKlasse ? '<input class="ls-k" placeholder="Klassencode" autocomplete="off" spellcheck="false" value="' + esc(s.k || "") + '" aria-label="Klassencode">' : "") +
        '<input class="ls-n" placeholder="Vorname" autocomplete="given-name" spellcheck="false" maxlength="30" value="' + esc(s.name || "") + '" aria-label="Vorname">' +
        '<button type="button" class="ls-voll ls-ok-btn">Eintragen</button>' + (offen ? '<button type="button" class="ls-link ls-abbr">Abbrechen</button>' : "") +
        (fehler ? '<span class="ls-fehler">' + esc(fehler) + '</span>' : "") +
        '<span class="ls-klein">Gespeichert werden Ihr Vorname, die Klasse und ob Ihre Antworten richtig waren. Sehen kann das nur Ihre Lehrperson.' + (mitKlasse ? " Ohne Klassencode wird nichts gesendet; Sie erhalten nur den Abschluss-Code." : "") + '</span>';
      var ok = el.querySelector(".ls-ok-btn"), n = el.querySelector(".ls-n"), k = el.querySelector(".ls-k");
      function los() { self.anmelden(k ? k.value : s.k, n.value); }
      ok.onclick = los;
      n.addEventListener("keydown", function (e) { if (e.key === "Enter") los(); });
      if (k) k.addEventListener("keydown", function (e) { if (e.key === "Enter") los(); });
      var ab = el.querySelector(".ls-abbr"); if (ab) ab.onclick = function () { self.zeichne(); };
    },
    anmelden: function (k, name) {
      var self = this; name = vorname(name); k = String(k || "").trim().toUpperCase();
      if (!nameOk(name)) { this.zeichne("Bitte nur den Vornamen eintragen (Buchstaben, höchstens 30 Zeichen).", true); return; }
      if (!k) { this.st.k = ""; this.st.kname = ""; this.st.name = name; schreiben(SPEICHER, this.st); this.zeichne(); return; }
      rpc("lern_klasse_info", { p_klasse: k }).then(function (j) {
        if (!j || !j.code) { self.zeichne("Den Klassencode " + k + " gibt es nicht.", true); return; }
        var alt = (self.st.name || "").toLowerCase(), neu = alt !== name.toLowerCase() || self.st.k !== j.code;
        // Lokale Resultate nur nachsenden, wenn auf diesem Gerät noch niemand anderes angemeldet war
        var nachsenden = neu && (alt === "" || alt === name.toLowerCase());
        self.st = { k: j.code, kname: j.name, name: name }; schreiben(SPEICHER, self.st);
        self.zeichne();
        if (nachsenden) self.nachtragen();
      }).catch(function () { self.zeichne("Keine Verbindung. Versuchen Sie es später nochmals.", true); });
    },
    nachtragen: function () {
      if (!this.angemeldet() || !this.cfg.alle) return;
      var liste = this.cfg.alle() || [], self = this;
      if (!liste.length) return;
      this.status = "send"; this.zeichne();
      rpc("lern_melden", { p_klasse: this.st.k, p_name: this.st.name, p_tool: this.cfg.tool, p_titel: this.cfg.titel, p_total: this.cfg.total, p_liste: liste.slice(0, 300), p_nachtrag: true })
        .then(function () { self.status = "ok"; self.zeichne(); })
        .catch(function () { self.status = "warn"; self.zeichne(); });
    },
    melden: function (a, ok, meta) {
      if (!this.angemeldet()) return;
      meta = meta || {};
      this.warteschlange.push({ a: String(a), ok: !!ok, n: meta.n, g: meta.g, t: meta.t ? String(meta.t).slice(0, 140) : undefined });
      schreiben(SPEICHER + "_q_" + this.cfg.tool, this.warteschlange);
      var self = this; clearTimeout(this.timer); this.timer = setTimeout(function () { self.senden(); }, 400);
    },
    senden: function () {
      if (!this.angemeldet() || !this.warteschlange.length || this.laeuft) return;
      var paket = this.warteschlange.slice(0, 100), self = this; this.laeuft = true;
      this.status = "send"; this.zeichne();
      rpc("lern_melden", { p_klasse: this.st.k, p_name: this.st.name, p_tool: this.cfg.tool, p_titel: this.cfg.titel, p_total: this.cfg.total, p_liste: paket, p_nachtrag: false })
        .then(function () {
          self.laeuft = false; self.warteschlange = self.warteschlange.slice(paket.length);
          schreiben(SPEICHER + "_q_" + self.cfg.tool, self.warteschlange);
          self.status = "ok"; self.zeichne();
          if (self.warteschlange.length) self.senden();
        })
        .catch(function (e) {
          self.laeuft = false;
          if (/Klasse nicht gefunden|Ungültig/.test(e.message)) { self.warteschlange = []; schreiben(SPEICHER + "_q_" + self.cfg.tool, []); self.st.kfehler = /Klasse/.test(e.message); }
          self.status = "warn"; self.zeichne();
          clearTimeout(self.timer); self.timer = setTimeout(function () { self.senden(); }, 20000);
        });
    },
    codeDialog: function () {
      var s = this.cfg.stats ? this.cfg.stats() : { richtig: 0, total: this.cfg.total };
      var code = abschlussCode(this.cfg.kuerzel || "ABU", s.richtig, s.total || this.cfg.total, this.st.name);
      var d = document.createElement("div"); d.className = "ls-dlg"; d.setAttribute("role", "dialog"); d.setAttribute("aria-modal", "true");
      d.innerHTML = '<div><h3>Abschluss-Code</h3><p>' + esc(this.cfg.titel) + ': <b>' + s.richtig + ' von ' + (s.total || this.cfg.total) + '</b> richtig.</p>' +
        '<div class="ls-code">' + esc(code) + '</div>' +
        '<p>Kopieren Sie den Code und fügen Sie ihn in kv digital in die Textfrage unter dieser Folie ein.</p>' +
        '<div class="ls-row"><span class="ls-stat ls-msg" style="margin-right:auto"></span><button type="button" class="ls-kop ls-voll">Kopieren</button><button type="button" class="ls-zu">Schliessen</button></div></div>';
      document.body.appendChild(d);
      var msg = d.querySelector(".ls-msg");
      d.querySelector(".ls-kop").onclick = function () {
        var fertig = function () { msg.textContent = "Kopiert."; };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(code).then(fertig, function () { msg.textContent = "Bitte den Code markieren und kopieren."; });
        else msg.textContent = "Bitte den Code markieren und kopieren.";
      };
      function zu() { d.remove(); }
      d.querySelector(".ls-zu").onclick = zu;
      d.addEventListener("click", function (e) { if (e.target === d) zu(); });
      document.addEventListener("keydown", function k(e) { if (e.key === "Escape") { zu(); document.removeEventListener("keydown", k); } });
    },
    abschlussCode: abschlussCode,
    codePruefen: codePruefen,
    rpc: rpc
  };
  window.Lernstand = L;
})();
