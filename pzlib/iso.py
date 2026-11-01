"""Proyeccion isometrica exacta de PZ B42 y re-proyeccion de sprites a caras 3D.

Espacio de escena (tileGeometry.txt): X = mundo +x, Y = arriba, Z = mundo +y,
origen = centro del suelo del cuadro, 1 piso = sqrt(6).
Sprite 2x (128x256): px = 64 + 64(X-Z), py = 224 + 32(X+Z) - (192/sqrt6) Y
(TileGeometryFile.java:704-705, IsoUtils.java).
"""
import hashlib
import io
import math
import os

import numpy as np
from PIL import Image

S6 = math.sqrt(6.0)
KY = 192.0 / S6
VIEW = np.array([S6 / 2, 1.0, S6 / 2])
VIEW = VIEW / np.linalg.norm(VIEW)

# Caras de Part de Roblox en ejes locales: (token, normal, derecha, arriba, eje_w, eje_h)
FACES = {
    'Right':  (0, (1, 0, 0), (0, 0, -1), (0, 1, 0), 2, 1),
    'Top':    (1, (0, 1, 0), (1, 0, 0), (0, 0, -1), 0, 2),
    'Back':   (2, (0, 0, 1), (1, 0, 0), (0, 1, 0), 0, 1),
    'Left':   (3, (-1, 0, 0), (0, 0, 1), (0, 1, 0), 2, 1),
    'Bottom': (4, (0, -1, 0), (1, 0, 0), (0, 0, 1), 0, 2),
    'Front':  (5, (0, 0, -1), (-1, 0, 0), (0, 1, 0), 0, 1),
}


def rot_xyz(rx, ry, rz):
    """JOML rotateXYZ: R = Rx * Ry * Rz (grados)."""
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    Rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
    Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    Rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    return Rx @ Ry @ Rz


def rot_y(deg):
    return rot_xyz(0, deg, 0)


def project(P, anchor=(64.0, 224.0)):
    P = np.asarray(P, dtype=float)
    X, Y, Z = P[..., 0], P[..., 1], P[..., 2]
    return np.stack([anchor[0] + 64.0 * (X - Z), anchor[1] + 32.0 * (X + Z) - KY * Y], axis=-1)


class TextureStore:
    """Guarda PNGs deduplicados por contenido; devuelve url rbxasset://."""

    def __init__(self, outdir, prefix='pz42'):
        self.dir = outdir
        self.prefix = prefix
        os.makedirs(outdir, exist_ok=True)
        self.count = 0

    def put(self, img):
        buf = io.BytesIO()
        img.save(buf, 'PNG', optimize=False)
        data = buf.getvalue()
        h = hashlib.sha1(data).hexdigest()[:20]
        path = os.path.join(self.dir, h + '.png')
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(data)
            self.count += 1
        return 'rbxasset://%s/%s.png' % (self.prefix, h)


def stats(img):
    a = np.asarray(img, dtype=np.float32)
    alpha = a[..., 3] / 255.0
    cov = float(alpha.mean()) if alpha.size else 0.0
    if alpha.sum() > 0:
        col = (a[..., :3] * alpha[..., None]).sum(axis=(0, 1)) / alpha.sum()
    else:
        col = np.array([128, 128, 128])
    return cov, tuple(int(max(0, min(255, round(v)))) for v in col)


def face_image(sprite, anchor, R, pos, size, face, ppu=96, maxpx=256):
    """Re-proyecta el sprite isometrico sobre una cara de un Part.
    R, pos: rotacion/posicion del Part en escena local del cuadro (unidades de escena)."""
    tok, n, r, u, iw, ih = FACES[face]
    n, r, u = (np.array(v, dtype=float) for v in (n, r, u))
    size = np.asarray(size, dtype=float)
    w, h = size[iw], size[ih]
    half_n = abs(float(n @ size)) / 2.0
    W = int(max(4, min(maxpx, round(w * ppu))))
    H = int(max(4, min(maxpx, round(h * ppu))))
    c0 = n * half_n
    P00 = c0 + r * (-0.5 * w) + u * (0.5 * h)
    P10 = c0 + r * (0.5 * w) + u * (0.5 * h)
    P01 = c0 + r * (-0.5 * w) + u * (-0.5 * h)
    pts = np.array([P00, P10, P01]) @ R.T + pos
    q = project(pts, anchor)
    ex = (q[1] - q[0]) / W
    ey = (q[2] - q[0]) / H
    coeffs = (ex[0], ey[0], q[0][0] + 0.5 * (ex[0] + ey[0]),
              ex[1], ey[1], q[0][1] + 0.5 * (ex[1] + ey[1]))
    img = sprite.transform((W, H), Image.AFFINE, coeffs, resample=Image.BILINEAR)
    return img


def floor_image(sprite, size=128):
    """Desproyecta el rombo del suelo (128x64 en y 192..256) a un cuadrado.
    Cara Top de Roblox: derecha = +X (dx), arriba = -Z => fila v crece con dy."""
    k = 128.0 / size
    coeffs = (0.5 * k, -0.5 * k, 64.0, 0.25 * k, 0.25 * k, 192.0)
    return sprite.transform((size, size), Image.AFFINE, coeffs, resample=Image.BILINEAR)


def reconstruct_points(sprite, depth, anchor=(64.0, 224.0), step=2):
    """Invierte la proyeccion usando el mapa de profundidad B42:
    normDepth = 1 - 0.25(dx+dy) - 0.5 dz (TileGeometryUtils.getNormalizedDepth)."""
    a = np.asarray(sprite)[::step, ::step, 3]
    ys, xs = np.nonzero(a > 160)
    if len(xs) < 12:
        return None
    ys = ys * step
    xs = xs * step
    d = depth[ys, xs]
    ok = d < 0.999
    ys, xs, d = ys[ok], xs[ok], d[ok]
    if len(xs) < 12:
        return None
    dz = (320.0 - 128.0 * d - ys) / 256.0
    s = 4.0 - 4.0 * d - 2.0 * dz
    aa = (xs - 64.0) / 64.0
    dx = (s + aa) / 2.0
    dy = (s - aa) / 2.0
    return np.c_[dx - 0.5, dz * S6, dy - 0.5]


def fit_panel(P):
    """Ajusta un plano a la nube; devuelve (R, centro, tam, rms) con eje local Y = normal."""
    c = P.mean(axis=0)
    U, Sv, Vt = np.linalg.svd(P - c, full_matrices=False)
    nrm = Vt[2]
    if nrm[1] < -1e-6 or (abs(nrm[1]) < 1e-6 and nrm @ VIEW < 0):
        nrm = -nrm
    rms = float(Sv[2] / math.sqrt(len(P)))
    cand = []
    for ax in (np.array([1.0, 0, 0]), np.array([0, 0, 1.0]), np.array([0, 1.0, 0])):
        p = ax - nrm * (ax @ nrm)
        cand.append((np.linalg.norm(p), p))
    cand.sort(key=lambda t: -t[0])
    ux = cand[0][1] / cand[0][0]
    uz = np.cross(ux, nrm)
    R = np.c_[ux, nrm, uz]
    loc = (P - c) @ R
    lo, hi = loc.min(axis=0), loc.max(axis=0)
    mid = (lo + hi) / 2.0
    center = c + R @ np.array([mid[0], 0.0, mid[2]])
    size = np.array([max(0.02, hi[0] - lo[0]), 0.02, max(0.02, hi[2] - lo[2])])
    return R, center, size, rms
