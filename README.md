# ELT process - Spotify API Data

## Kubernetes
### How to Install 
> 1. Download the latest stable version at https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
> 2. Add the kubectl.exe on the path of enviroment variables

To facilitate the configuration of the cluster, I used **minikube**, which is a local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.
To download it, you will need:
> 1. 2 CPUs or more
> 2. 2GB of free memory
> 3. 20GB of free disk space
> 4. Internet connection
> 5. Container or virtual machine manager (in my case, I used Docker)

## Chocolatey
Chocolatey aims to automate the entire software lifecycle from install through upgrade and removal on Windows operating systems. 

### How to install
> 1. Open Windows Powershell as an administrator
> 2. Type the command:
``
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
``

## Kubectx e Kubens
- **kubectx** is a tool to switch between contexts (clusters) on kubectl faster.
- **kubens** is a tool to switch between Kubernetes namespaces (and configure them for kubectl) easily.
  
To install, you will need to have chocolatey installed as well. After that, just type ``choco install kubectlx`` and ``choco install kubens`` on powershell

## Helm

Helm helps you **manage** Kubernetes applications — Helm Charts help you define, install, and upgrade even the most complex Kubernetes application.

### How to install
`` choco install kubernetes-helm ``

## Commands used to create the minikube instance and configurate the airflow

-- First, we need to create our k8s cluster: ``minikube start``

-- Installing airflow on helm: ``helm repo add apache-airflow https://airflow.apache.org/``

-- Por padrão, o airflow aponta para o proprio diretorio de DAGs. Então precisamos *copiar* o pacote helm para a nossa máquina local, ao invés de baixá-lo diretamente para o cluster: 
```
helm pull apache-airflow/airflow
tar zxvf airflow-1.11.0.tgz
```

-- Toda vez que instala o helm, ele aponta para um arquivo values.yaml

-- No caso do airflow, no final do arquivo, na parte de ``gitSync``, ele aponta diretamente para o arquivo git do próprio airflow. 
Precisamos alterar essa parte, para que possamos criar nossas próprias DAGs.

-- Se tiver repositório privado: criar um arquivo encoding com **nome** e **token** do git, e atualizar o yaml com o seguinte comando: ``kubectl apply -f git-secret.yaml -n airflow``

-- Caso tenha helm rodando mas quer alterar alguns valores: ``helm upgrade --install airflow airflow``

-- Depois, executamos o seguinte comando: ``helm install airflow airflow -n airflow --create-namespace``

-- Check is the pods on the namespaces are ok ``k9s -n airflow``

-- Change the default namespace ``kubens airflow``

-- Access the airflow ``kubectl port-forward svc/airflow-webserver 8080:8080``
