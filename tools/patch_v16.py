from pathlib import Path

# v1.6 hotfix is applied after v1.4 + v1.5 patches.
# v1.5 accidentally placed a function declaration directly after a
# window.importSharedText assignment without a statement terminator.
# WebView therefore failed to parse the entire script and the app UI was inert.
index = Path('app/src/main/assets/index.html')
html = index.read_text(encoding='utf-8')

old = "return false}} function importClipboard()"
new = "return false}}; function importClipboard()"
if old not in html:
    raise SystemExit('v1.6 JavaScript hotfix target not found')
html = html.replace(old, new, 1)
index.write_text(html, encoding='utf-8')

gradle = Path('app/build.gradle')
g = gradle.read_text(encoding='utf-8')
g = g.replace('versionCode 6', 'versionCode 7', 1)
g = g.replace("versionName '1.5'", "versionName '1.6'", 1)
gradle.write_text(g, encoding='utf-8')

print('Applied JOB_Track v1.6 startup hotfix')
