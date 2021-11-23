.PHONY: help
all:           ## View kube configuration
	@kubectl config view

.PHONY: help
help:          ## Show command list
	@echo usage:
	@echo       make [ target ] [ optional ]
	@echo ``
	@echo optional:
	@echo       env=[ environment ]
	@echo       c=[ command ]
	@echo ``
	@echo target:
	@echo ``
	@awk '/^[a-zA-Z0-9\-_+. ]*:[a-zA-Z0-9\-_+. ]*#{2}/ { print; }' $(MAKEFILE_LIST)

.PHONY: convert
convert:       ## kompose create manifest file
	@kompose -f docker-compose.yml convert -o kubemanifests.yaml

.PHONY: create
create:        ## kubectl create from manifest file
	@kubectl create -f kubemanifests.yaml,secret.yaml
.PHONY: apply
apply:         ## kubectl apply changes from manifest file
	@kubectl apply -f kubemanifests.yaml,secret.yaml

.PHONY: pods
pods:          ## List of pods running with c=<pod_name>
	@kubectl get pods $(c)

.PHONY: desc
desc:          ## Description of pods running with c=<pod_name>
	@kubectl describe pods $(c)

.PHONY: logs
logs:          ## Display log file with c=<pod_name>
	@kubectl logs $(c)

.PHONY: svc
svc:           ## List of services with c=<pod_name>
	@kubectl get svc $(c)

.PHONY: pvc
pvc:           ## List of persistent volume claim with c=<pod_name>
	@kubectl get pvc $(c)

.PHONY: events
events:        ## Get list of events inside service with c=<pod_name>
	@kubectl get events $(c)

.PHONY: deploy
deploy:        ## Get deployment list with c=<pod_name>
	@kubectl get deployments $(c)

.PHONY: del-svc
del-svc:       ## Delete all kube services
	@kubectl delete service --all

.PHONY: del-deploy
del-deploy:    ## Delete all kube services
	@kubectl delete deployment --all

.PHONY: del-pvc
del-pvc:       ## Delete all kube persistent volume claim
	@kubectl delete pvc --all
.PHONY: destroy
destroy:       ## Destroy all kube service, deployment and persistent volumes
	@kubectl delete service --all
	@kubectl delete deployment --all
	@kubectl delete pvc --all

# .PHONY: create
# create:        ## kubectl create from manifest file
# 	@kubectl create -f db-service.yaml,db-deployment.yaml,db-data-persistentvolumeclaim.yaml, \
# 	goredis-service.yaml,goredis-deployment.yaml, \
# 	api-service.yaml,api-deployment.yaml,api-data-persistentvolumeclaim.yaml,tmp-persistentvolumeclaim.yaml, \
# 	web-service.yaml,web-deployment.yaml,web-data-persistentvolumeclaim.yaml,node-modules-persistentvolumeclaim.yaml, \
# 	pgadmin-service.yaml,pgadmin-deployment.yaml, \
# 	proxy-service.yaml,proxy-deployment.yaml,proxy-data-persistentvolumeclaim.yaml, \
# 	webnet-networkpolicy.yaml,secret.yaml

# # .PHONY: create-db
# # create-db:     ## kubectl create database from manifest file
# # 	@kubectl create -f manifetsts/db-service.yaml,manifetsts/db-deployment.yaml,manifetsts/db-data-persistentvolumeclaim.yaml,manifetsts/secret.yaml
# .PHONY: create-redis
# create-redis:  ## kubectl create redis from manifest file
# 	@kubectl create -f manifetsts/goredis-service.yaml,manifetsts/goredis-deployment.yaml
# .PHONY: create-pg
# create-pg:  ## kubectl create pgadmin from manifest file
# 	@kubectl create -f manifetsts/pgadmin-service.yaml,manifetsts/pgadmin-deployment.yaml
# .PHONY: create-api
# create-api:  ## kubectl create api from manifest file
# 	@kubectl create -f manifetsts/api-service.yaml,manifetsts/api-deployment.yaml,manifetsts/api-data-persistentvolumeclaim.yaml,manifetsts/tmp-persistentvolumeclaim.yaml
# .PHONY: create-web
# create-web:  ## kubectl create web from manifest file
# 	@kubectl create -f manifetsts/web-service.yaml,manifetsts/web-deployment.yaml,manifetsts/web-data-persistentvolumeclaim.yaml,manifetsts/node-modules-persistentvolumeclaim.yaml
# .PHONY: create-proxy
# create-proxy:  ## kubectl create proxy from manifest file
# 	@kubectl create -f manifetsts/proxy-service.yaml,manifetsts/proxy-deployment.yaml,manifetsts/proxy-data-persistentvolumeclaim.yaml
# # .PHONY: create-ingress
# # create-ingress:  ## kubectl create ingress from manifest file
# # 	@kubectl create -f manifetsts/kube-ingress.yaml