# Kubernetes resources for kmom05

Apply with:

```bash
kubectl apply -f kubernetes/andreas/00-namespace.yml
kubectl apply -f kubernetes/andreas/01-clusterissuers.yml
kubectl apply -f kubernetes/andreas/02-app-secrets.yml
kubectl apply -f kubernetes/andreas/03-mysql.yml
kubectl apply -f kubernetes/andreas/04-microblog.yml
kubectl apply -f kubernetes/andreas/05-hpa.yml
```

Or with kustomize:

```bash
kubectl apply -k kubernetes/andreas
```
