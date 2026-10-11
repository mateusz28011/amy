import sys, numpy as np, amy
from amy import _amy
from scipy.io import wavfile
out = sys.argv[1]
sr, block = amy.AMY_SAMPLE_RATE, amy.AMY_BLOCK_SIZE
step_s = 60 / 145 / 4                     # 16ths at 145 BPM
gate = '0,1,55,1,15,0,0,0'                   # hold 55 ms, 15 ms release: silent before the next 16th
_amy.stop(); _amy.start(0)
amy.send(osc=0, wave=amy.PCM, preset=311, bp0=gate)
audio, hits, t = [], [], 0
for bar in range(4):
    for s in range(16):
        if s % 4 in (0, 1):               # a kick on each beat plus the 16th after it
            hits.append(t)
            amy.send(osc=0, vel=1)
        n = int(round((bar * 16 + s + 1) * step_s * sr)) - t
        n_blocks = max(1, round(n / block))
        chunk = amy.render(n_blocks * block / sr)[:, 0]
        audio.append(chunk); t += len(chunk)
a = np.concatenate(audio)
d = np.abs(np.diff(a))
print(out, 'peak %.4f maxjump %.5f' % (np.max(np.abs(a)), d.max()))
np.save(out + '.npy', a); np.save(out + '_hits.npy', np.array(hits))
wavfile.write(out + '.wav', sr, (np.clip(a * 8, -1, 1) * 32767).astype(np.int16))
