terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.8.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.1"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

resource "null_resource" "create_kind_cluster" {
  provisioner "local-exec" {
    command = "kind create cluster --config kind-config.yaml --name kind-cluster"
  }
}

resource "docker_image" "fastapi_image" {
  name         = "fastapi_test-web:latest"
  build {
    context    = "./"
    dockerfile = "Dockerfile"
  }
}

resource "null_resource" "load_docker_image" {
  depends_on = [null_resource.create_kind_cluster, docker_image.fastapi_image]

  provisioner "local-exec" {
    command = "kind load docker-image fastapi_test-web:latest --name kind-cluster"
  }
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "helm_release" "fastapi" {
  depends_on      = [null_resource.load_docker_image]
  name            = "fastapi-test"
  chart           = "./helm"
  namespace       = "fastapi"
  create_namespace = true

  values = [
    file("./helm/values.yaml"),
    jsonencode({
      database = {
        host     = "db"
        port     = "5432"
        name     = "fastapitest"
        user     = "postgres"
        password = "6526"
        image    = "postgres:15-alpine"
      },
      image = {
        repository = "fastapi_test-web"
        tag        = "latest"
        pullPolicy = "Never"
      }
    })
  ]
}

