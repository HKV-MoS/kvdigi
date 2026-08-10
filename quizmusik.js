/*!
 * quizmusik.js – gemeinsame Quizmusik fuer abu-tools
 *
 * Einbinden (am Ende der Seite, vor </body>):
 *   <script src="quizmusik.js?v=1"></script>
 *
 * Im Quiz aufrufen:
 *   QuizMusik.frage(istLetzteFrage)   // Musik zur Frage starten
 *   QuizMusik.stopp()                 // beim Antworten / Rundenende
 *
 * Ohne weitere Konfiguration laeuft millionaer_musik.mp3; bei
 * QuizMusik.frage(true) laeuft millionaer_musik_final.mp3.
 * Die Tonspur startet erst nach der ersten Interaktion auf der Seite –
 * das verlangen die Browser so. Ein Schalter unten rechts blendet sie aus.
 */
(function (global) {
  'use strict';

  var cfg = {
    standard: 'millionaer_musik.mp3?v=1',
    final: 'millionaer_musik_final.mp3?v=1',
    lautstaerke: 0.30,
    lautstaerkeFinal: 0.34,
    an: true                    // Grundeinstellung: Musik eingeschaltet
  };

  var spuren = {};              // url -> Audio
  var aktuell = null;           // laufendes Audio
  var wunsch = null;            // {url, vol} – was laufen soll, sobald erlaubt
  var freigegeben = false;      // Browser erlaubt Wiedergabe
  var schalter = null;

  function hole(url, vol) {
    if (!spuren[url]) {
      var a = new Audio(url);
      a.loop = true;
      a.preload = 'auto';
      spuren[url] = a;
    }
    spuren[url].volume = vol;
    return spuren[url];
  }

  function ausblenden(a) {
    if (!a || a.paused) return;
    var start = a.volume;
    var schritte = 12;
    var i = 0;
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
    if (!wunsch || !cfg.an) return;
    var a = hole(wunsch.url, wunsch.vol);
    if (aktuell && aktuell !== a) ausblenden(aktuell);
    aktuell = a;
    if (a.paused) {
      a.currentTime = 0;
      var p = a.play();
      if (p && p.catch) {
        p.then(function () { freigegeben = true; })
         .catch(function () { freigegeben = false; });   // wartet auf Klick
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
    }, { once: false });
  });

  function zeichneSchalter() {
    if (schalter) return;
    schalter = document.createElement('button');
    schalter.type = 'button';
    schalter.id = 'quizMusikSchalter';
    schalter.setAttribute('aria-pressed', String(cfg.an));
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
  }

  var QuizMusik = {
    /* Einstellungen ueberschreiben, z. B. andere Dateinamen oder an:false */
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

    /* Musik anhalten (Antwort geklickt, Runde vorbei, Reiter gewechselt) */
    stopp: function () {
      wunsch = null;
      ausblenden(aktuell);
      aktuell = null;
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
