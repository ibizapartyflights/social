"""Monta el reel a partir de tools/reel_motion.js: python3 tools/reel_build.py framesdir out.mp4 [musica.wav]
Cada capa de texto entra con fundido + deslizamiento (sin zoom). Escenas unidas con xfade de 0.2 s.
Con musica -> versión Instagram (AAC 192k). Sin musica -> versión TikTok (-an)."""
import sys, json, subprocess, os
d, out = sys.argv[1], sys.argv[2]; music = sys.argv[3] if len(sys.argv) > 3 else None
meta = json.load(open(os.path.join(d, 'meta.json'))); X = 0.2; FPS = 30
inputs, fil, labels = [], [], []
idx = 0
for i, m in enumerate(meta):
    dur = m['dur'] + (X if i < len(meta) - 1 else 0)
    inputs += ['-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', os.path.join(d, f's{i}_bg.png')]
    base = idx; idx += 1
    fil.append(f'[{base}:v]scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[b{i}_0]')
    cur = f'b{i}_0'
    step = m.get('step', min(0.32, 0.9 / max(1, m['layers'])))
    for k in range(m['layers']):
        inputs += ['-loop', '1', '-framerate', str(FPS), '-t', f'{dur:.3f}', '-i', os.path.join(d, f's{i}_L{k}.png')]
        st = 0.08 + k * step if i > 0 or k > 0 else 0.0  # el gancho entra ya en el frame 0
        fil.append(f'[{idx}:v]format=rgba,fade=in:st={st:.2f}:d=0.22:alpha=1[l{i}_{k}]')
        y = f"'if(lt(t,{st:.2f}),60,max(0,60*(1-(t-{st:.2f})/0.22)))'" if st > 0 else '0'
        fil.append(f'[{cur}][l{i}_{k}]overlay=x=0:y={y}:format=auto[b{i}_{k+1}]')
        cur = f'b{i}_{k+1}'; idx += 1
    fil.append(f'[{cur}]fps={FPS},format=yuv420p[sc{i}]'); labels.append(f'sc{i}')
prev, off = labels[0], 0.0
for i in range(1, len(labels)):
    off += meta[i - 1]['dur']
    tr = 'slideup' if i % 2 else 'wipeleft'
    if i == len(labels) - 1: tr = 'fade'
    fil.append(f'[{prev}][{labels[i]}]xfade=transition={tr}:duration={X}:offset={off:.3f}[x{i}]'); prev = f'x{i}'
total = sum(m['dur'] for m in meta)
cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs
if music: cmd += ['-i', music]
cmd += ['-filter_complex', ';'.join(fil), '-map', f'[{prev}]']
if music: cmd += ['-map', f'{idx}:a', '-c:a', 'aac', '-b:a', '192k', '-shortest']
else: cmd += ['-an']
cmd += ['-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-tune', 'stillimage', '-r', str(FPS), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print(out, f'{total:.1f}s')
