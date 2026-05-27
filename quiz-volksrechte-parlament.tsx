import { useState } from "react";
import { Check, X, RotateCcw, Trophy, Repeat, Coins } from "lucide-react";

const QUESTIONS = [
  {
    frage: "Wie viele gültige Unterschriften braucht eine Volksinitiative – und in welcher Frist?",
    optionen: [
      "50'000 Unterschriften innert 100 Tagen",
      "100'000 Unterschriften innert 18 Monaten",
      "100'000 Unterschriften innert 100 Tagen",
      "50'000 Unterschriften innert 18 Monaten",
    ],
    richtig: 1,
    erklaerung:
      "Für eine Volksinitiative müssen 100'000 gültige Unterschriften innerhalb von 18 Monaten gesammelt werden.",
  },
  {
    frage: "Wie viele Unterschriften braucht das fakultative Referendum – und in welcher Frist?",
    optionen: [
      "50'000 Unterschriften innert 100 Tagen",
      "100'000 Unterschriften innert 18 Monaten",
      "50'000 Unterschriften innert 18 Monaten",
      "30'000 Unterschriften innert 90 Tagen",
    ],
    richtig: 0,
    erklaerung:
      "Beim fakultativen Referendum müssen 50'000 Unterschriften innerhalb von 100 Tagen gegen ein neues Bundesgesetz gesammelt werden.",
  },
  {
    frage: "Das obligatorische Referendum muss durch eine Unterschriftensammlung ausgelöst werden.",
    typ: "wf",
    richtig: 1,
    erklaerung:
      "Falsch. Das obligatorische Referendum kommt automatisch – ohne Unterschriftensammlung. Es ist bei bestimmten Beschlüssen wie Verfassungsänderungen zwingend.",
  },
  {
    frage: "Welches Mehr braucht eine Volksinitiative zur Annahme?",
    optionen: [
      "Nur das einfache Volksmehr",
      "Nur das Ständemehr",
      "Das doppelte Mehr (Volksmehr UND Ständemehr)",
      "Eine Zweidrittelmehrheit im Parlament",
    ],
    richtig: 2,
    erklaerung:
      "Eine Volksinitiative ändert die Bundesverfassung. Darum braucht sie das doppelte Mehr: die Mehrheit der Abstimmenden (Volksmehr) UND die Mehrheit der Kantone (Ständemehr).",
  },
  {
    frage: "Welches Mehr genügt beim fakultativen Referendum zur Annahme bzw. Ablehnung der Vorlage?",
    optionen: [
      "Das einfache Volksmehr",
      "Das doppelte Mehr",
      "Nur das Ständemehr",
      "Eine Dreiviertelmehrheit",
    ],
    richtig: 0,
    erklaerung:
      "Beim fakultativen Referendum genügt das einfache Volksmehr – also die Mehrheit der Abstimmenden. Ein Ständemehr ist nicht nötig.",
  },
  {
    frage: "Wie viele Mitglieder hat der Nationalrat?",
    optionen: ["46 Mitglieder", "100 Mitglieder", "200 Mitglieder", "246 Mitglieder"],
    richtig: 2,
    erklaerung:
      "Der Nationalrat – die «grosse Kammer» – hat 200 Mitglieder. Er vertritt das Volk; grosse Kantone haben mehr Sitze.",
  },
  {
    frage: "Wie viele Mitglieder hat der Ständerat?",
    optionen: ["26 Mitglieder", "46 Mitglieder", "100 Mitglieder", "200 Mitglieder"],
    richtig: 1,
    erklaerung:
      "Der Ständerat – die «kleine Kammer» – hat 46 Mitglieder: je 2 pro Vollkanton, je 1 pro Halbkanton.",
  },
  {
    frage: "Wen vertritt der Ständerat?",
    optionen: [
      "Das gesamte Schweizer Volk",
      "Die Kantone",
      "Die politischen Parteien",
      "Die Berufsverbände",
    ],
    richtig: 1,
    erklaerung:
      "Der Ständerat vertritt die Kantone. Der Nationalrat hingegen vertritt das Volk.",
  },
  {
    frage: "Nationalrat und Ständerat zusammen bilden die Bundesversammlung.",
    typ: "wf",
    richtig: 0,
    erklaerung:
      "Richtig. Nationalrat (200) und Ständerat (46) bilden zusammen die Bundesversammlung – das Parlament der Schweiz.",
  },
  {
    frage: "Zu welcher Staatsgewalt gehört die Bundesversammlung?",
    optionen: [
      "Exekutive (Vollziehung)",
      "Judikative (Rechtsprechung)",
      "Legislative (Gesetzgebung)",
      "Sie gehört zu keiner Staatsgewalt",
    ],
    richtig: 2,
    erklaerung:
      "Die Bundesversammlung ist die Legislative: Sie erlässt Gesetze, beschliesst das Budget und wählt die Regierung. Die Exekutive ist der Bundesrat, die Judikative das Bundesgericht.",
  },
  {
    frage: "Bei welchem Beschluss kommt zwingend ein obligatorisches Referendum?",
    optionen: [
      "Bei jedem neuen Bundesgesetz",
      "Bei einer Änderung der Bundesverfassung",
      "Bei jeder Erhöhung der Mehrwertsteuer um 0,1 %",
      "Bei der Wahl des Bundesrats",
    ],
    richtig: 1,
    erklaerung:
      "Verfassungsänderungen müssen immer automatisch vors Volk – mit doppeltem Mehr. Das ist das obligatorische Referendum.",
  },
  {
    frage: "Wie oft werden Nationalrat und Ständerat gewählt?",
    optionen: ["Jedes Jahr", "Alle 2 Jahre", "Alle 4 Jahre", "Alle 8 Jahre"],
    richtig: 2,
    erklaerung:
      "Nationalrat und Ständerat werden alle 4 Jahre gewählt. Stimmberechtigt ist, wer 18 Jahre alt ist und das Schweizer Bürgerrecht besitzt.",
  },
];

