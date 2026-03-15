#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║         MORSE CODE  ·  Terminal Interface            ║
║  Encode · Decode · Play Audio · Listen from Mic      ║
╚══════════════════════════════════════════════════════╝

Dependencies (audio only):
    pip install numpy sounddevice

Run:
    python morse_code.py
"""

import os
import sys
import shutil
import collections

# ─────────────────────────────────────────────────────────────────────────────
# ANSI colours & helpers
# ─────────────────────────────────────────────────────────────────────────────


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


USE_COLOR = _supports_color()


class C:
    """ANSI colour codes — falls back to empty strings if terminal lacks support."""

    if USE_COLOR:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        DIM = "\033[2m"
        # foreground
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        # bright foreground
        BBLACK = "\033[90m"
        BRED = "\033[91m"
        BGREEN = "\033[92m"
        BYELLOW = "\033[93m"
        BBLUE = "\033[94m"
        BMAGENTA = "\033[95m"
        BCYAN = "\033[96m"
        BWHITE = "\033[97m"
        # background
        BG_BLACK = "\033[40m"
        BG_CYAN = "\033[46m"
        BG_WHITE = "\033[47m"
    else:
        RESET = BOLD = DIM = ""
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
        BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ""
        BG_BLACK = BG_CYAN = BG_WHITE = ""


def clr(text: str, *codes: str) -> str:
    if not codes:
        return text
    return "".join(codes) + text + C.RESET


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def term_width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def hline(char: str = "─", width: int | None = None) -> str:
    return char * (width or min(term_width(), 72))


def box(lines: list[str], title: str = "", width: int | None = None) -> str:
    w = width or min(term_width() - 2, 70)
    inner = w - 2
    top = "╔" + "═" * inner + "╗"
    bottom = "╚" + "═" * inner + "╝"
    if title:
        pad = inner - len(title) - 2
        lp = pad // 2
        rp = pad - lp
        top = "╔" + "═" * lp + f" {title} " + "═" * rp + "╗"
    result = [top]
    for line in lines:
        # strip ANSI for length measurement
        import re

        visible = re.sub(r"\033\[[0-9;]*m", "", line)
        pad_needed = inner - len(visible)
        result.append("║ " + line + " " * max(pad_needed - 2, 0) + " ║")
    result.append(bottom)
    return "\n".join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Morse tables
# ─────────────────────────────────────────────────────────────────────────────

MORSE_CODE: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
    " ": "/",
}
REVERSE_MORSE: dict[str, str] = {v: k for k, v in MORSE_CODE.items()}

# ─────────────────────────────────────────────────────────────────────────────
# Core encode / decode
# ─────────────────────────────────────────────────────────────────────────────


def encode(text: str) -> str:
    if not text:
        raise ValueError("Input text must not be empty.")
    tokens = []
    for ch in text.upper():
        if ch not in MORSE_CODE:
            raise ValueError(f"Character {ch!r} is not supported.")
        tokens.append(MORSE_CODE[ch])
    return " ".join(tokens)


def decode(morse: str) -> str:
    if not morse.strip():
        raise ValueError("Input Morse code must not be empty.")
    decoded_words = []
    for word in morse.strip().split(" / "):
        chars = []
        for token in word.split():
            if token not in REVERSE_MORSE:
                raise ValueError(f"Unknown Morse sequence: {token!r}.")
            chars.append(REVERSE_MORSE[token])
        decoded_words.append("".join(chars))
    return " ".join(decoded_words)


# ─────────────────────────────────────────────────────────────────────────────
# Audio helpers
# ─────────────────────────────────────────────────────────────────────────────


def _require_audio():
    try:
        import numpy as np
        import sounddevice as sd

        return np, sd
    except ImportError:
        print(clr("\n  ⚠  Audio requires: pip install numpy sounddevice\n", C.BYELLOW))
        return None, None


def play_morse(
    morse_str: str, wpm: int = 15, frequency: int = 700, volume: float = 0.6
) -> None:
    np, sd = _require_audio()
    if np is None:
        return

    SR = 44100
    unit_s = 1.2 / wpm

    def _tone(dur_s):
        t = np.linspace(0, dur_s, int(SR * dur_s), endpoint=False)
        wave = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
        fade = min(int(SR * 0.005), len(wave) // 2)
        wave[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)
        wave[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
        return wave

    def _sil(dur_s):
        return np.zeros(int(SR * dur_s), dtype=np.float32)

    tokens = morse_str.strip().split()
    chunks = []
    for i, tok in enumerate(tokens):
        if tok == "/":
            chunks.append(_sil(4 * unit_s))
            continue
        for j, sym in enumerate(tok):
            chunks.append(_tone(unit_s) if sym == "." else _tone(3 * unit_s))
            if j < len(tok) - 1:
                chunks.append(_sil(unit_s))
        if i < len(tokens) - 1 and tokens[i + 1] != "/":
            chunks.append(_sil(3 * unit_s))

    if not chunks:
        return

    audio = np.concatenate(chunks)
    total_s = len(audio) / SR
    print(
        clr(f"\n  ♪  Playing at {wpm} WPM · {frequency} Hz · {total_s:.1f}s …", C.BCYAN)
    )
    sd.play(audio, samplerate=SR)
    sd.wait()
    print(clr("  ♪  Playback complete.\n", C.BCYAN))


class MorseListener:
    def __init__(self, wpm=15, threshold=0.02, sample_rate=44100, frame_size=512):
        self.np, self.sd = _require_audio()
        self.SR = sample_rate
        self.frame_size = frame_size
        self.threshold = threshold
        self._running = False

        unit_s = 1.2 / wpm
        self.dot_max = unit_s * 2.0
        self.char_gap = unit_s * 2.0
        self.word_gap = unit_s * 5.0

    def _rms(self, frame):
        return float(self.np.sqrt(self.np.mean(frame.astype(self.np.float64) ** 2)))

    def _timings_to_morse(self, timings):
        tokens, letter = [], []
        for is_tone, dur in timings:
            if is_tone:
                letter.append("." if dur <= self.dot_max else "-")
            else:
                if dur >= self.word_gap:
                    if letter:
                        tokens.append("".join(letter))
                        letter = []
                    tokens.append("/")
                elif dur >= self.char_gap:
                    if letter:
                        tokens.append("".join(letter))
                        letter = []
        if letter:
            tokens.append("".join(letter))
        return " ".join(tokens)

    def listen(self, duration_s=10.0):
        if self.np is None:
            return None, None

        frames_needed = int(self.SR * duration_s) // self.frame_size
        frame_time = self.frame_size / self.SR
        was_tone, seg_start, timings = False, 0.0, []
        self._running = True

        print(
            clr(
                f"\n  🎙  Listening for {duration_s:.0f}s …  (Ctrl-C to stop early)\n",
                C.BMAGENTA,
            )
        )
        print(
            clr(
                "  Tip: use a tone-generator app on your phone held near the mic,",
                C.DIM,
            )
        )
        print(clr("       or tap/knock rhythmically for manual keying.\n", C.DIM))

        try:
            with self.sd.InputStream(
                samplerate=self.SR,
                channels=1,
                dtype="float32",
                blocksize=self.frame_size,
            ) as stream:
                for f in range(frames_needed):
                    if not self._running:
                        break
                    frame, _ = stream.read(self.frame_size)
                    now = f * frame_time
                    is_on = self._rms(frame) > self.threshold
                    if is_on != was_tone:
                        dur = now - seg_start
                        if dur > 0.015:
                            timings.append((was_tone, dur))
                        seg_start = now
                        was_tone = is_on
        except KeyboardInterrupt:
            pass

        self._running = False
        seg_dur = frames_needed * frame_time - seg_start
        if seg_dur > 0.015:
            timings.append((was_tone, seg_dur))

        ms = self._timings_to_morse(timings)
        if not ms:
            return None, None
        try:
            text = decode(ms)
        except ValueError:
            text = f"(noisy/partial — raw morse: {ms})"
        return ms, text


# ─────────────────────────────────────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────────────────────────────────────

BANNER_LINES = [
    r"  ███╗   ███╗ ██████╗ ██████╗ ███████╗███████╗",
    r"  ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██╔════╝",
    r"  ██╔████╔██║██║   ██║██████╔╝███████╗█████╗  ",
    r"  ██║╚██╔╝██║██║   ██║██╔══██╗╚════██║██╔══╝  ",
    r"  ██║ ╚═╝ ██║╚██████╔╝██║  ██║███████║███████╗",
    r"  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝",
    r"",
    r"   ·  ─  ·  ─     C O D E     ·  ─  ·  ─  ·  ",
]

MENU_ITEMS = [
    ("1", "🔤", "Encode", "Type text  →  get Morse code"),
    ("2", "📡", "Decode", "Type Morse →  get plain text"),
    ("3", "🔊", "Play", "Type text  →  hear Morse audio"),
    ("4", "🎙", "Listen", "Speak/tap into mic  →  decode"),
    ("5", "📖", "Reference", "Show full Morse code table"),
    ("Q", "🚪", "Quit", "Exit the program"),
]


def print_banner():
    w = min(term_width(), 72)
    print()
    for line in BANNER_LINES:
        print(clr(line.center(w), C.BCYAN, C.BOLD))
    print()


def print_menu():
    w = min(term_width() - 4, 68)
    print(clr("  " + hline("═", w), C.BBLACK))
    print(clr("   MAIN MENU", C.BYELLOW, C.BOLD))
    print(clr("  " + hline("─", w), C.BBLACK))
    for key, icon, label, desc in MENU_ITEMS:
        k = clr(f" {key} ", C.BG_BLACK, C.BYELLOW, C.BOLD)
        ico = icon
        lbl = clr(f"{label:<10}", C.BWHITE, C.BOLD)
        dsc = clr(desc, C.DIM)
        print(f"  {k}  {ico}  {lbl}  {dsc}")
    print(clr("  " + hline("═", w), C.BBLACK))
    print()


def section_header(title: str, icon: str = ""):
    w = min(term_width() - 4, 68)
    print()
    print(clr("  " + hline("─", w), C.BBLACK))
    print(clr(f"  {icon}  {title}", C.BYELLOW, C.BOLD))
    print(clr("  " + hline("─", w), C.BBLACK))
    print()


def ok(label: str, value: str):
    print(clr(f"  ✔  {label}: ", C.BGREEN, C.BOLD) + clr(value, C.BWHITE))


def err(msg: str):
    print(clr(f"  ✘  {msg}", C.BRED, C.BOLD))


def ask(prompt: str, default: str = "") -> str:
    hint = clr(f"  (default: {default})", C.DIM) if default else ""
    arrow = clr("  › ", C.BCYAN, C.BOLD)
    if default:
        print(f"  {clr(prompt, C.WHITE)}{hint}")
    else:
        print(f"  {clr(prompt, C.WHITE)}")
    raw = input(arrow).strip()
    return raw if raw else default


def pause():
    print()
    input(clr("  Press Enter to return to the menu …", C.DIM))


# ─────────────────────────────────────────────────────────────────────────────
# Reference table
# ─────────────────────────────────────────────────────────────────────────────


def show_reference():
    section_header("Morse Code Reference Table", "📖")
    items = [(k, v) for k, v in MORSE_CODE.items() if k != " "]
    cols = 5
    col_w = 14
    for i, (ch, code) in enumerate(items):
        char_str = clr(f"{ch}", C.BYELLOW, C.BOLD)
        code_str = clr(f"{code}", C.BCYAN)
        cell = f"  {char_str} {code_str:<8}"
        print(cell, end="\n" if (i + 1) % cols == 0 else "")
    print()
    print(clr("  (Space character encodes as  /  word separator)", C.DIM))
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Menu screens
# ─────────────────────────────────────────────────────────────────────────────


def screen_encode():
    section_header("Encode Text → Morse Code", "🔤")
    text = ask("Enter the text to encode")
    if not text:
        err("Nothing entered.")
        pause()
        return
    try:
        result = encode(text)
        print()
        ok("Input ", text)
        ok("Morse ", clr(result, C.BCYAN))
        print()
        # Pretty visual: replace . and - with coloured symbols
        visual = result.replace(".", clr("·", C.BYELLOW)).replace(
            "-", clr("━", C.BBLUE)
        )
        print(clr("  Visual: ", C.DIM) + visual)
    except ValueError as e:
        err(str(e))
    pause()


def screen_decode():
    section_header("Decode Morse Code → Text", "📡")
    print(clr("  Format: letters separated by spaces, words by  /", C.DIM))
    print(clr("  Example:  .... . .-.. .-.. --- / .-- --- .-. .-.. -..", C.DIM))
    print()
    morse = ask("Enter Morse code")
    if not morse:
        err("Nothing entered.")
        pause()
        return
    try:
        result = decode(morse)
        print()
        ok("Morse", morse)
        ok("Text ", clr(result, C.BGREEN, C.BOLD))
    except ValueError as e:
        err(str(e))
    pause()


def screen_play():
    section_header("Play Morse Code as Audio", "🔊")
    text = ask("Enter text to play as Morse audio")
    if not text:
        err("Nothing entered.")
        pause()
        return
    try:
        morse_str = encode(text)
        ok("Morse", clr(morse_str, C.BCYAN))
        print()
        wpm = int(ask("Words per minute (WPM)", "15"))
        freq = int(ask("Tone frequency in Hz  ", "700"))
        play_morse(morse_str, wpm=wpm, frequency=freq)
    except ValueError as e:
        err(str(e))
    pause()


def screen_listen():
    section_header("Listen & Decode Morse from Microphone", "🎙")
    print(clr("  The app will record your microphone and decode Morse tones.", C.DIM))
    print(clr("  Use a tone-generator app, buzzer, or tap loudly near the mic.", C.DIM))
    print()
    duration = float(ask("Recording duration (seconds)", "10"))
    wpm = int(ask("Expected sending speed (WPM) ", "15"))
    threshold = float(ask("Amplitude threshold 0.0–1.0  ", "0.02"))
    print()

    listener = MorseListener(wpm=wpm, threshold=threshold)
    ms, text = listener.listen(duration_s=duration)

    if ms:
        ok("Morse detected", clr(ms, C.BCYAN))
        ok("Decoded text  ", clr(text, C.BGREEN, C.BOLD))
    else:
        print()
        err("No Morse signal detected.")
        print(clr("  Suggestions:", C.DIM))
        print(clr("    • Lower the threshold (try 0.005 or 0.001)", C.DIM))
        print(clr("    • Make sure your microphone is enabled", C.DIM))
        print(clr("    • Increase the volume of your tone source", C.DIM))
    pause()


# ─────────────────────────────────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────────────────────────────────

DISPATCH = {
    "1": screen_encode,
    "2": screen_decode,
    "3": screen_play,
    "4": screen_listen,
    "5": show_reference,
}


def run():
    clear_screen()
    print_banner()
    print_menu()

    while True:
        try:
            choice = (
                input(clr("  Choose an option › ", C.BYELLOW, C.BOLD)).strip().lower()
            )
        except (EOFError, KeyboardInterrupt):
            choice = "q"

        if choice in ("q", "quit", "exit"):
            print()
            print(clr("  Farewell!  ", C.BCYAN) + clr(".-.. --- ...", C.DIM))
            print()
            break

        if choice in DISPATCH:
            clear_screen()
            DISPATCH[choice]()
            clear_screen()
            print_banner()
            print_menu()
        else:
            print(clr("  Please enter 1–5 or Q.\n", C.BRED))


# ─────────────────────────────────────────────────────────────────────────────
# CLI passthrough (optional non-interactive use)
# ─────────────────────────────────────────────────────────────────────────────


def cli():
    args = sys.argv[1:]
    cmd = args[0].lower() if args else ""

    if cmd in ("encode", "e") and len(args) >= 2:
        print(encode(" ".join(args[1:])))
    elif cmd in ("decode", "d") and len(args) >= 2:
        print(decode(" ".join(args[1:])))
    elif cmd in ("play", "p") and len(args) >= 2:
        ms = encode(" ".join(args[1:]))
        print(f"Morse: {ms}")
        play_morse(ms)
    elif cmd in ("listen", "l"):
        dur = float(args[1]) if len(args) >= 2 else 10.0
        ms, text = MorseListener().listen(duration_s=dur)
        if ms:
            print(f"Morse : {ms}\nText  : {text}")
        else:
            print("No signal detected.")
    else:
        run()


if __name__ == "__main__":
    cli()
