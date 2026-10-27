#!/usr/bin/env python3
"""Prepare one talking-head clip for the effects, once. Works on Mac and Windows (MediaPipe + ffmpeg, no GPU).

usage: python prep.py <clip> <out_dir> [--start S] [--end E] [--width 1080]

Writes into out_dir:
  plate.mp4      the clip, vertical 1080x1920 (or --width), 30 fps, H.264, original audio
  matte.mp4      person matte, white = you (gray H.264)
  subject.webm   you cut out, VP9 with alpha (layer it above anything that should go behind you)
  tracking.json  per frame: face box, forehead, eyes, chin, tilt; up to two hands (21 points), all smoothed, in plate pixels
  tracking.js    the same data as `window.TRACK = {...}` for HyperFrames scenes
  check.jpg      3 frames of the cut-out over orange, to check edges round hair and fingers
"""
import argparse, json, math, os, subprocess, sys
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(os.path.dirname(HERE), 'models')


def probe(path):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', path],
                                  capture_output=True, text=True, check=True).stdout)
    return float(j['format']['duration'])


def frames(path, W, H, start, dur):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', path, '-t', str(dur),
           '-vf', f'fps=30,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},format=rgb24',
           '-f', 'rawvideo', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    p.stdout.close(); p.wait()


def guided(I, p, r=10, eps=1e-3):
    box = lambda x: cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1))
    mI, mp_ = box(I), box(p)
    a = (box(I * p) - mI * mp_) / (box(I * I) - mI * mI + eps)
    b = mp_ - a * mI
    return np.clip(box(a) * I + box(b), 0, 1)


