REGISTRY_PATH := mmaugust
IMAGE_NAME := deprecation-exporter


.PHONY: $(IMAGE_NAME).image
$(IMAGE_NAME).image:
	docker build -t $(IMAGE_NAME):latest .
	
.PHONY: $(IMAGE_NAME).tag
$(IMAGE_NAME).tag:
	docker tag $(IMAGE_NAME):latest $(REGISTRY_PATH)/${IMAGE_NAME}:latest
	
.PHONY: $(IMAGE_NAME).push
$(IMAGE_NAME).push:
	docker push $(REGISTRY_PATH)/${IMAGE_NAME}:latest