const WF_LABELS = ["Wahr", "Falsch"];

// Gewinnstufen: Frage 1 (unten) bis Frage 12 (oben)
const BETRAG = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 500000, 1000000];
const GESAMT = BETRAG.reduce((a, b) => a + b, 0);
const chf = (n) => n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "'");

const POLY = "polygon(0 50%, 22px 0, calc(100% - 22px) 0, 100% 50%, calc(100% - 22px) 100%, 22px 100%)";
const SMALLPOLY = "polygon(0 50%, 9px 0, calc(100% - 9px) 0, 100% 50%, calc(100% - 9px) 100%, 9px 100%)";

const FILL = {
  default: "linear-gradient(180deg,#1a3c86 0%,#0d2356 52%,#081640 100%)",
  correct: "linear-gradient(180deg,#23ad59 0%,#118040 52%,#0a5c2b 100%)",
  wrong: "linear-gradient(180deg,#e23a37 0%,#bb1d1d 52%,#7e1b1b 100%)",
};
const BORDER = {
  default: "linear-gradient(180deg,#8fb3f7,#27429a)",
  correct: "linear-gradient(180deg,#69f0a6,#0a5c2b)",
  wrong: "linear-gradient(180deg,#ffb0b0,#7e1b1b)",
};

function AnswerButton({ letter, text, onClick, disabled, state, removed }) {
  if (removed) {
    return (
      <div
        className="relative w-full"
        style={{ clipPath: POLY, background: BORDER.default, padding: "2.5px", opacity: 0.16 }}
      >
        <div
          className="flex items-center"
          style={{
            clipPath: POLY,
            background: FILL.default,
            minHeight: "58px",
            paddingLeft: "30px",
            paddingRight: "26px",
          }}
        >
          <span className="font-extrabold text-base" style={{ color: "#f4ad33" }}>
            {letter}
          </span>
        </div>
      </div>
    );
  }

  const fill = state === "correct" ? FILL.correct : state === "wrong" ? FILL.wrong : FILL.default;
  const border = state === "correct" ? BORDER.correct : state === "wrong" ? BORDER.wrong : BORDER.default;
  const letterColor = state === "correct" || state === "wrong" ? "#ffffff" : "#f4ad33";
  const glow =
    state === "correct"
      ? "drop-shadow(0 0 9px rgba(52,211,153,.75))"
      : state === "wrong"
      ? "drop-shadow(0 0 9px rgba(248,113,113,.7))"
      : "drop-shadow(0 2px 4px rgba(0,0,0,.45))";

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`relative w-full transition ${
        disabled ? "cursor-default" : "cursor-pointer hover:brightness-125"
      }`}
      style={{
        clipPath: POLY,
        background: border,
        padding: "2.5px",
        filter: glow,
        opacity: state === "dim" ? 0.32 : 1,
      }}
    >
      <div
        className="flex items-center"
        style={{
          clipPath: POLY,
          background: fill,
          minHeight: "58px",
          paddingLeft: "30px",
          paddingRight: "26px",
        }}
      >
        <span className="font-extrabold text-base mr-3 flex-shrink-0" style={{ color: letterColor }}>
          {letter}
        </span>
        <span className="text-left text-[13.5px] sm:text-[15px] font-semibold text-white leading-tight py-2">
          {text}
        </span>
        {state === "correct" && <Check className="ml-auto w-5 h-5 text-white flex-shrink-0" strokeWidth={3} />}
        {state === "wrong" && <X className="ml-auto w-5 h-5 text-white flex-shrink-0" strokeWidth={3} />}
      </div>
    </button>
  );
}

