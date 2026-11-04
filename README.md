# Nicole Salem — Portfolio

Static portfolio site, hosted on Netlify. Every push to `main` redeploys automatically.

## Editing

- **Project text:** `build/content.py`
- **Page layout and Home/About text:** `build/build.py`
- **Styles:** `assets/styles.css`
- **Menu and project filters:** `assets/site.js`

To preview locally, generate the pages into `public/`:

```
python3 build/build.py
```

Netlify runs this same command on every push and publishes `public/`, so you only need to commit the source files.
