from pathlib import Path

index = Path('app/src/main/assets/index.html')
html = index.read_text(encoding='utf-8')

replacements = [
    ('<button id="fab" class="fab" onclick="form()" aria-label="기업 추가">＋</button>', '<button id="fab" class="fab" onclick="openForm()" aria-label="기업 추가">＋</button>'),
    ("if(state.view==='form')return form(state.id||'',true);", "if(state.view==='form')return openForm(state.id||'',true);"),
    ("<button onclick=\"form('${e(id)}')\">수정</button>", "<button onclick=\"openForm('${e(id)}')\">수정</button>"),
    ("function form(id='',skipHistory=false){", "function openForm(id='',skipHistory=false){"),
]

for old, new in replacements:
    if old not in html:
        raise SystemExit('index replacement target not found: ' + old[:100])
    html = html.replace(old, new, 1)

old_data = '''function dataPage(skipHistory=false){ setRoute({view:'data'},skipHistory); fab.classList.add('hidden'); app.innerHTML=`<div class="toolbar"><button class="secondary" onclick="history.back()">← 홈으로</button></div><div class="section"><h3>데이터 관리</h3><div class="box text">기업 분석 데이터를 다른 기기에서 가져오거나 백업할 때만 사용합니다. 평소에는 사용할 필요가 없습니다.</div></div><div class="actions"><button class="secondary" onclick="importJ()">데이터 가져오기</button><button class="secondary" onclick="exportJ()">데이터 백업 복사</button></div>`; window.scrollTo(0,0) }'''
new_data = '''function dataPage(skipHistory=false){ setRoute({view:'data'},skipHistory); fab.classList.add('hidden'); app.innerHTML=`<div class="toolbar"><button class="secondary" onclick="history.back()">← 홈으로</button></div><div class="section"><h3>데이터 관리</h3><div class="box text">ChatGPT에서 받은 .json 파일을 선택하면 기업 분석이 바로 저장됩니다.</div></div><input id="jsonFileInput" class="hidden" type="file" accept=".json,application/json" onchange="importJsonFile(event)"><div class="actions"><button class="secondary" onclick="document.getElementById('jsonFileInput').click()">JSON 파일 선택</button><button class="secondary" onclick="exportJ()">데이터 백업 복사</button></div>`; window.scrollTo(0,0) }'''
if old_data not in html:
    raise SystemExit('dataPage target not found')
html = html.replace(old_data, new_data, 1)

old_import = '''function importJ(){let t=prompt('기업 분석 데이터를 붙여넣으세요.');if(!t)return;try{let x=JSON.parse(t);const list=Array.isArray(x)?x:[x];for(let item of list.reverse()){item.id=item.id||'id'+Date.now()+Math.random().toString(16).slice(2);a.unshift(item)}save();alert('가져오기가 완료되었습니다.');dataPage(true)}catch(_){alert('데이터 형식을 확인하세요.')}}'''
new_import = '''function mergeImportedData(x){const list=Array.isArray(x)?x:[x];let count=0;for(const raw of list){if(!raw||typeof raw!=='object'||Array.isArray(raw))continue;const item={...raw};item.id=item.id||'id'+Date.now()+Math.random().toString(16).slice(2);const i=a.findIndex(v=>v.id===item.id);if(i>=0)a[i]=item;else a.unshift(item);count++}if(!count)throw new Error('no valid company');save();alert(count+'개 기업을 가져왔습니다.');dataPage(true)} function importJsonFile(ev){const input=ev&&ev.target;const file=input&&input.files&&input.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{mergeImportedData(JSON.parse(String(reader.result||'')))}catch(_){alert('JSON 파일 형식을 확인하세요.')}};reader.onerror=()=>alert('파일을 읽을 수 없습니다.');reader.readAsText(file,'UTF-8');} function importJ(){let t=prompt('기업 분석 데이터를 붙여넣으세요.');if(!t)return;try{mergeImportedData(JSON.parse(t))}catch(_){alert('데이터 형식을 확인하세요.')}}'''
if old_import not in html:
    raise SystemExit('importJ target not found')
html = html.replace(old_import, new_import, 1)

index.write_text(html, encoding='utf-8')

java = Path('app/src/main/java/com/example/jobtrack/MainActivity.java')
j = java.read_text(encoding='utf-8')

j = j.replace('import android.webkit.WebSettings;\n', 'import android.webkit.WebSettings;\nimport android.webkit.WebChromeClient;\nimport android.webkit.ValueCallback;\n')
j = j.replace('    private WebView webView;\n', '    private WebView webView;\n    private ValueCallback<Uri[]> filePathCallback;\n    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;\n')

needle = '''        webView.setWebViewClient(new WebViewClient() {'''
chrome = '''        webView.setWebChromeClient(new WebChromeClient() {\n            @Override\n            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {\n                if (MainActivity.this.filePathCallback != null) {\n                    MainActivity.this.filePathCallback.onReceiveValue(null);\n                }\n                MainActivity.this.filePathCallback = filePathCallback;\n                Intent intent;\n                try {\n                    intent = fileChooserParams.createIntent();\n                    intent.setType("application/json");\n                    intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"application/json", "text/json", "text/plain"});\n                    startActivityForResult(Intent.createChooser(intent, "JSON 파일 선택"), FILE_CHOOSER_REQUEST_CODE);\n                } catch (Exception e) {\n                    MainActivity.this.filePathCallback = null;\n                    return false;\n                }\n                return true;\n            }\n        });\n\n        webView.setWebViewClient(new WebViewClient() {'''
if needle not in j:
    raise SystemExit('WebViewClient insertion target not found')
j = j.replace(needle, chrome, 1)

back_needle = '''    @Override\n    @SuppressWarnings("deprecation")\n    public void onBackPressed() {'''
on_result = '''    @Override\n    protected void onActivityResult(int requestCode, int resultCode, Intent data) {\n        if (requestCode == FILE_CHOOSER_REQUEST_CODE) {\n            Uri[] result = null;\n            if (resultCode == RESULT_OK && data != null) {\n                if (data.getClipData() != null) {\n                    int count = data.getClipData().getItemCount();\n                    result = new Uri[count];\n                    for (int i = 0; i < count; i++) result[i] = data.getClipData().getItemAt(i).getUri();\n                } else if (data.getData() != null) {\n                    result = new Uri[]{data.getData()};\n                }\n            }\n            if (filePathCallback != null) {\n                filePathCallback.onReceiveValue(result);\n                filePathCallback = null;\n            }\n            return;\n        }\n        super.onActivityResult(requestCode, resultCode, data);\n    }\n\n    @Override\n    @SuppressWarnings("deprecation")\n    public void onBackPressed() {'''
if back_needle not in j:
    raise SystemExit('onBackPressed target not found')
j = j.replace(back_needle, on_result, 1)
java.write_text(j, encoding='utf-8')

gradle = Path('app/build.gradle')
g = gradle.read_text(encoding='utf-8')
g = g.replace("versionCode 4", "versionCode 5", 1)
g = g.replace("versionName '1.3'", "versionName '1.4'", 1)
gradle.write_text(g, encoding='utf-8')

print('Applied JOB_Track v1.4 patch')
