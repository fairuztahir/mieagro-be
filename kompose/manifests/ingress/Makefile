
.PHONY: apply-ing-ctrl
apply-ing-ctrl:
	@kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.43.0/deploy/static/provider/do/deploy.yaml

.PHONY: destroy-ing-ctrl
destroy-ing-ctrl:
	@kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.43.0/deploy/static/provider/do/deploy.yaml

.PHONY: apply
apply:
	@kubectl apply -f ingress.yaml

.PHONY: destroy
destroy:
	@kubectl delete -f ingress.yaml

.PHONY: apply-default
apply-default:
	@kubectl apply -f service.yaml

.PHONY: destroy-default
destroy-default:
	@kubectl delete -f service.yaml