export default function Quiz() {
  const [runde, setRunde] = useState(QUESTIONS.map((_, i) => i));
  const [pos, setPos] = useState(0);
  const [selected, setSelected] = useState(null);
  const [beantwortet, setBeantwortet] = useState(false);
  const [falsche, setFalsche] = useState([]);
  const [rundeNr, setRundeNr] = useState(1);
  const [erstePunkte, setErstePunkte] = useState(0);
  const [phase, setPhase] = useState("quiz");
  const [status, setStatus] = useState(QUESTIONS.map(() => null));
  const [jokerVerfuegbar, setJokerVerfuegbar] = useState(true);
  const [entfernt, setEntfernt] = useState([]);

  const fIndex = runde[pos];
  const frage = QUESTIONS[fIndex];
  const optionen = frage.typ === "wf" ? WF_LABELS : frage.optionen;
  const istWF = frage.typ === "wf";
  const istLetzte = pos === runde.length - 1;
  const istWiederholung = rundeNr > 1;
  const gewonnen = status.reduce((sum, s, qi) => (s === "richtig" ? sum + BETRAG[qi] : sum), 0);

  const jokerNutzbar = jokerVerfuegbar && !beantwortet && !istWF && entfernt.length === 0;
  const jokerStatus = !jokerVerfuegbar ? "used" : jokerNutzbar ? "ready" : "off";

  const waehlen = (i) => {
    if (beantwortet || entfernt.includes(i)) return;
    setSelected(i);
    setBeantwortet(true);
    setStatus((st) => {
      const next = [...st];
      next[fIndex] = i === frage.richtig ? "richtig" : "falsch";
      return next;
    });
    if (i !== frage.richtig) {
      setFalsche((arr) => (arr.includes(fIndex) ? arr : [...arr, fIndex]));
    }
  };

  const jokerNutzen = () => {
    if (!jokerNutzbar) return;
    const falscheOpt = optionen.map((_, i) => i).filter((i) => i !== frage.richtig);
    const mix = [...falscheOpt].sort(() => Math.random() - 0.5).slice(0, 2);
    setEntfernt(mix);
    setJokerVerfuegbar(false);
  };

  const weiter = () => {
    if (!istLetzte) {
      setPos((x) => x + 1);
      setSelected(null);
      setBeantwortet(false);
      setEntfernt([]);
      return;
    }
    if (rundeNr === 1) setErstePunkte(QUESTIONS.length - falsche.length);
    setPhase(falsche.length === 0 ? "fertig" : "rundenende");
  };

  const wiederholungStarten = () => {
    setRunde(falsche);
    setFalsche([]);
    setPos(0);
    setSelected(null);
    setBeantwortet(false);
    setEntfernt([]);
    setRundeNr((n) => n + 1);
    setPhase("quiz");
  };

  const neustart = () => {
    setRunde(QUESTIONS.map((_, i) => i));
    setFalsche([]);
    setPos(0);
    setSelected(null);
    setBeantwortet(false);
    setRundeNr(1);
    setErstePunkte(0);
    setStatus(QUESTIONS.map(() => null));
    setJokerVerfuegbar(true);
    setEntfernt([]);
    setPhase("quiz");
  };

  const note = (() => {
    const q = erstePunkte / QUESTIONS.length;
    if (q >= 0.9) return "Hervorragend – fast alles auf Anhieb!";
    if (q >= 0.7) return "Stark gespielt – die Wiederholung hat den Rest gefestigt.";
    if (q >= 0.5) return "Geschafft – die Wiederholungsrunden haben geholfen.";
    return "Durchgekämpft – jetzt sitzt jede Frage.";
  })();

  const rungColor = (qi) => {
    if (phase === "quiz" && qi === fIndex) return "current";
    if (status[qi] === "richtig") return "richtig";
    if (status[qi] === "falsch") return "falsch";
    return "leer";
  };
  const RUNG_BG = {
    current: "linear-gradient(180deg,#f6b13c,#d98512)",
    richtig: "linear-gradient(180deg,#1f9d51,#0c5d2c)",
    falsch: "linear-gradient(180deg,#c4302d,#7c1b1b)",
    leer: "linear-gradient(180deg,#173061,#0c1d44)",
  };

  // Joker-Pille
  const jokerStyle = {
    ready: {
      background: "linear-gradient(180deg,#1a3c86,#0c1f4c)",
      border: "2px solid #f4ad33",
      color: "#f4ad33",
      filter: "drop-shadow(0 0 5px rgba(246,177,60,.55))",
    },
    used: {
      background: "linear-gradient(180deg,#1a2540,#0c1326)",
      border: "2px solid #475569",
      color: "#64748b",
    },
    off: {
      background: "linear-gradient(180deg,#15295c,#0a1838)",
      border: "2px solid rgba(244,173,51,.3)",
      color: "rgba(244,173,51,.45)",
    },
  };

  const MoneyBar = () => (
    <div className="flex justify-center mb-3">
      <div
        className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full"
        style={{
          background: "linear-gradient(180deg,#1a3c86,#0c1f4c)",
          border: "1.5px solid rgba(244,173,51,.6)",
        }}
      >
        <Coins className="w-4 h-4 text-amber-300" />
        <span className="text-[11px] font-semibold text-blue-200 uppercase tracking-wider">
          Gewonnen
        </span>
        <span
          className="text-base font-extrabold text-amber-300"
          style={{ textShadow: "0 0 8px rgba(246,177,60,.5)" }}
        >
          CHF {chf(gewonnen)}
        </span>
      </div>
    </div>
  );

  return (
    <div
      className="min-h-screen p-3 sm:p-5 font-sans"
      style={{
        background: "radial-gradient(ellipse at 50% 22%, #1f3f86 0%, #0c1f4c 46%, #050b1d 100%)",
      }}
    >
      <div className="max-w-3xl mx-auto">
        {/* Titel */}
        <div className="text-center mb-4">
          <div className="text-[11px] font-bold tracking-[0.25em] text-amber-300/80 uppercase">
            HKV Aarau · ABU
          </div>
          <h1
            className="text-xl sm:text-2xl font-extrabold mt-1 text-white"
            style={{ textShadow: "0 0 14px rgba(246,177,60,.55)" }}
          >
            Volksrechte &amp; Parlament
          </h1>
        </div>

        {(phase === "quiz" || phase === "rundenende") && <MoneyBar />}

        {/* mobile Fortschritt */}
        <div className="md:hidden mb-3 flex flex-wrap justify-center gap-1.5">
          {QUESTIONS.map((_, qi) => {
            const c = rungColor(qi);
            return (
              <div
                key={qi}
                className="w-6 h-6 flex items-center justify-center text-[10px] font-bold text-white"
                style={{
                  clipPath: SMALLPOLY,
                  background: RUNG_BG[c],
                  filter: c === "current" ? "drop-shadow(0 0 5px rgba(246,177,60,.9))" : "none",
                }}
              >
                {qi + 1}
              </div>
            );
          })}
        </div>

        <div className="flex gap-4">
          {/* Hauptbereich */}
          <div className="flex-1 min-w-0">
            {phase === "quiz" && (
              <>
                <div className="flex items-center justify-between mb-2 px-1 gap-2">
                  <span className="text-xs font-semibold text-blue-200">
                    {istWiederholung ? (
                      <span className="inline-flex items-center gap-1 text-amber-300">
                        <Repeat className="w-3.5 h-3.5" />
                        Wiederholung · Runde {rundeNr}
                      </span>
                    ) : (
                      <>Frage {pos + 1} von {runde.length}</>
                    )}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="hidden sm:inline text-[11px] font-bold text-amber-300 whitespace-nowrap">
                      Stufe CHF {chf(BETRAG[fIndex])}
                    </span>
                    <button
                      onClick={jokerNutzen}
                      disabled={!jokerNutzbar}
                      title={
                        jokerStatus === "used"
                          ? "Joker bereits verwendet"
                          : jokerStatus === "off"
                          ? istWF
                            ? "Beim Wahr/Falsch nicht nötig"
                            : "Erst bei der nächsten offenen Frage"
                          : "Zwei falsche Antworten entfernen"
                      }
                      className={`text-xs font-extrabold px-3 py-1 rounded-full transition ${
                        jokerStatus === "ready"
                          ? "cursor-pointer hover:brightness-125"
                          : "cursor-default"
                      }`}
                      style={jokerStyle[jokerStatus]}
                    >
                      <span className={jokerStatus === "used" ? "line-through" : ""}>
                        50 : 50
                      </span>
                    </button>
                  </div>
                </div>

                {/* Frage-Lozenge */}
                <div
                  style={{
                    clipPath: POLY,
                    background: "linear-gradient(180deg,#9fc0fb,#2a47a0)",
                    padding: "2.5px",
                    filter: "drop-shadow(0 3px 8px rgba(0,0,0,.5))",
                  }}
                >
                  <div
                    className="flex items-center justify-center text-center"
                    style={{
                      clipPath: POLY,
                      background: "linear-gradient(180deg,#11295f 0%,#0a1c46 100%)",
                      minHeight: "92px",
                      padding: "14px 34px",
                    }}
                  >
                    <p className="text-[14px] sm:text-base font-bold text-white leading-snug">
                      {frage.frage}
                    </p>
                  </div>
                </div>

                {/* Antworten */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 mt-3">
                  {optionen.map((opt, i) => {
                    const istEntfernt = entfernt.includes(i);
                    let state = "idle";
                    if (beantwortet) {
                      if (i === frage.richtig) state = "correct";
                      else if (i === selected) state = "wrong";
                      else state = "dim";
                    }
                    return (
                      <AnswerButton
                        key={i}
                        letter={String.fromCharCode(65 + i)}
                        text={opt}
                        state={state}
                        removed={istEntfernt}
                        disabled={beantwortet || istEntfernt}
                        onClick={() => waehlen(i)}
                      />
                    );
                  })}
                </div>

                {/* Rückmeldung */}
                {beantwortet && (
                  <div
                    className="mt-3 rounded-lg px-4 py-3 border"
                    style={{
                      background:
                        selected === frage.richtig ? "rgba(16,122,64,.22)" : "rgba(180,40,40,.22)",
                      borderColor: selected === frage.richtig ? "#34d39966" : "#f8717166",
                    }}
                  >
                    <p
                      className="text-sm font-bold"
                      style={{ color: selected === frage.richtig ? "#6ee7a8" : "#fca5a5" }}
                    >
                      {selected === frage.richtig
                        ? `Richtig! +CHF ${chf(BETRAG[fIndex])}`
                        : "Leider falsch – diese Frage kommt später nochmals."}
                    </p>
                    <p className="text-[13px] text-blue-100/90 mt-1 leading-relaxed">
                      {frage.erklaerung}
                    </p>
                  </div>
                )}

                {beantwortet && (
                  <button
                    onClick={weiter}
                    className="mt-3 w-full font-bold py-3 rounded-lg text-[#1a1100] transition hover:brightness-110"
                    style={{ background: "linear-gradient(180deg,#f7c14e,#e0921a)" }}
                  >
                    {istLetzte
                      ? falsche.length === 0
                        ? "Auswertung anzeigen"
                        : "Runde abschliessen"
                      : "Nächste Frage"}
                  </button>
                )}
              </>
            )}

            {phase === "rundenende" && (
              <div
                className="rounded-xl px-5 py-7 text-center border border-amber-400/30"
                style={{ background: "linear-gradient(180deg,#11295f,#0a1c46)" }}
              >
                <div
                  className="w-14 h-14 mx-auto rounded-full flex items-center justify-center"
                  style={{ background: "linear-gradient(180deg,#f6b13c,#d98512)" }}
                >
                  <Repeat className="w-7 h-7 text-[#1a1100]" />
                </div>
                <h2 className="text-lg font-extrabold text-white mt-3">
                  {falsche.length === 1 ? "Noch 1 Frage offen" : `Noch ${falsche.length} Fragen offen`}
                </h2>
                <p className="text-[13px] text-blue-200 mt-1">
                  Diese Fragen waren noch nicht richtig. Sie kommen jetzt nochmals – bis alle sitzen.
                </p>
                <div className="mt-4 space-y-2 text-left">
                  {falsche.map((fi) => (
                    <div
                      key={fi}
                      className="rounded-md px-3 py-2 text-[13px] text-blue-50 border border-amber-400/25 flex justify-between gap-3"
                      style={{ background: "rgba(246,177,60,.12)" }}
                    >
                      <span>{QUESTIONS[fi].frage}</span>
                      <span className="text-amber-300 font-bold whitespace-nowrap">
                        CHF {chf(BETRAG[fi])}
                      </span>
                    </div>
                  ))}
                </div>
                <button
                  onClick={wiederholungStarten}
                  className="mt-5 w-full font-bold py-3 rounded-lg text-[#1a1100] transition hover:brightness-110"
                  style={{ background: "linear-gradient(180deg,#f7c14e,#e0921a)" }}
                >
                  Wiederholungsrunde starten
                </button>
              </div>
            )}

            {phase === "fertig" && (
              <div
                className="rounded-xl px-5 py-8 text-center border border-amber-400/40"
                style={{ background: "linear-gradient(180deg,#13306c,#0a1c46)" }}
              >
                <div
                  className="w-16 h-16 mx-auto rounded-full flex items-center justify-center"
                  style={{
                    background: "linear-gradient(180deg,#f7c64e,#dd9018)",
                    filter: "drop-shadow(0 0 16px rgba(246,177,60,.7))",
                  }}
                >
                  <Trophy className="w-9 h-9 text-[#1a1100]" />
                </div>
                <h2
                  className="text-2xl font-extrabold text-amber-300 mt-3"
                  style={{ textShadow: "0 0 14px rgba(246,177,60,.6)" }}
                >
                  Gewonnen!
                </h2>
                <p className="text-[13px] text-blue-100 mt-1">
                  Alle 12 Fragen richtig beantwortet. {note}
                </p>

                <div
                  className="mt-5 rounded-lg py-5 border border-amber-300/30"
                  style={{ background: "rgba(246,177,60,.1)" }}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Coins className="w-6 h-6 text-amber-300" />
                    <span
                      className="text-3xl font-extrabold text-amber-300"
                      style={{ textShadow: "0 0 12px rgba(246,177,60,.6)" }}
                    >
                      CHF {chf(GESAMT)}
                    </span>
                  </div>
                  <div className="text-xs text-blue-200 mt-1">Gesamtgewinn</div>
                  <div className="text-[11px] text-blue-300/70 mt-3 border-t border-blue-300/15 pt-2">
                    {erstePunkte} / {QUESTIONS.length} richtig im ersten Anlauf ·{" "}
                    {rundeNr === 1 ? "ohne Wiederholung" : `${rundeNr} Durchgänge gespielt`}
                  </div>
                </div>

                <button
                  onClick={neustart}
                  className="mt-5 w-full font-bold py-3 rounded-lg text-[#1a1100] transition hover:brightness-110 flex items-center justify-center gap-2"
                  style={{ background: "linear-gradient(180deg,#f7c14e,#e0921a)" }}
                >
                  <RotateCcw className="w-4 h-4" />
                  Neue Runde spielen
                </button>
              </div>
            )}
          </div>

          {/* Gewinnstufen-Leiter (Desktop) */}
          <div className="hidden md:block w-36 flex-shrink-0">
            <div className="text-[10px] font-bold tracking-widest text-amber-300/80 uppercase text-center mb-2">
              Gewinnstufen
            </div>
            <div className="space-y-1">
              {Array.from({ length: 12 }).map((_, k) => {
                const qi = 11 - k;
                const c = rungColor(qi);
                const milestone = qi === 3 || qi === 7 || qi === 11;
                return (
                  <div
                    key={qi}
                    style={{
                      clipPath: SMALLPOLY,
                      background: RUNG_BG[c],
                      padding: "1.5px",
                      filter: c === "current" ? "drop-shadow(0 0 6px rgba(246,177,60,.9))" : "none",
                    }}
                  >
                    <div
                      className="flex items-center justify-between px-3 py-1"
                      style={{
                        clipPath: SMALLPOLY,
                        background:
                          c === "leer" ? "linear-gradient(180deg,#0e2152,#081639)" : "transparent",
                      }}
                    >
                      <span
                        className={`text-[11px] ${milestone ? "font-extrabold" : "font-semibold"}`}
                        style={{
                          color:
                            c === "leer"
                              ? milestone
                                ? "#f4ad33"
                                : "#7f9fd6"
                              : c === "current"
                              ? "#1a1100"
                              : "#ffffff",
                        }}
                      >
                        {chf(BETRAG[qi])}
                      </span>
                      {c === "richtig" && <Check className="w-3 h-3 text-white" strokeWidth={3.5} />}
                      {c === "falsch" && <X className="w-3 h-3 text-white" strokeWidth={3.5} />}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <p className="text-center text-[11px] text-blue-300/50 mt-4">
          ABU · Allgemeinbildender Unterricht · HKV Aarau
        </p>
      </div>
    </div>
  );
}
