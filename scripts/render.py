#!/usr/bin/env python3
"""Add effects to a talking-head clip. One command, both engines, Mac and Windows.

usage:
  python render.py <clip> <plan.json> <out.mp4>            render the clip with every effect in the plan
  python render.py <clip> <plan.json> <out_dir> --check    only save one still per effect (fast look before the full render)

plan.json:
  {"name": "Raed", "handle": "@raed",
   "effects": [{"fx": "orbit", "start": 3.0, "end": 6.0},
               {"fx": "palm-tags", "start": 8.0, "end": 11.5, "replace": {"OLD WAY": "BEFORE", "CLAUDE": "AFTER"}}]}
Times are seconds in the clip. "replace" swaps on-screen words in the studio effects (see SKILL.md for each effect's words).
"""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
STUDIO = {'paper-cut', 'palm-tags', 'wall-of-words', 'green-screen', 'phone-mockup'}
CLASSIC = {'glass-widgets', 'orbit', 'spotlight', 'glitter-spotlight', 'checklist', 'liquid-glass-graph', 'apple-toggles', 'messages',
           'led-sign', 'red-collage', 'cover-star', 'split-headline', 'backdrop-word', 'headline-wall', 'match-cut', 'place-in-grid'}
WAITLIST = {'documentary', 'render-studio', 'shatter-on-clap', 'glass-type', 'frame-break', 'vertigo', 'echo-hands', 'ui-world', 'zoom-through-cut'}
WAITLIST_MSG = 'is coming soon in the Creator Studio plugin, not in this free pack. Join the waitlist to get it.'


def run(cmd, **kw):
    print('  $', ' '.join(str(c) for c in cmd[:4]), '...', flush=True)
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def duration(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True, check=True).stdout)


def prep(clip, work):
    d = os.path.join(work, 'prep')
    if not os.path.exists(os.path.join(d, 'tracking.js')):
        print('Cutting you out and tracking your face and hands (once per clip)...', flush=True)
        run([PY, os.path.join(ROOT, 'scripts', 'prep.py'), clip, d])
    thumbs = os.path.join(d, 'thumbs')
    if not os.path.isdir(thumbs):
        os.makedirs(thumbs); dur = duration(os.path.join(d, 'plate.mp4'))
        for i in range(1, 9):
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(dur * (i - .5) / 8), '-i', os.path.join(d, 'plate.mp4'),
                            '-frames:v', '1', '-vf', 'crop=1080:1350:0:250,scale=240:-1', os.path.join(thumbs, f't{i}.jpg')], check=True)
    return d


def studio_clip(e, i, pdir, work, draft):
    """Render one studio effect for its window as its own short video."""
    lab = os.path.join(work, 'lab'); os.makedirs(os.path.join(lab, 'effects'), exist_ok=True)
    assets = os.path.join(lab, 'assets'); os.makedirs(assets, exist_ok=True)
    for f in ('plate.mp4', 'subject.webm', 'tracking.js'):
        if not os.path.exists(os.path.join(assets, f)): shutil.copy(os.path.join(pdir, f), assets)
    for f in ('gsap.min.js', 'fxkit.js'): shutil.copy(os.path.join(ROOT, 'kit', f), assets)
    if not os.path.isdir(os.path.join(assets, 'thumbs')): shutil.copytree(os.path.join(pdir, 'thumbs'), os.path.join(assets, 'thumbs'))
    s, d = float(e['start']), float(e['end']) - float(e['start'])
    html = open(os.path.join(ROOT, 'effects', e['fx'] + '.html'), encoding='utf-8').read()
    import re
    html = re.sub(r'window\.FX_START = [0-9.]+;', f'window.FX_START = {s:.3f};', html)
    html = re.sub(r'data-media-start="[0-9.]+"', f'data-media-start="{s:.3f}"', html)
    html = html.replace('data-duration="4"', f'data-duration="{d:.3f}"').replace('FX.follow(tl, 0, 4,', f'FX.follow(tl, 0, {d:.3f},')
    for old, new in (e.get('replace') or {}).items(): html = html.replace(old, new)
    name = f"{e['fx']}_{i}.html"
    open(os.path.join(lab, 'effects', name), 'w', encoding='utf-8').write(html)
    out = os.path.join(work, f'fx_{i}.mp4')
    npx = shutil.which('npx') or 'npx'
    run([npx, '--yes', 'hyperframes', 'render', lab, '-c', 'effects/' + name, '-o', out, '--quality', 'draft' if draft else 'standard', '--quiet'])
    return out


