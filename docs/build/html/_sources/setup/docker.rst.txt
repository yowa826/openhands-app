Docker イメージのダウンロード
=============================

ここでは OpenHands 用 Docker コンテナを取得する。

#. Dockerエンジンを起動する::

#. ターミナルを開いて次を実行する::

.. code-block:: bash

    docker pull docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik

    docker run -it --rm --pull=always \
        -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik \
        -e LOG_ALL_EVENTS=true \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v ~/.openhands:/.openhands \
        -p 3000:3000 \
        --add-host host.docker.internal:host-gateway \
        --name openhands-app \
        docker.all-hands.dev/all-hands-ai/openhands:0.45