.PHONY: destroy
destroy:     ## kubectl apply changes from manifest file
	@kubectl delete -f api-deployment.yaml,api-service.yaml,api-data-persistentvolumeclaim.yaml,tmp-persistentvolumeclaim.yaml,api-secret.yaml

.PHONY: apply
apply:       ## kubectl apply changes from manifest file
	@kubectl apply -f api-deployment.yaml,api-service.yaml,api-data-persistentvolumeclaim.yaml,tmp-persistentvolumeclaim.yaml,api-secret.yaml

.PHONY: watch
watch:       ## kubectl watch pod build up, ctrl+c to exit
	@kubectl get pods --watch

.PHONY: get
get:         ## kubectl get service, pod
	@kubectl get svc,pods