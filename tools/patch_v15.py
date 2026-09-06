from pathlib import Path

# v1.5 is applied after tools/patch_v14.py.
index = Path('app/src/main/assets/index.html')
html = index.read_text(encoding='utf-8')

old_data = '''function dataPage(skipHistory=false){ setRoute({view:'data'},skipHistory); fab.classList.add('hidden'); app.innerHTML=`<div class="toolbar"><button class="secondary" onclick="history.back()">← 홈으로</button></div><div class="section"><h3>데이터 관리</h3><div class="box text">ChatGPT에서 받은 .json 파일을 선택하면 기업 분석이 바로 저장됩니다.</div></div><input id="jsonFileInput" class="hidden" type="file" accept=".json,application/json" onchange="importJsonFile(event)"><div class="actions"><button class="secondary" onclick="document.getElementById('jsonFileInput').click()">JSON 파일 선택</button><button class="secondary" onclick="exportJ()">데이터 백업 복사</button></div>`; window.scrollTo(0,0) }'''
new_data = '''function dataPage(skipHistory=false){ setRoute({view:'data'},skipHistory); fab.classList.add('hidden'); app.innerHTML=`<div class="toolbar"><button class="secondary" onclick="history.back()">← 홈으로</button></div><div class="section"><h3>데이터 관리</h3><div class="box text">평소에는 ChatGPT의 앱 저장용 JSON 텍스트를 Android 공유 메뉴에서 <b>이직로그</b>로 보내면 바로 저장할 수 있습니다.<br><br>공유가 어려우면 JSON을 복사한 뒤 아래의 <b>클립보드에서 가져오기</b>를 누르세요. .json 파일 선택은 백업·대량 가져오기용입니다.</div></div><input id="jsonFileInput" class="hidden" type="file" accept=".json,application/json" onchange="importJsonFile(event)"><div class="actions"><button class="secondary" onclick="importClipboard()">클립보드에서 가져오기</button><button class="secondary" onclick="document.getElementById('jsonFileInput').click()">JSON 파일 선택</button><button class="secondary" onclick="exportJ()">데이터 백업 복사</button></div>`; window.scrollTo(0,0) }'''
if old_data not in html:
    raise SystemExit('v1.5 dataPage target not found')
html = html.replace(old_data, new_data, 1)