def smooth(arr, tau_frames=4.0):
    """Forward + backward exponential smoothing over frames; NaN gaps are filled from neighbours first."""
    arr = np.array(arr, np.float64)
    if arr.ndim == 1: arr = arr[:, None]
    for k in range(arr.shape[1]):
        col = arr[:, k]; good = ~np.isnan(col)
        if good.sum() == 0: continue
        col[~good] = np.interp(np.where(~good)[0], np.where(good)[0], col[good]); arr[:, k] = col
    a = 1 - math.exp(-1 / tau_frames)
    for i in range(1, len(arr)): arr[i] = arr[i - 1] + a * (arr[i] - arr[i - 1])
    for i in range(len(arr) - 2, -1, -1): arr[i] = arr[i + 1] + a * (arr[i] - arr[i + 1])
    return arr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('clip'); ap.add_argument('out')
    ap.add_argument('--start', type=float, default=0.0); ap.add_argument('--end', type=float)
    ap.add_argument('--width', type=int, default=1080)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    W = a.width; H = int(round(W * 16 / 9 / 2)) * 2
    end = a.end if a.end is not None else probe(a.clip)
    dur = end - a.start

    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core.base_options import BaseOptions
    VIDEO = vision.RunningMode.VIDEO
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(MODELS, 'selfie_multiclass_256x256.tflite')),
        running_mode=VIDEO, output_confidence_masks=True, output_category_mask=False))
    face = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(MODELS, 'face_landmarker.task')), running_mode=VIDEO, num_faces=1))
    hands = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(MODELS, 'hand_landmarker.task')), running_mode=VIDEO, num_hands=2,
        min_hand_detection_confidence=0.4, min_tracking_confidence=0.4))

    # plate (with audio) straight from ffmpeg
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a.start), '-i', a.clip, '-t', str(dur),
                    '-vf', f'fps=30,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},format=yuv420p',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-g', '30', '-keyint_min', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                    os.path.join(a.out, 'plate.mp4')], check=True)

    menc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                             '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', os.path.join(a.out, 'matte.mp4')],
                            stdin=subprocess.PIPE)
    sw, sh = 540, int(round(540 * H / W))
    prev = None; F = []; HD = []; checks = {}
    n_total = int(dur * 30)
    for i, rgb in enumerate(frames(a.clip, W, H, a.start, dur)):
        ms = int(i * 1000 / 30)
        small = cv2.resize(rgb, (sw, sh), interpolation=cv2.INTER_AREA)
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(small))
        bg = seg.segment_for_video(img, ms).confidence_masks[0].numpy_view().astype(np.float32).reshape(sh, sw)
        m = cv2.resize(1 - bg, (W, H), interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        m = guided(gray, m, r=8, eps=2e-3)
        m = np.clip((m - 0.5) * 1.8 + 0.5, 0, 1)
        if prev is not None: m = 0.7 * m + 0.3 * prev
        prev = m
        menc.stdin.write((m * 255 + 0.5).astype(np.uint8).tobytes())
        if i in (int(n_total * 0.2), int(n_total * 0.5), int(n_total * 0.8)): checks[i] = (rgb.copy(), m.copy())

        fr = face.detect_for_video(img, ms)
        if fr.face_landmarks:
            L = np.array([[p.x * W, p.y * H] for p in fr.face_landmarks[0]])
            x0, y0 = L.min(0); x1, y1 = L.max(0)
            le = L[[33, 133]].mean(0); re = L[[362, 263]].mean(0)
            F.append([(x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, *L[10], *le, *re, *L[152]])
        else:
            F.append([np.nan] * 12)
        hr = hands.detect_for_video(img, ms)
        hs = sorted([np.array([[p.x * W, p.y * H] for p in h]) for h in hr.hand_landmarks], key=lambda h: h[0, 0])
        HD.append(hs)
        if i % 150 == 0: print(f'  {i / 30:5.1f}s / {dur:.1f}s', flush=True)
    menc.stdin.close(); menc.wait()

    n = len(F)
    Fs = smooth(F, 3.0)
    # hands: keep the left/right slot by x position, smooth each slot, mark frames where it was seen
    slots = []
    for s in range(2):
        pts, seen = [], []
        for hs in HD:
            h = None
            if len(hs) == 2: h = hs[s]
            elif len(hs) == 1: h = hs[0] if (hs[0][0, 0] < W / 2) == (s == 0) else None
            pts.append(h.reshape(-1) if h is not None else [np.nan] * 42); seen.append(h is not None)
        slots.append((smooth(pts, 2.5) if any(seen) else None, seen))

    out = {'fps': 30, 'width': W, 'height': H, 'start': a.start, 'frames': n, 'face': [], 'hands': []}
    for i in range(n):
        f = Fs[i]
        tilt = math.degrees(math.atan2(f[9] - f[7], f[8] - f[6]))
        out['face'].append({'cx': round(f[0], 1), 'cy': round(f[1], 1), 'w': round(f[2], 1), 'h': round(f[3], 1),
                            'forehead': [round(f[4], 1), round(f[5], 1)], 'leye': [round(f[6], 1), round(f[7], 1)],
                            'reye': [round(f[8], 1), round(f[9], 1)], 'chin': [round(f[10], 1), round(f[11], 1)], 'tilt': round(tilt, 2)})
        hh = []
        for arr, seen in slots:
            hh.append({'seen': bool(seen[i]), 'pts': [[round(arr[i][2 * k], 1), round(arr[i][2 * k + 1], 1)] for k in range(21)]} if arr is not None else None)
        out['hands'].append(hh)
    json.dump(out, open(os.path.join(a.out, 'tracking.json'), 'w'), separators=(',', ':'))
    open(os.path.join(a.out, 'tracking.js'), 'w').write('window.TRACK = ' + json.dumps(out, separators=(',', ':')) + ';\n')

    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(a.out, 'plate.mp4'), '-i', os.path.join(a.out, 'matte.mp4'),
                    '-filter_complex', '[1]format=gray[m];[0][m]alphamerge,format=yuva420p', '-an',
                    '-c:v', 'libvpx-vp9', '-b:v', '6M', '-g', '30', '-auto-alt-ref', '0', '-row-mt', '1', '-deadline', 'realtime', '-cpu-used', '8',
                    os.path.join(a.out, 'subject.webm')], check=True)

    tiles = []
    for i in sorted(checks):
        rgb, m = checks[i]
        o = rgb * m[..., None] + np.array([255, 120, 30]) * (1 - m[..., None])
        tiles.append(cv2.resize(o.astype(np.uint8), (W // 3, H // 3)))
    if tiles: cv2.imwrite(os.path.join(a.out, 'check.jpg'), cv2.cvtColor(np.hstack(tiles), cv2.COLOR_RGB2BGR))
    seen = sum(1 for f in F if not np.isnan(f[0]))
    print(f'READY  {n} frames, face found in {seen}, hands in {sum(1 for h in HD if h)}  ->  {a.out}')


if __name__ == '__main__':
    main()
