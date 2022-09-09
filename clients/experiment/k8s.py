import time

from kubernetes import client, config
from kubernetes.client import V1Deployment, V1ObjectMeta, V1DeploymentSpec, V1LabelSelector, V1PodTemplateSpec, \
    V1PodSpec, V1Toleration, V1Container, V1EnvFromSource, V1ConfigMapEnvSource


def start_telemd_kubernetes_adapter() -> V1Deployment:
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.AppsV1Api()
    image = 'edgerun/telemd-kubernetes-adapter:0.1.18'
    return v1.create_namespaced_deployment(pretty=True, namespace='default',
                                           body=V1Deployment(
                                               api_version='apps/v1',
                                               kind='Deployment',
                                               metadata=V1ObjectMeta(name='telemd-kubernetes-adapter'),
                                               spec=V1DeploymentSpec(
                                                   replicas=1,
                                                   selector=V1LabelSelector(match_labels={
                                                       'app': 'telemd-kubernetes-adapter'
                                                   }),
                                                   template=V1PodTemplateSpec(
                                                       metadata=V1ObjectMeta(
                                                           labels={'app': 'telemd-kubernetes-adapter'}),
                                                       spec=V1PodSpec(
                                                           tolerations=[
                                                               V1Toleration(
                                                                   key='node-role.kubernetes.io/master',
                                                                   operator='Exists',
                                                                   effect='NoSchedule'
                                                               )
                                                           ],
                                                           node_selector={
                                                               'kubernetes.io/hostname': 'eb-k3s-master'
                                                           },
                                                           containers=[
                                                               V1Container(
                                                                   name='telemd-kubernetes-adapter',
                                                                   image=image,
                                                                   env_from=[
                                                                       V1EnvFromSource(
                                                                           config_map_ref=
                                                                           V1ConfigMapEnvSource(
                                                                               name='telemd-kubernetes-adapter-config'
                                                                           )
                                                                       )
                                                                   ]
                                                               )
                                                           ]
                                                       )
                                                   ),
                                               ),
                                           ))


def stop_telemd_kubernetes_adapter():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.AppsV1Api()
    v1.delete_namespaced_deployment(name='telemd-kubernetes-adapter', namespace='default')


if __name__ == '__main__':
    print('start telemd kubernetes adapter')
    start_telemd_kubernetes_adapter()
    print('wait 20 seconds')
    time.sleep(20)
    print('stop telemd kubernetes adapter')
    stop_telemd_kubernetes_adapter()
