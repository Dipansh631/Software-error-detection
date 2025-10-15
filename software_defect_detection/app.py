from flask import Flask, request, render_template_string
import os
import json

from utils.static_analysis import analyze_code
from utils.feature_extract import metrics_to_features, load_or_train_model


app = Flask(__name__)


PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>🔍 Software Defect Detection System</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; color: #1a1a1a; }
      .container { max-width: 860px; margin: 0 auto; }
      h1 { font-size: 1.8rem; }
      .card { border: 1px solid #e5e5e5; border-radius: 8px; padding: 1rem 1.25rem; margin-top: 1rem; }
      .btn { display: inline-block; background: #2f6feb; color: white; padding: 0.6rem 1rem; border-radius: 6px; border: none; cursor: pointer; }
      .btn:disabled { background: #9fb4f2; cursor: not-allowed; }
      .muted { color: #666; font-size: 0.95rem; }
      pre { background: #fafafa; padding: 1rem; border-radius: 6px; overflow-x: auto; }
      .result { font-size: 1.2rem; margin-top: 0.5rem; }
      .ok { color: #157347; }
      .bad { color: #b42318; }
      .footer { margin-top: 2rem; color: #666; font-size: 0.9rem; }
      input[type="file"] { margin: 0.5rem 0 1rem; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>🔍 Software Defect Detection System</h1>
      <p class="muted">Upload a source code file and click Analyze to run static analysis and a machine learning prediction.</p>

      <div class="card">
        <form method="POST" enctype="multipart/form-data">
          <label for="codefile"><strong>Source Code File</strong></label><br/>
          <input id="codefile" name="codefile" type="file" accept=".py,.txt,.java,.js,.cpp,.c,.cs,.rb,.go,.ts" required />
          <br/>
          <button class="btn" type="submit">Analyze Code</button>
        </form>
      </div>

      {% if result %}
      <div class="card">
        <div><strong>Prediction</strong></div>
        <div class="result {{ 'bad' if result.is_defective else 'ok' }}">
          {% if result.is_defective %}⚠️ Defective{% else %}✅ Clean{% endif %}
        </div>
        <div class="muted">Model: {{ result.model_name }}</div>
      </div>

      <div class="card">
        <div><strong>Static Analysis Metrics</strong></div>
        <pre>{{ result.metrics_json }}</pre>
      </div>
      {% endif %}

      <div class="footer">Built with Flask + scikit-learn. Demo metrics only; not a substitute for full static analysis.</div>
    </div>
  </body>
</html>
"""


def _read_file_storage_to_text(file_storage) -> str:
    """Read an uploaded file (werkzeug FileStorage) into a UTF-8 string.

    Tries utf-8 first, then latin-1 as a fallback to avoid hard failures on odd encodings.
    """
    raw = file_storage.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="ignore")


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        uploaded = request.files.get('codefile')
        if uploaded and uploaded.filename:
            code_text = _read_file_storage_to_text(uploaded)

            # 1) Static analysis
            metrics = analyze_code(code_text)

            # 2) Features and model
            X = metrics_to_features(metrics)
            model, model_name = load_or_train_model(os.path.join('software_defect_detection', 'model', 'defect_model.pkl'))

            # 3) Predict
            y_pred = model.predict(X)[0]
            is_defective = bool(int(y_pred))

            result = {
                'is_defective': is_defective,
                'metrics_json': json.dumps(metrics, indent=2),
                'model_name': model_name,
            }

    return render_template_string(PAGE_TEMPLATE, result=result)


if __name__ == '__main__':
    # Run the Flask development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


