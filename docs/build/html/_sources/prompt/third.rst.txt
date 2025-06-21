返答プロンプト②
=============

２回目のプロンプトを参考にしばらく開発を行ったのち、
次のようなメッセージが返ってきた。

.. code-block:: text
    :linenos:

    変更内容
    ユーティリティ関数

    utils.py を新規作成し、速度・圧力配列を CSV に保存する arrays_to_csv 関数を実装しました。

    ドキュメント

    README.md を更新し、API 仕様表と 「Known Issues / Future Roadmap」 セクションを追加しました。

    次のステップ
    テスト

    tests/test_solver.py にテストケースを実装し、ソルバーの動作を検証してください。

    フロントエンド強化

    HTML テンプレートで Plotly を用いたクライアント側バリデーションと可視化を実装してください。

    テストやフロントエンドの強化について、さらにサポートが必要な場合はお知らせください！

メッセージに対し、以下の通りChatGPTに追加の指示文を生成させた。

.. code-block:: text
    :linenos:

    次の指示書 ― 実装フェーズ 2（テスト & フロントエンド強化）
    目的
    ユーザー体験を完成レベルへ引き上げる。
    具体的には自動テスト整備・可視化・入力バリデーション・進捗 UI を実装し、ワンクリックで解析→可視化→CSV 取得まで完結させる。

    1. tests/test_solver.py ― 単体テスト実装
    #	内容	詳細
    1	基準ケース	solve_flow(50, 50, ν=1e-3, u_in=1.0, p_out=0.0, n_steps=2000) を実行し、平均速度 u.mean() が 0.02±0.02 内であることを np.isclose で検証。
    2	残差収束	solve_flow(..., n_steps=400) の info["max_residual"] が 1e-3 未満になることを確認。
    3	エッジケース	極端に小さい格子 (10×10) や上限格子 (200×200) がエラーなく返ることを確認。
    4	PyTest 実行速度	合計実行時間 < 60 s。CI 用に pytest -q でパスすること。

    ヒント: テスト実行時は NUMBA_DISABLE_JIT=1 を環境変数にセットし、JIT を無効化して高速に実行。

    2. app.py ― 進捗 API & ダウンロード機能
    進捗 API

    python
    -----
    @app.get("/progress/<job_id>")
    def progress(job_id):
        return {"ratio": 0.0-1.0, "message": "Running n/total"}
    -----
    CSV ダウンロード

    ・/download/<job_id> で arrays_to_csv が書き出したファイルを send_file で返す。
    ・ファイル名は cfd_result_<job_id>.csv とする。

    3. HTML テンプレート強化
    templates/index.html

    ・Bootstrap5 + form-floating のまま、以下属性を追加：

    html
    -----
    <input name="nx" type="number" min="10" max="200" step="10" required>
    -----
    ・JS (vanilla) で 即時バリデーション。不正入力時は is-invalid を付与。

    templates/result.html

    ・Plotly CDN を <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script> で読み込み。
    ・速度ベクトル: quiver 相当を Scattergl で。
    ・圧力コンター: Contour でカラーマップ Viridis。
    ・「CSV ダウンロード」ボタンと「トップへ戻る」リンクを配置。
    ・計算時間・格子サイズをフッターに表示。

    進捗バー

    ・progress.html を用意せず、index.html で fetch("/progress/...") を 1 s 間隔でポーリングし Bootstrap の progress bar を更新。
    ・100 % で location.href = "/result/<job_id>"。

    4. utils.py 連携
    ・arrays_to_csv(u, v, p, path) を /download エンドポイントで利用。
    ・計算完了時に自動で呼び出し、static/outputs/<job_id>/ へ保存するロジックを cfd.py または app.py へ組み込み。

    5. CI / Lint（オプション）
    ・requirements-dev.txt に

    nginx
    -----
    pytest
    flake8
    black
    isort
    -----
    を追記。

    ・pre-commit 設定例を .pre-commit-config.yaml に追加（任意）。

    納品物
    ・更新済みコード（テスト、テンプレート、app.py、utils.py 追記）。
    ・追加依存ファイル（requirements-dev.txt, .pre-commit-config.yaml）。
    ・README.md へ「テスト実行方法」「フロントエンド機能概要」を追記。

    以上