OpenHands を使ってみた感想
=========================

ChatGPTとOpenhandsを組み合わせて開発をした感想をまとめる。

.. rubric:: 良かった点

* 指示文を ChatGPT に生成させれば、アプリ開発の要件定義に必要な最低限の項目がもれなく洗い出せるため **バグが少なくなりやすい**。
* ページ遷移／リクエスト処理／HTML など “簡素だが最低限” の実装が得られるので **アプリ開発初心者向き**。
* Flask のメソッドをまったく知らなくてもアプリ開発が進められる。
* 一度にすべて開発するのではなく **細かい進捗を返してくる** ため、大幅に間違った完成物になりにくい。

.. rubric:: イマイチな点

* あくまで **最低限のアプリ**。アプリ開発上級者には向かない。
* **複雑なバックエンド** の自動生成は困難と思われる（ただし「ここに処理を書く」メモは出してくれる）。
* 多少なりとも **最初はバグが出る**。細部の調整は人間が行う必要がある。