def main():
    if len(sys.argv) < 4: sys.exit(__doc__)
    clip, plan_path, out = os.path.abspath(sys.argv[1]), sys.argv[2], os.path.abspath(sys.argv[3])
    check = '--check' in sys.argv
    plan = json.load(open(plan_path, encoding='utf-8')); fx = plan['effects']
    for e in fx:
        n = e['fx'] = e['fx'].lower().lstrip('/')
        if n in WAITLIST: sys.exit(f"'{n}' {WAITLIST_MSG}")
        if n not in STUDIO | CLASSIC: sys.exit(f"Unknown effect '{n}'. Free effects: {', '.join(sorted(STUDIO | CLASSIC))}")
        if float(e['end']) <= float(e['start']): sys.exit(f"'{n}': end must be after start")
    stem = os.path.splitext(os.path.basename(clip))[0]
    work = os.path.join(os.path.dirname(clip), stem + '_effects_work'); os.makedirs(work, exist_ok=True)
    studio = [e for e in fx if e['fx'] in STUDIO]; classic = [e for e in fx if e['fx'] in CLASSIC]
    pdir = prep(clip, work) if studio else None
    base_src = os.path.join(pdir, 'plate.mp4') if pdir else clip

    # classic effects: one pass with the plan (they draw onto the frames)
    cplan = os.path.join(work, 'classic_plan.json')
    for e in classic:
        e.setdefault('name', plan.get('name', 'You')); e.setdefault('handle', plan.get('handle', '@yourhandle'))
        if e['fx'] == 'glitter-spotlight': e['fx'], e['look'] = 'spotlight', e.get('look', 'sparkle')
    json.dump({'effects': classic}, open(cplan, 'w'), indent=1)
    fxpy = os.path.join(ROOT, 'engines', 'classic', 'fx.py')

    if check:
        os.makedirs(out, exist_ok=True)
        if classic:
            mids = ','.join(f"{(float(e['start']) + float(e['end'])) / 2:.2f}" for e in classic)
            run([PY, fxpy, '--plan', cplan, base_src, os.path.join(out, 'classic.png'), '--still', mids])
        for i, e in enumerate(studio):
            v = studio_clip(e, i, pdir, work, draft=True)
            mid = (float(e['end']) - float(e['start'])) * .6
            run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{mid:.2f}', '-i', v, '-frames:v', '1', os.path.join(out, f"{e['fx']}_{i}.png")])
        print('CHECK READY', out); return

    base = base_src
    if classic:
        base = os.path.join(work, 'base.mp4')
        run([PY, fxpy, '--plan', cplan, base_src, base])
    if not studio:
        shutil.copy(base, out); print('DONE', out); return
    clips = [(e, studio_clip(e, i, pdir, work, draft=False)) for i, e in enumerate(studio)]
    # lay each studio window over the base at its time; sound stays the clip's own
    inputs = ['-i', base]; chain, last = [], '0:v'
    for k, (e, v) in enumerate(clips, 1):
        s, en = float(e['start']), float(e['end'])
        inputs += ['-itsoffset', f'{s:.3f}', '-i', v]
        chain.append(f"[{last}][{k}:v]overlay=enable='between(t,{s:.3f},{en - 1 / 60:.3f})':eof_action=pass[v{k}]"); last = f'v{k}'
    run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chain), '-map', f'[{last}]', '-map', '0:a?',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out])
    print('DONE', out)


if __name__ == '__main__':
    main()
