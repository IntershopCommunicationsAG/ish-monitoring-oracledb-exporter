# Prometheus Oracle Exporter

* Installs prometheus [oracle exporter](https://dev.azure.com/ishcloudops/ish-monitoring/_git/ish-monitoring-oracledb-exporter)

## TL;DR;

```console
$ helm install ish-monitoring-oracledb-exporter
```

## Introduction

This chart bootstraps a prometheus [oracle exporter](https://dev.azure.com/ishcloudops/ish-monitoring/_git/ish-monitoring-oracledb-exporter) deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

## Installing the Chart

To install the chart with the release name `my-release`:

```console
$ helm install --name my-release ish-monitoring-oracledb-exporter
```

The command deploys oracle exporter on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```console
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the oracle Exporter chart and their default values.

| Parameter                       | Description                                | Default                                                    |
| ------------------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| `image`                         | Image                                      | `ishcloudopsicp.azurecr.io/intershop/ish-monitoring-oracledb-exporter`                      |
| `imageTag`                      | Image tag                                  | `latest`                                      |
| `imagePullPolicy`               | Image pull policy                          | `IfNotPresent` |
| `service.annotations`           | annotations for the service                | `{}`           |
| `service.type`      | Service type |  `ClusterIP` |
| `service.port`                      | The service port                               | `8000`                                     |
| `service.targetPort`                      | The target port of the container                               | `8000`                                        |
| `service.name`                  | Name of the service port                   | `http`                                                     |
| `service.labels`                | Labels to add to the service               | `{}`                                                       |
| `serviceMonitor.enabled`          | Use servicemonitor from prometheus operator                             | `false`                     |
| `serviceMonitor.namespace`        | Namespace thes Servicemonitor  is installed in                          |                             |
| `serviceMonitor.interval`         | How frequently Prometheus should scrape                                 |                             |
| `serviceMonitor.telemetryPath`    | path to cloudwatch-exporter telemtery-path                              |                             |
| `serviceMonitor.labels`           | labels for the ServiceMonitor passed to Prometheus Operator             | `{}`                        |
| `serviceMonitor.timeout`          | Timeout after which the scrape is ended                                 |                             |
| `resources`          |                                  |                    `{}`                                  |
| `oracle`                 | Oracle datasource configuration                      |  see [values.yaml](values.yaml)              |
| `flask.config`                 | flask configuration                      |  see [values.yaml](values.yaml)              |
| `collectMetricsIntervalSec`                 | metrics gathering interval                      | `15` |
| `rbac.create`                   | Specifies whether RBAC resources should be created.| `true` |
| `rbac.pspEnabled`               | Specifies whether a PodSecurityPolicy should be created.| `true` |
| `serviceAccount.create`         | Specifies whether a service account should be created.| `true` |
| `serviceAccount.name`           | Name of the service account.|        |
| `tolerations`                   | Add tolerations                            | `[]`  |
| `nodeSelector`                    | node labels for pod assignment | `{}`  |
| `affinity`                       |     node/pod affinities | `{}` |
| `annotations`                    | Deployment annotations | `{}` |
| `podLabels`                      | Additional labels to add to each pod      | `{}` |
| `extraContainers`                | Additional sidecar containers | `""` |
| `extraVolumes`                   | Additional volumes for use in extraContainers | `""` |
| `securityContext`                | Security options the pod should run with. [More info](https://kubernetes.io/docs/concepts/policy/security-context/) | `{}` |


Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```console
$ helm install --name my-release \
  --set serviceAccount.name=oracle  \
    ish-monitoring-oracledb-exporter
```

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example,

```console
$ helm install --name my-release -f values.yaml ish-monitoring-oracledb-exporter
```
