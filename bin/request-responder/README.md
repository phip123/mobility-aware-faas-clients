# Request Reponder Experiments

The experiments in this folder aim to execute only the Request Responder Experiments with different workloads and
parameters.
Prerequisites:
* KUBECONFIG/`kubectl` must be available in the running shell
* the **working directory** must be the *root directory of the repository*.

To execute a run (located in `runs`), execute:

    # wait for the request-responder deployment to be spawned
    # Only once
    ./bin/request-responder/bin/deploy.sh 

    # initializes the etcd storage for the load balancer, executes the given script and then removes all created pods
    # Repeat as needed/wanted
    ./bin/request-responder/run.sh ./bin/request-responder/runs/test.sh

    # tears down the origin deployment
    # Only once
    ./bin/request-responder/bin/teardown.sh