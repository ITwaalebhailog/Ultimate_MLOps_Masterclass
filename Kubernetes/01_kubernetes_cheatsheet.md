# Kubernetes Cheat Sheet

Kubernetes is used to **orchestrate containerized applications**.

---

# 1. Cluster Information

Check cluster info

~~~bash
kubectl cluster-info
~~~

Check nodes

~~~bash
kubectl get nodes
~~~

---

# 2. Pods

List pods

~~~bash
kubectl get pods
~~~

Describe pod

~~~bash
kubectl describe pod pod_name
~~~

Delete pod

~~~bash
kubectl delete pod pod_name
~~~

View logs

~~~bash
kubectl logs pod_name
~~~

Execute command inside pod

~~~bash
kubectl exec -it pod_name -- bash
~~~

---

# 3. Deployments

Create deployment

~~~bash
kubectl create deployment nginx --image=nginx
~~~

List deployments

~~~bash
kubectl get deployments
~~~

Scale deployment

~~~bash
kubectl scale deployment nginx --replicas=3
~~~

Update image

~~~bash
kubectl set image deployment/nginx nginx=nginx:1.25
~~~

Delete deployment

~~~bash
kubectl delete deployment nginx
~~~

---

# 4. Services

List services

~~~bash
kubectl get svc
~~~

Expose deployment

~~~bash
kubectl expose deployment nginx --port=80 --type=NodePort
~~~

---

# 5. Namespaces

List namespaces

~~~bash
kubectl get namespaces
~~~

Create namespace

~~~bash
kubectl create namespace dev
~~~

Run pod in namespace

~~~bash
kubectl get pods -n dev
~~~

---

# 6. ConfigMaps and Secrets

Create configmap

~~~bash
kubectl create configmap app-config --from-file=config.properties
~~~

Create secret

~~~bash
kubectl create secret generic db-secret --from-literal=password=123
~~~

---

# 7. Apply YAML

Apply configuration

~~~bash
kubectl apply -f deployment.yaml
~~~

Delete resource

~~~bash
kubectl delete -f deployment.yaml
~~~
