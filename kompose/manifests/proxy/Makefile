.PHONY: destroy
destroy:         ## kubectl apply changes from manifest file
	@kubectl delete -f proxy-service.yaml,proxy-deployment.yaml,proxy-data-persistentvolumeclaim.yaml

.PHONY: apply
apply:         ## kubectl apply changes from manifest file
	@kubectl apply -f proxy-service.yaml,proxy-deployment.yaml,proxy-data-persistentvolumeclaim.yaml

.PHONY: watch
watch:         ## kubectl watch pod build up, ctrl+c to exit
	@kubectl get pods --watch

.PHONY: get
get:         ## kubectl get service, pod
	@kubectl get svc,pods