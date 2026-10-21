"""把 src/page.html（頁面本體）包成可獨立開啟的 www/index.html。"""
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
page = (root / "src" / "page.html").read_text(encoding="utf8")

head = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b0e12">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="抽成記錄">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>
:root{color-scheme:light;padding-top:max(env(safe-area-inset-top,0px),var(--safe-area-inset-top,0px));padding-bottom:max(env(safe-area-inset-bottom,0px),var(--safe-area-inset-bottom,0px))}
body{margin:0;font:14px system-ui,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
</head><body>
"""

tail = """
<script>
if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0 && location.hostname !== 'localhost') {
  navigator.serviceWorker.register('sw.js').catch(function () {});
}
</script>
</body></html>
"""

out = root / "www" / "index.html"
out.write_text(head + page + tail, encoding="utf8")
print("wrote", out, len(head + page + tail), "bytes")
