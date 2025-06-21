# app.py - Flask entry point

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from concurrent.futures import ThreadPoolExecutor
import os
import uuid
from cfd import solve_flow
from utils import arrays_to_csv

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=2)
progress_dict = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_cfd():
    # Extract form data and validate
    nx = int(request.form['nx'])
    ny = int(request.form['ny'])
    nu = float(request.form['nu'])
    u_in = float(request.form['uin'])
    p_out = float(request.form['pout'])
    n_steps = int(request.form['nsteps'])
    job_id = str(uuid.uuid4())
    progress_dict[job_id] = 0
    executor.submit(execute_cfd, nx, ny, nu, u_in, p_out, n_steps, job_id)
    return redirect(url_for('progress_page', job_id=job_id))

@app.route('/progress/<job_id>')
def progress(job_id):
    progress = progress_dict.get(job_id, 100)
    message = f"Running {progress}/100"
    return jsonify({'ratio': progress / 100, 'message': message})

@app.route('/status/<job_id>')          # ← progress 用 HTML
def progress_page(job_id):
    return render_template('progress.html', job_id=job_id)

@app.route('/result/<job_id>')
def result(job_id):
    # Display results
    return render_template('result.html', job_id=job_id)

@app.route('/download/<job_id>')
def download(job_id):
    file_path = f'static/outputs/{job_id}/cfd_result_{job_id}.csv'
    if not os.path.exists(file_path):
        return "File not ready. Try again later.", 404
    return send_file(file_path, as_attachment=True)

def execute_cfd(nx, ny, nu, u_in, p_out, n_steps, job_id):
    try:
        # 進捗 5 % にしておく
        progress_dict[job_id] = 5
        result = solve_flow(nx, ny, nu, u_in, p_out, n_steps)
        arrays_to_csv(result['u'], result['v'], result['p'], f'static/outputs/{job_id}/cfd_result_{job_id}.csv')
        progress_dict[job_id] = 100
    except Exception as e:
        progress_dict[job_id] = -1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50484)