/*!
 * quizmusik.js – gemeinsame Quizmusik fuer abu-tools
 *
 * Einbinden (vor dem Quizskript, sonst bleibt Frage 1 stumm):
 *   <script src="quizmusik.js?v=2"></script>
 *
 * Im Quiz aufrufen:
 *   QuizMusik.frage(istLetzteFrage)   // Musik zur Frage starten
 *   QuizMusik.stopp()                 // beim Antworten / Rundenende
 *   QuizMusik.sieg()                  // Fanfare, wenn das Quiz geschafft ist
 *   QuizMusik.aktiv(true|false)       // nur dort, wo das Quiz sichtbar ist
 *
 * aktiv(false) blendet den Schalter aus und haelt die Musik an, ohne die
 * angemeldete Tonspur zu vergessen – beim naechsten aktiv(true) laeuft sie
 * weiter. Seiten, die aktiv() nie aufrufen, verhalten sich wie bisher.
 *
 * Dateien: millionaer_musik.mp3 (Standard), millionaer_musik_final.mp3
 * (letzte Frage), millionaer_musik_sieg.mp3 (Fanfare, einmalig).
 * Fehlt eine Datei, passiert schlicht nichts.
 */
(function (global) {
  'use strict';

  var cfg = {
    standard: 'millionaer_musik.mp3?v=1',
    final: 'millionaer_musik_final.mp3?v=1',
    sieg: 'millionaer_musik_sieg.mp3?v=1',
    lautstaerke: 0.30,
    lautstaerkeFinal: 0.34,
    lautstaerkeSieg: 0.42,
    an: true                    // Grundeinstellung: Musik eingeschaltet
  };

  var spuren = {};              // url -> Audio
  var aktuell = null;           // laufendes Audio
  var wunsch = null;            // {url, vol, schleife} – was laufen soll
  var freigegeben = false;      // Browser erlaubt Wiedergabe
  var imBereich = true;         // ist das Quiz gerade sichtbar?
  var schalter = null;

  function hole(url, vol, schleife) {
    if (!spuren[url]) {
      var a = new Audio(url);
      a.preload = 'auto';
      a.addEventListener('error', function () { /* Datei fehlt: still bleiben */ });
      spuren[url] = a;
    }
    spuren[url].loop = schleife !== false;
    spuren[url].volume = vol;
    return spuren[url];
  }

  function ausblenden(a) {
    if (!a || a.paused) return;
    var start = a.volume, i = 0, schritte = 12;
    var t = setInterval(function () {
      i++;
      a.volume = Math.max(0, start * (1 - i / schritte));
      if (i >= schritte) {
        clearInterval(t);
        a.pause();
        a.currentTime = 0;
        a.volume = start;
      }
    }, 40);
  }

  function spiele() {
    if (!wunsch || !cfg.an || !imBereich) return;
    var a = hole(wunsch.url, wunsch.vol, wunsch.schleife);
    if (aktuell && aktuell !== a) ausblenden(aktuell);
    aktuell = a;
    if (a.paused) {
      a.currentTime = 0;
      var p = a.play();
      if (p && p.catch) {
        p.then(function () { freigegeben = true; })
         .catch(function () { freigegeben = false; });
      }
    }
  }

  // Erste Interaktion schaltet die Wiedergabe frei
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {
    document.addEventListener(ev, function einmal() {
      freigegeben = true;
      spiele();
      ['pointerdown', 'keydown', 'touchstart'].forEach(function (e2) {
        document.removeEventListener(e2, einmal);
      });
    });
  });

  function zeichneSchalter() {
    if (schalter) return;
    schalter = document.createElement('button');
    schalter.type = 'button';
    schalter.id = 'quizMusikSchalter';
    schalter.style.cssText =
      'position:fixed;right:14px;bottom:14px;z-index:8000;' +
      'font:600 13px/1 system-ui,-apple-system,sans-serif;' +
      'padding:9px 13px;border-radius:999px;cursor:pointer;' +
      'border:1px solid rgba(255,255,255,.28);' +
      'background:rgba(12,20,44,.86);color:#F3CE8E;' +
      'box-shadow:0 4px 14px rgba(0,0,0,.3)';
    schalter.addEventListener('click', function () { QuizMusik.umschalten(); });
    document.body.appendChild(schalter);
    beschrifte();
  }

  function beschrifte() {
    if (!schalter) return;
    schalter.textContent = cfg.an ? '🔊 Musik' : '🔇 Musik';
    schalter.title = cfg.an ? 'Quizmusik ausschalten' : 'Quizmusik einschalten';
    schalter.setAttribute('aria-pressed', String(cfg.an));
    schalter.style.display = imBereich ? '' : 'none';
  }

  var QuizMusik = {
    init: function (opt) {
      for (var k in (opt || {})) if (opt.hasOwnProperty(k)) cfg[k] = opt[k];
      beschrifte();
      return this;
    },

    /* Musik zur laufenden Frage. istFinale = true -> zweite Tonspur */
    frage: function (istFinale) {
      wunsch = istFinale
        ? { url: cfg.final, vol: cfg.lautstaerkeFinal }
        : { url: cfg.standard, vol: cfg.lautstaerke };
      if (freigegeben) spiele();
    },

    /* Siegesfanfare - laeuft einmal durch, nicht in Schleife */
    sieg: function () {
      wunsch = { url: cfg.sieg, vol: cfg.lautstaerkeSieg, schleife: false };
      if (freigegeben) spiele();
    },

    /* Musik anhalten (Antwort geklickt, Runde vorbei) */
    stopp: function () {
      wunsch = null;
      ausblenden(aktuell);
      aktuell = null;
    },

    /* Quiz sichtbar oder nicht: steuert Schalter und Wiedergabe */
    aktiv: function (ja) {
      imBereich = !!ja;
      beschrifte();
      if (!imBereich) { ausblenden(aktuell); aktuell = null; }
      else if (wunsch && freigegeben) spiele();
      return imBereich;
    },

    umschalten: function () {
      cfg.an = !cfg.an;
      beschrifte();
      if (!cfg.an) { ausblenden(aktuell); aktuell = null; }
      else if (wunsch) spiele();
      return cfg.an;
    },

    get an() { return cfg.an; }
  };

  global.QuizMusik = QuizMusik;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', zeichneSchalter);
  } else {
    zeichneSchalter();
  }
})(window);
