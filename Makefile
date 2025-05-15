.PHONY: build-backend build-frontend deploy

build-backend:
	docker build -t metricboost:0.0.2 .
	docker save -o images/metricboost.0.0.2.tar metricboost:0.0.2

build-frontend:
	cd frontend && pnpm run build

deploy: build-backend build-frontend
	@echo "Deployment complete"