# ELT process - Spotify API Data

## Kubernetes
### How to Install 
1. Download the latest stable version at https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
2. Add the kubectl.exe on the path of enviroment variables

To facilitate the configuration of the cluster, I used **minikube**, which is a local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.
To download it, you will need:
1. 2 CPUs or more
2. 2GB of free memory
3. 20GB of free disk space
4. Internet connection
5. Container or virtual machine manager (in my case, I used the windowns version of Docker)

## Chocolatey
Chocolatey aims to automate the entire software lifecycle from install through upgrade and removal on Windows operating systems. 
### How to install
1. Open Windows Powershell as an administrator
2. Type the command:

   2.1 Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

## Kubectx e Kubens
- A tool to switch between contexts (clusters) on kubectl faster
- To install, you will need to have chocolatey installed as well. After that, just type *choco install kubectlx* on powershell
- choco install kubens

## Helm
### How to install
1. *choco install helm*

## CREATE THE INSTANCES ON K8S

-- Creating our k8s cluster
minikube start

-- Setting up helm
choco install kubernetes-helm

-- Installing airflow on helm
helm repo add apache-airflow https://airflow.apache.org/
helm install my-airflow -n airflow apache-airflow/airflow --version 1.11.0 --create-namespace

-- Check is the pods on the namespaces are ok
k9s -n airflow

-- Change the default namespace
kubens airflow

-- Access the airflow
kubectl port-forward svc/airflow-webserver 8080:8080

-- Por padrão, o airflow aponta para o proprio diretorio de DAGs
helm pull apache-airflow/airflow
tar zxvf airflow-1.11.0.tgz

-- Toda vez que instala o helm, ele aponta para um arquivo values.yaml
-- Mudar no final do arquivo de values, na parte de git sync, para o nosso próprio repositório
