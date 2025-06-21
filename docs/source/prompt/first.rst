初回プロンプト
=============

| Openhandsへの指示分はChatGPTで生成した。
| 使用し他モデルはChatGPTo3。
| 最初のプロンプトは以下の通り。

.. code-block:: text
   :linenos:

   指示書 ― Flask 2D CFD アプリ生成

   1. ゴール
   --------
   ブラウザでフォームを開き、以下の境界条件を入力できる。

   流入速度          U_in  [m/s]
   流出圧力          p_out [Pa]
   動粘性係数        ν     [m²/s]
   計算格子数        N_x, N_y （最大 200×200）
   計算ステップ数    n_steps（最大 5 000）

   「解析実行」ボタンを押すとサーバ側で 2 次元非圧縮性 Navier-Stokes
   （MAC 法の簡易版）を有限差分で計算。

   処理完了後に
     • 速度場（u, v）のカラーコンター & ベクトル図
     • 圧力場のカラーコンター
     • ダウンロード用 CSV（x, y, u, v, p）
   を表示・提供する。

   2. 技術スタック
   ---------------
   Python 3.11 + Flask 3.0
   数値計算 : NumPy・Numba（JIT で高速化）
   可視化   : Plotly（静的 HTML に埋め込む）
   バックグラウンド実行 : ThreadPoolExecutor でノンブロッキング
   依存パッケージは requirements.txt に明記。

   3. ディレクトリ構成
   ------------------
   cfd_app/
   ├── app.py                # Flask エントリ
   ├── cfd.py                # 2D CFD ソルバー & ユーティリティ
   ├── templates/
   │   ├── index.html        # 入力フォーム
   │   └── result.html       # 結果ページ
   ├── static/
   │   └── style.css         # 最小限のデザイン
   ├── tests/
   │   └── test_solver.py    # PyTest 用 収束・物理量保存テスト
   ├── Dockerfile            # 本番デプロイ用
   ├── requirements.txt
   └── README.md

   4. 実装要件
   -----------
   cfd.py
     • solve_cavity(nx, ny, Re, n_steps) -> dict[str, np.ndarray] のインターフェース
     • ループは Numba @njit(parallel=True) で加速
     • 収束確認（最大残差 <1e-4）をログ出力

   app.py
     • GET /           → 入力フォーム
     • POST /run       → 非同期で CFD 実行し /result/<job_id> へリダイレクト
     • 大規模入力や異常値は HTTP 400
     • 実行中は JavaScript fetch + /progress API でプログレスバー表示

   HTML / CSS
     • Bootstrap 5 CDN
     • フォームは form-floating
     • 結果ページは Plotly グラフ 2 枚を d-flex gap-3 で横並び

   テスト
     • 格子 50×50, Re=100 のキャビティで定常計算
     • 中心渦の u = −0.05 ± 0.02 を確認

   Dockerfile（抜粋）
     FROM python:3.11-slim
     WORKDIR /app
     COPY . .
     RUN pip install -r requirements.txt
     EXPOSE 3000
     CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]

   5. 追加仕様
   -----------
   • 結果 PNG を /static/outputs/<job_id>/ に自動保存  
   • ジョブ履歴を SQLite で保持し再閲覧可  
   • 限界時間 30 s 超で解像度を半分に落として継続しユーザーに通知  
   • 生成物は MIT ライセンス。型ヒント・Google-style docstring・
     日本語コメント付きで可読性を確保