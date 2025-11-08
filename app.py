from flask import Flask, request, render_template
import os
import json
import time

from utils.static_analysis import analyze_code
from utils.feature_extract import metrics_to_features, load_or_train_model


app = Flask(__name__)

# Disable caching in development mode
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Add cache-busting context processor
@app.context_processor
def inject_cache_bust():
    return dict(cache_bust=int(time.time()))


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
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'model', 'defect_model.pkl')
            model, model_name = load_or_train_model(model_path)

            # 3) Predict
            y_pred = model.predict(X)[0]
            is_defective = bool(int(y_pred))

            result = {
                'is_defective': is_defective,
                'metrics_json': json.dumps(metrics, indent=2),
                'model_name': model_name,
            }

    return render_template('index.html', result=result)


if __name__ == '__main__':
    # Run the Flask development server
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("Starting Flask Server...")
    print("="*60)
    print(f"\nServer running at: http://127.0.0.1:{port}")
    print(f"Press Ctrl+C to stop the server\n")
    app.run(host='127.0.0.1', port=port, debug=True)


