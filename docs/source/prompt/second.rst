返答プロンプト①
=============

1回目のプロンプトを参考にしばらく開発を行ったのち、
次のようなメッセージが返ってきた。

.. code-block:: text
    :linenos:

    進捗概要
    ディレクトリ構成
    アプリに必要なフォルダとファイルを作成済み。

    作成済みファイル
    ファイル	役割
    app.py	Flask エントリポイント。基本ルーティングを設定。
    cfd.py	NumPy／Numba ベースの 2 次元 CFD ソルバーのプレースホルダー。
    templates/index.html	ユーザーが境界条件を入力する HTML フォーム。
    templates/result.html	解析結果表示用の HTML ページ。
    static/style.css	最小限のスタイルシート。
    tests/test_solver.py	CFD ソルバーを検証する PyTest ファイル。
    Dockerfile	Docker イメージビルド用ファイル。
    requirements.txt	依存パッケージ一覧。
    README.md	ローカル実行および Docker 実行の手順書。

    次のステップ
    cfd.py

    CFD ソルバー本体のロジックを実装する。

    app.py

    フォーム送信の受け取り、非同期実行、結果ページへの遷移を実装する。

    可視化

    Plotly で速度場・圧力場を描画できるように設定する。

    その他、具体的な作業や疑問点があればお気軽にお知らせください。

メッセージに対し、以下の通りChatGPTに追加の指示文を生成させた。

.. code-block:: text
    :linenos:

    次の指示書 ― 実装フェーズ 1
    目的
    最小構成から「動くプロトタイプ」へ。
    具体的には CFD ソルバー実装＋非同期実行＋可視化＋ダウンロード機能を仕上げる。

    1. cfd.py ― CFD ソルバー実装
    アルゴリズム

    ・2 次元非圧縮性 Navier-Stokes（速度‐圧力分割：MAC／SIMPLE‐like）。
    ・キャビティ流れを基本形とし、境界条件は全壁ノースリップをデフォルト、流入・流出はフォーム入力で上書き可。

    API

    python
    ------
    def solve_flow(nx: int, ny: int, nu: float,
                u_in: float, p_out: float,
                n_steps: int, ρ: float = 1.0) -> dict[str, np.ndarray]:
        """計算完了後に { 'u': u, 'v': v, 'p': p } を返す。"""
    ------

    高速化

    ・主要ループに @njit(parallel=True) を付与。
    ・nx * ny ≤ 40_000 で 30 s 以内を目標。

    テスト

    ・tests/test_solver.py に以下を実装：

    python
    ------
    res = solve_flow(50, 50, nu=1e-3, u_in=1.0, p_out=0.0, n_steps=2000)
    assert np.isclose(res["u"].mean(), 0.02, atol=0.02)
    ------
    ・GitHub Actions 相当の CI を想定し、テスト時間 < 60 s。

    2. app.py ― 非同期実行フロー
    エンドポイント

    Method	Path	役割
    GET	/	入力フォーム
    POST	/run	ジョブ登録 → /progress/<job_id> にリダイレクト
    GET	/progress/<job_id>	JSON で進捗％返却
    GET	/result/<job_id>	結果ページ
    GET	/download/<job_id>	CSV ダウンロード

    バックエンド

    ・ThreadPoolExecutor(max_workers=2) にジョブ投入。
    ・計算中は Python queue or dict で進捗を共有。
    ・タイムアウト 30 s 超えたら解像度を半分に落として続行し、ユーザーに警告メッセージ表示。

    3. テンプレート & フロントエンド
    index.html

    ・Bootstrap 5 + form-floating。
    ・JavaScript でクライアント側バリデーション（max=200 など）。

    result.html

    ・Plotly で
        ・速度ベクトル＋等値線 (subplot 左)
        ・圧力コンター (subplot 右)
    ・「CSV ダウンロード」ボタンを配置。

    /progress

    ・fetch API で 1 s ごとにポーリング → progress bar (aria-valuenow) 更新。

    4. 補助ユーティリティ
    utils.py を追加し、

    python
    -----
    def arrays_to_csv(u, v, p, fname) -> Path:
        ...
    -----
    ・完了後に /static/outputs/{job_id}/ へ PNG + CSV を保存。

    5. ドキュメント更新
    ・README.md に

        ・入力例スクリーンショット
        ・API 仕様表
        ・「known issues / 今後のロードマップ」節を追記。

    6. コーディング規約
    ・型ヒント必須、Google-style docstring、日本語コメント。
    ・flake8, black, isort を CI 推奨設定で追加（requirements-dev.txt に分離）。

    納品物
    ・更新済み code diff（すでに存在するファイルは上書き）。
    ・新規 utils.py。
    ・追加テスト & 依存ファイル。

    以上。