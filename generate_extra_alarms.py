import wave, struct, math, base64, io

sr = 22050

def square(f, t):
    return 1.0 if math.sin(2 * math.pi * f * t) >= 0 else -1.0

def triangle(f, t):
    p = (t * f) % 1.0
    return 4 * abs(p - 0.5) - 1

def env(t, dur, attack=0.01, peak=0.9):
    # exponential-ish attack then decay, matching the WebAudio envelopes used in index.html
    if t < attack:
        return peak * (t / attack)
    decay_span = max(dur - attack, 0.001)
    dt = (t - attack) / decay_span
    return peak * math.exp(-4.5 * dt)

def render_notes(notes, wave_fn, total_dur):
    n = int(sr * total_dur)
    out = [0.0] * n
    for (freq, start, dur, peak) in notes:
        i0 = int(sr * start)
        ni = int(sr * dur)
        for i in range(ni):
            idx = i0 + i
            if idx >= n:
                break
            t = i / sr
            out[idx] += wave_fn(freq, t) * env(t, dur, 0.01, peak)
    # clip
    return [max(-1.0, min(1.0, s)) for s in out]

def to_wav_datauri(samples):
    buf = io.BytesIO()
    w = wave.open(buf, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b''.join(struct.pack('<h', int(s * 32767)) for s in samples))
    w.close()
    return 'data:audio/wav;base64,' + base64.b64encode(buf.getvalue()).decode()

# rapid: 6 square beeps alternating 1000/1320Hz, 0.16s apart, ~0.12s each
rapid_notes = []
for i in range(6):
    f = 1320 if i % 2 else 1000
    rapid_notes.append((f, i * 0.16, 0.11, 0.9))
rapid_uri = to_wav_datauri(render_notes(rapid_notes, square, 6 * 0.16 + 0.15))

# chime: two triangle notes
chime_notes = [(660, 0.0, 0.45, 0.9), (523, 0.26, 0.6, 0.9)]
chime_uri = to_wav_datauri(render_notes(chime_notes, triangle, 0.26 + 0.6 + 0.15))

# 8bit: 4 ascending square notes
bit_notes = []
for i, f in enumerate([523, 659, 784, 1047]):
    bit_notes.append((f, i * 0.1, 0.09, 0.85))
bit_uri = to_wav_datauri(render_notes(bit_notes, square, 3 * 0.1 + 0.15))

# cheer (PR celebration): 3 ascending triangle notes
cheer_notes = []
for i, f in enumerate([660, 880, 1175]):
    cheer_notes.append((f, i * 0.12, 0.14, 0.5))
cheer_uri = to_wav_datauri(render_notes(cheer_notes, triangle, 2 * 0.12 + 0.2))

p = '/Users/ryojikakizaki/Desktop/health/app/index.html'
html = open(p, encoding='utf-8').read()

if 'id="snd-rapid"' in html:
    print('already present')
else:
    tags = (
        '<audio id="snd-rapid" preload="auto" playsinline src="' + rapid_uri + '"></audio>\n'
        '<audio id="snd-chime" preload="auto" playsinline src="' + chime_uri + '"></audio>\n'
        '<audio id="snd-8bit" preload="auto" playsinline src="' + bit_uri + '"></audio>\n'
        '<audio id="snd-cheer" preload="auto" playsinline src="' + cheer_uri + '"></audio>'
    )
    marker = '<audio id="snd-go" src="snd-go.mp3" preload="auto" playsinline></audio>'
    assert marker in html, 'marker not found'
    html = html.replace(marker, marker + '\n' + tags, 1)
    open(p, 'w', encoding='utf-8').write(html)
    print('injected sizes:', len(rapid_uri), len(chime_uri), len(bit_uri), len(cheer_uri))
