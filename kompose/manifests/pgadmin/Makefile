.PHONY: destroy
destroy:     ## kubectl apply changes from manifest file
	@kubectl delete -f pgadmin-service.yaml,pgadmin-deployment.yaml,pgadmin-secret.yaml

.PHONY: apply
apply:       ## kubectl apply changes from manifest file
	@kubectl apply -f pgadmin-service.yaml,pgadmin-deployment.yaml,pgadmin-secret.yaml

.PHONY: watch
watch:       ## kubectl watch pod build up, ctrl+c to exit
	@kubectl get pods --watch

.PHONY: get
get:         ## kubectl get service, pod
	@kubectl get svc,pods