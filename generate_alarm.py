import wave, struct, math, base64, io

sr = 22050
def tone(freq, dur, amp=0.62):
    n = int(sr * dur); out = []
    edge = 0.012 * sr
    for i in range(n):
        env = min(1.0, i / edge, (n - i) / edge)
        out.append(int(amp * env * math.sin(2 * math.pi * freq * i / sr) * 32767))
    return out
def silence(dur):
    return [0] * int(sr * dur)

seq = []
for f in [880, 1175, 880, 1175]:
    seq += tone(f, 0.16) + silence(0.07)

buf = io.BytesIO()
w = wave.open(buf, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(b''.join(struct.pack('<h', s) for s in seq)); w.close()
datauri = 'data:audio/wav;base64,' + base64.b64encode(buf.getvalue()).decode()

p = '/Users/ryojikakizaki/Desktop/health/app/index.html'
html = open(p, encoding='utf-8').read()
tag = '<audio id="alarm" preload="auto" playsinline src="' + datauri + '"></audio>'
if 'id="alarm"' in html:
    print('already present')
else:
    html = html.replace('<div id="toast"></div>', '<div id="toast"></div>\n' + tag, 1)
    open(p, 'w', encoding='utf-8').write(html)
    print('injected, datauri_len=', len(datauri))