old_import = '''function mergeImportedData(x){const list=Array.isArray(x)?x:[x];let count=0;for(const raw of list){if(!raw||typeof raw!=='object'||Array.isArray(raw))continue;const item={...raw};item.id=item.id||'id'+Date.now()+Math.random().toString(16).slice(2);const i=a.findIndex(v=>v.id===item.id);if(i>=0)a[i]=item;else a.unshift(item);count++}if(!count)throw new Error('no valid company');save();alert(count+'개 기업을 가져왔습니다.');dataPage(true)} function importJsonFile(ev){const input=ev&&ev.target;const file=input&&input.files&&input.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{mergeImportedData(JSON.parse(String(reader.result||'')))}catch(_){alert('JSON 파일 형식을 확인하세요.')}};reader.onerror=()=>alert('파일을 읽을 수 없습니다.');reader.readAsText(file,'UTF-8');} function importJ(){let t=prompt('기업 분석 데이터를 붙여넣으세요.');if(!t)return;try{mergeImportedData(JSON.parse(t))}catch(_){alert('데이터 형식을 확인하세요.')}}'''
new_import = r'''function mergeImportedData(x,options={}){const list=Array.isArray(x)?x:[x];let count=0,lastId='';for(const raw of list){if(!raw||typeof raw!=='object'||Array.isArray(raw))continue;if(!String(raw.company||'').trim())continue;const item={...raw};item.id=item.id||'id'+Date.now()+Math.random().toString(16).slice(2);const i=a.findIndex(v=>v.id===item.id);if(i>=0)a[i]={...a[i],...item};else a.unshift(item);lastId=item.id;count++}if(!count)throw new Error('no valid company');save();if(options.openDetail&&count===1&&lastId){history.replaceState({view:'detail',id:lastId},'');detail(lastId,true)}else if(options.returnHome){history.replaceState({view:'home'},'');home(true)}else dataPage(true);if(!options.silent)alert(count+'개 기업을 가져왔습니다.');return {count,lastId}} function parseSharedJson(text){let t=String(text||'').trim();if(!t)throw new Error('empty share');const tryParse=s=>{try{return JSON.parse(String(s).trim())}catch(_){return null}};let direct=tryParse(t);if(direct)return direct;const fence=/```(?:json)?\s*([\s\S]*?)```/gi;let m;while((m=fence.exec(t))){const v=tryParse(m[1]);if(v)return v}function balanced(start){const open=t[start],close=open==='{'?'}':']';let depth=0,inStr=false,esc=false;for(let i=start;i<t.length;i++){const ch=t[i];if(inStr){if(esc){esc=false;continue}if(ch==='\\'){esc=true;continue}if(ch==='"')inStr=false;continue}if(ch==='"'){inStr=true;continue}if(ch===open)depth++;else if(ch===close){depth--;if(depth===0)return t.slice(start,i+1)}}return ''}for(let i=0;i<t.length;i++){if(t[i]==='{'||t[i]==='['){const candidate=balanced(i);if(candidate){const v=tryParse(candidate);if(v)return v}}}throw new Error('no json found')} window.importSharedText=function(text){try{const parsed=parseSharedJson(text);const result=mergeImportedData(parsed,{openDetail:true,silent:true});setTimeout(()=>alert(result.count===1?'이직로그에 저장했습니다.':'기업 '+result.count+'개를 저장했습니다.'),80);return true}catch(err){setTimeout(()=>alert('공유한 내용에서 앱 저장용 JSON을 찾지 못했습니다.\nChatGPT의 앱 저장용 JSON 블록을 공유하거나 복사해 주세요.'),80);return false}} function importClipboard(){try{if(!window.JobTrackAndroid)throw new Error('bridge');const text=JobTrackAndroid.getClipboardText();if(!String(text||'').trim()){alert('클립보드가 비어 있습니다.');return}window.importSharedText(text)}catch(_){alert('클립보드 내용을 가져올 수 없습니다.')}} function importJsonFile(ev){const input=ev&&ev.target;const file=input&&input.files&&input.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{mergeImportedData(JSON.parse(String(reader.result||'')))}catch(_){alert('JSON 파일 형식을 확인하세요.')}};reader.onerror=()=>alert('파일을 읽을 수 없습니다.');reader.readAsText(file,'UTF-8');} function importJ(){let t=prompt('기업 분석 데이터를 붙여넣으세요.');if(!t)return;try{mergeImportedData(JSON.parse(t))}catch(_){alert('데이터 형식을 확인하세요.')}}'''
if old_import not in html:
    raise SystemExit('v1.5 import target not found')
html = html.replace(old_import, new_import, 1)
index.write_text(html, encoding='utf-8')

java = Path('app/src/main/java/com/example/jobtrack/MainActivity.java')
j = java.read_text(encoding='utf-8')

j = j.replace('import android.content.Intent;\n', 'import android.content.ClipboardManager;\nimport android.content.ClipData;\nimport android.content.Context;\nimport android.content.Intent;\n', 1)
j = j.replace('import android.webkit.ValueCallback;\n', 'import android.webkit.JavascriptInterface;\nimport android.webkit.ValueCallback;\n', 1)
j = j.replace('import android.webkit.WebViewClient;\n', 'import android.webkit.WebViewClient;\n\nimport org.json.JSONObject;\n\nimport java.io.BufferedReader;\nimport java.io.InputStream;\nimport java.io.InputStreamReader;\nimport java.nio.charset.StandardCharsets;\n', 1)

j = j.replace('    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;\n', '    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;\n    private String pendingSharedText;\n    private boolean pageReady = false;\n', 1)

needle = '        getWindow().getDecorView().setSystemUiVisibility(0);\n\n        webView = new WebView(this);'
replacement = '        getWindow().getDecorView().setSystemUiVisibility(0);\n\n        captureShareIntent(getIntent());\n\n        webView = new WebView(this);'
if needle not in j:
    raise SystemExit('v1.5 onCreate share target not found')
j = j.replace(needle, replacement, 1)

needle = '        webView.setBackgroundColor(Color.rgb(11, 15, 23));\n        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);\n'
replacement = '        webView.setBackgroundColor(Color.rgb(11, 15, 23));\n        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);\n        webView.addJavascriptInterface(new AndroidBridge(), "JobTrackAndroid");\n'
if needle not in j:
    raise SystemExit('v1.5 bridge target not found')
j = j.replace(needle, replacement, 1)

