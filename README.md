# Printers - Static Site

This is a simple static website for a printers shop. It's intended to be hosted on GitHub Pages.

What is included
- `index.html` - Home page (default)
- `wedding-cards.html` - Gallery of wedding card samples
- `assets/` - CSS, JS, images
- `data/cards.json` - Manifest of wedding card items and their images

How the Wedding Cards page works
- Each wedding card item is represented by a subfolder under `assets/images/cards/<folder>`.
- The `data/cards.json` file lists each item, its `folder` name, `title`, and an `images` array. The JS (`assets/js/cards.js`) reads this manifest and builds a Bootstrap carousel for each item.

To add a new card
1. Create a new folder under `assets/images/cards`, e.g. `card4`.
2. Add images named as you like, e.g. `1.jpg`, `2.jpg`.
3. Edit `data/cards.json` and add an entry listing the `folder` and `images`.

Publish on GitHub Pages
1. Create a new GitHub repository and push this folder as the repo root.
2. In GitHub repository settings, enable GitHub Pages and select the `main` branch and `/ (root)` as the site source.
3. Your site will be available at `https://<username>.github.io/<repo>/`.

Local testing
You can run a simple static server. With Python 3 installed:

```powershell
python -m http.server 8000
# then open http://localhost:8000/index.html
```

Auto-generate `data/cards.json`

If you add many folders or images, use the provided script to generate `data/cards.json` automatically.

```powershell
python scripts/generate_cards_json.py
```

Image optimization (optional)

Install Pillow and run the optimizer to resize and compress images in-place:

```powershell
pip install -r requirements.txt
python scripts/optimize_images.py --max-size 1600 --quality 85
```

Batch import images

If you'd like to bulk upload or replace images, put them in a folder named `incoming/` at the workspace root or provide a zip archive and use the importer script:

```powershell
# Import from a folder named 'incoming' and regenerate the manifest
python scripts/import_images.py incoming --generate

# Import from a zip and also optimize images
python scripts/import_images.py uploads/images.zip --generate --optimize
```

Naming conventions supported by the importer:
- `banner.jpg` or `banner.png` at the root of the incoming folder will replace the site's banner.
- Subfolders named `card1`, `card2`, etc. will be copied into `assets/images/cards/card1`, etc.
- Files named like `card1_1.jpg` or `card1-1.jpg` will be copied into `assets/images/cards/card1/`.
Files named like `card1_1.jpg` or `card1-1.jpg` will be copied into `assets/images/cards/card1/`.

Publishing from `main` with GitHub Actions
----------------------------------------

This repository includes a GitHub Actions workflow that will automatically publish the repository root to GitHub Pages whenever you push to the `main` branch. The workflow file is `.github/workflows/pages.yml` and a `.nojekyll` file is included so static files are served as-is.

To publish from your local machine (PowerShell):

```powershell
# set your repo remote if you haven't already
git remote add origin https://github.com/<your-username>/<your-repo>.git

# ensure you're on main and up-to-date
git checkout -B main

# stage the new files and any other changes
git add .
git commit -m "Add GitHub Pages workflow and publishing helpers"

# push to GitHub (you may be prompted for credentials or token)
git push -u origin main
```

After pushing, open the repository on GitHub and verify the workflow ran under the Actions tab. Pages will be available at `https://<your-username>.github.io/<your-repo>/` once the deploy step completes.

If you prefer to use a `gh-pages` branch instead of `main`, I can adjust the workflow and instructions.
 
Quick verification checklist
- Confirm the workflow file exists on GitHub at `.github/workflows/pages.yml`.
- In the repository's Actions tab, check that a run started after your push and that the "Deploy to GitHub Pages" job completed successfully.
- Visit `https://ksh7393.github.io/padmavathiprinters/` (or the URL shown in your Pages settings) once the Actions deployment step finishes.

Badge (optional)
You can show a Pages workflow badge in this README. Replace `<your-username>` and `<your-repo>` with your values:

```markdown
[![pages-build-deployment](https://github.com/<your-username>/<your-repo>/actions/workflows/pages.yml/badge.svg)](https://github.com/<your-username>/<your-repo>/actions/workflows/pages.yml)
```

If you prefer to use a `gh-pages` branch instead of `main`, I can adjust the workflow and instructions.


