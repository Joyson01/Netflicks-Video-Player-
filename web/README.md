# NetFlex web

A browser-first reimagining of Joyson's [original Tkinter/VLC project](https://github.com/Joyson01/Netflicks-Video-Player-). Ten openly licensed Blender films with real streaming playback. No account, uploads, analytics, database, or API keys.

## Run

Requires Python 3 for the preview server and Node 18+ for tests. The site itself has no build step or runtime package dependencies.

```sh
python3 -m http.server 4187 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4187. Serve over HTTP(S); ES modules and catalogue loading cannot run by opening index.html as a file.

## Features

- Responsive cinematic home, searchable film collection and combined genre filters.
- Film details, editorial content notes, creator credits and licence links.
- HTML5 video with native playback, volume, seeking and fullscreen controls, manual quality selection, ten-second skips, restart and retry.
- My List and Continue Watching stored only in localStorage under `netflex:v1`. Progress saves every four seconds and on pause, close, backgrounding and page exit. Finished films are removed from Continue Watching.
- Hash links for films/player; browser navigation, keyboard-accessible dialogs and reduced-motion support.
- Browser data controls with explicit two-step reset. Unavailable storage degrades to in-memory session state; corrupt saved records are ignored.

## Check

```sh
node --check dist/app.mjs
node --test tests/*.test.mjs
```

Browser QA: Spring playback, seeking, resume after reload, watchlist persistence, search, genre filtering, film details and narrow viewport. External streams were range-checked during catalogue preparation. Availability remains dependent on Blender's public video service; stream URLs can change. The player provides quality selection, retry and a link to the original film when playback fails. No video assets are rehosted. Native format support can vary by browser.

## Content

`dist/catalog.json` stores the reviewed metadata and stream URLs. Artwork in `dist/assets/` comes from the linked official project pages. Videos are streamed unmodified from video.blender.org. The About page and each film detail show creator attribution and CC licence links. Content notes are editorial guidance, not official ratings. NetFlex is not affiliated with Netflix or Blender.

`scripts/prepare_catalog.py` refreshes media source metadata and artwork using Blender's public API and official project pages (requires `requests` and `beautifulsoup4`). Review licence metadata and changes before publishing a refreshed catalogue. The initial collection was prepared 2026-11-18.

## Hosting

GitHub Pages publishes `web/dist/` at https://netflex.joyson01.me. The deployment workflow runs when files in `web/dist/` change on `main`. The same directory can be served by any static HTTPS host.

The app stores no visitor reports. Google Fonts supplies the typefaces; the hosting provider, fonts provider and Blender servers receive normal network requests. Browser storage is per origin and device: preview and production have independent watchlists, and clearing site data resets them.