needle = '''            @Override\n            @SuppressWarnings("deprecation")\n            public boolean shouldOverrideUrlLoading(WebView view, String url) {\n                return openExternal(url);\n            }\n        });'''
replacement = '''            @Override\n            @SuppressWarnings("deprecation")\n            public boolean shouldOverrideUrlLoading(WebView view, String url) {\n                return openExternal(url);\n            }\n\n            @Override\n            public void onPageFinished(WebView view, String url) {\n                super.onPageFinished(view, url);\n                pageReady = true;\n                deliverPendingShare();\n            }\n        });'''
if needle not in j:
    raise SystemExit('v1.5 WebViewClient target not found')
j = j.replace(needle, replacement, 1)

needle = '''    @Override\n    protected void onActivityResult(int requestCode, int resultCode, Intent data) {'''
methods = '''    @Override\n    protected void onNewIntent(Intent intent) {\n        super.onNewIntent(intent);\n        setIntent(intent);\n        captureShareIntent(intent);\n        deliverPendingShare();\n    }\n\n    private void captureShareIntent(Intent intent) {\n        if (intent == null || !Intent.ACTION_SEND.equals(intent.getAction())) return;\n        String text = intent.getStringExtra(Intent.EXTRA_TEXT);\n        if (text == null || text.trim().isEmpty()) {\n            Uri stream = intent.getParcelableExtra(Intent.EXTRA_STREAM);\n            if (stream != null) text = readTextFromUri(stream);\n        }\n        if (text != null && !text.trim().isEmpty()) pendingSharedText = text;\n    }\n\n    private String readTextFromUri(Uri uri) {\n        try (InputStream input = getContentResolver().openInputStream(uri);\n             BufferedReader reader = new BufferedReader(new InputStreamReader(input, StandardCharsets.UTF_8))) {\n            StringBuilder sb = new StringBuilder();\n            String line;\n            while ((line = reader.readLine()) != null) sb.append(line).append('\\n');\n            return sb.toString();\n        } catch (Exception ignored) {\n            return null;\n        }\n    }\n\n    private void deliverPendingShare() {\n        if (!pageReady || webView == null || pendingSharedText == null) return;\n        final String shared = pendingSharedText;\n        pendingSharedText = null;\n        String js = "window.importSharedText ? window.importSharedText(" + JSONObject.quote(shared) + ") : false";\n        webView.post(() -> webView.evaluateJavascript(js, null));\n    }\n\n    private class AndroidBridge {\n        @JavascriptInterface\n        public String getClipboardText() {\n            try {\n                ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);\n                if (cm == null || !cm.hasPrimaryClip()) return "";\n                ClipData clip = cm.getPrimaryClip();\n                if (clip == null || clip.getItemCount() == 0) return "";\n                CharSequence text = clip.getItemAt(0).coerceToText(MainActivity.this);\n                return text == null ? "" : text.toString();\n            } catch (Exception ignored) {\n                return "";\n            }\n        }\n    }\n\n    @Override\n    protected void onActivityResult(int requestCode, int resultCode, Intent data) {'''
if needle not in j:
    raise SystemExit('v1.5 method insertion target not found')
j = j.replace(needle, methods, 1)
java.write_text(j, encoding='utf-8')

manifest = Path('app/src/main/AndroidManifest.xml')
m = manifest.read_text(encoding='utf-8')
m = m.replace('<activity android:name=".MainActivity" android:exported="true">', '<activity android:name=".MainActivity" android:exported="true" android:launchMode="singleTop">', 1)
needle = '''            </intent-filter>\n        </activity>'''
replacement = '''            </intent-filter>\n            <intent-filter>\n                <action android:name="android.intent.action.SEND"/>\n                <category android:name="android.intent.category.DEFAULT"/>\n                <data android:mimeType="text/plain"/>\n            </intent-filter>\n            <intent-filter>\n                <action android:name="android.intent.action.SEND"/>\n                <category android:name="android.intent.category.DEFAULT"/>\n                <data android:mimeType="application/json"/>\n            </intent-filter>\n        </activity>'''
if needle not in m:
    raise SystemExit('v1.5 manifest target not found')
m = m.replace(needle, replacement, 1)
manifest.write_text(m, encoding='utf-8')

gradle = Path('app/build.gradle')
g = gradle.read_text(encoding='utf-8')
g = g.replace('versionCode 5', 'versionCode 6', 1)
g = g.replace("versionName '1.4'", "versionName '1.5'", 1)
gradle.write_text(g, encoding='utf-8')

print('Applied JOB_Track v1.5 share import patch')
