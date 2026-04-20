# Images

Raster artwork used as PBIR backgrounds, banners, section dividers, and
placeholder/mocked logos.

> **Current state (v0.1):** the catalog is intentionally empty \u2014 no raster
> assets ship yet. Planned additions are tracked in the `gaps[]` array of
> [`images-index.json`](images-index.json) (neutral gradient backgrounds,
> banner strips, demo-customer logos). The folder structure below is the
> **target layout** when those assets land; create the subfolders as you
> populate them.

## Folders (target layout)

| Folder | Purpose | Max size / asset |
|---|---|---|
| `backgrounds/` | Full-canvas backgrounds (textures, gradients). Placed on `shape/background` visuals. | 300 KB, WebP preferred |
| `banners/` | Header bands at the top of executive pages. 1664 \u00d7 120 px typical. | 150 KB |
| `dividers/` | Horizontal / vertical dividers between page zones. | 30 KB |
| `logos/` | Placeholder / demo logos ONLY. **No real customer logos shipped here.** For production-quality industry placeholder marks see [`../logos/`](../logos/) at the asset root. |

## Rules

1. **Resolution:** match the target canvas — 1664 × 936 (desktop 16:9) or
   320 × 568 (phone). Never upscale.
2. **Compression:** WebP (lossless ≤ 100 KB, lossy ≤ 50 KB). JPEG for photos.
   PNG only when transparency is required and WebP isn't supported.
3. **Alt-text friendly:** every image's `alt` field in the index must be ≥ 20
   chars and describe the image's *role* (not its subject). Lint W10 enforces.
4. **License** in index for every file. Prefer CC0 (Unsplash / Pexels license).

## Index

[`images-index.json`](images-index.json) — same manifest convention as icons.
Schema lives at [`images-index.schema.json`](images-index.schema.json).
