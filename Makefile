.PHONY: build-backend build-frontend deploy

build-backend:
	docker build -t metricboost:0.1.0 .
	docker save -o images/metricboost.0.1.0.tar metricboost:0.1.0

build-frontend:
	cd frontend && pnpm run build

deploy: build-backend build-frontend
	@echo "Deployment complete"