# Flower Helm Chart (`contrib/helm/flower`)

Chart разворачивает Flower из образа, собранного по `contrib/Dockerfile`, добавляет sidecar `fluent-bit` для сбора логов и подключает внешний dependency chart `kube-prometheus-stack` для сбора метрик.

## Сборка образа

```bash
docker build -f contrib/Dockerfile -t <registry>/flower-contrib:latest .
docker push <registry>/flower-contrib:latest
```

## Установка dependency и релиза

```bash
cd contrib/helm/flower
helm dependency update
helm upgrade --install flower . \
  --namespace monitoring \
  --create-namespace \
  --set image.repository=<registry>/flower-contrib \
  --set image.tag=latest \
  --set env[0].name=PORT --set env[0].value=5555 \
  --set env[1].name=CELERY_BROKER_URL --set env[1].value=redis://redis:6379/0
```

## Что включено

- `Deployment` с контейнерами:
  - `flower-app`
  - `fluent-bit` sidecar
- `Service` для UI и `/metrics`
- `ServiceMonitor` для Prometheus Operator (если CRD доступна)
- Внешний чарт `kube-prometheus-stack` как dependency

## Логи

`fluent-bit` sidecar читает `CRI`-логи контейнера `flower-app` через `hostPath` `/var/log/containers` и по умолчанию отправляет их в `stdout` sidecar-контейнера.

## Метрики

Flower метрики снимаются с `http://<service>:5555/metrics` через `ServiceMonitor`.
