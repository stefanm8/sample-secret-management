# sample-secret-management
Example of managing secrets with sops, google kms, google iam and github actions

## Requirements

github secrets:
- GCP_PROJECT *get this from gcp console*
- GCP_KEY *obtained earlier, stored in /tmp/github-account-key.json*
- GCP_EMAIL *github-sample@<project>.iam.gserviceaccount.com*

## Setting up environment

1. Create keyring with KMS

```bash
gcloud kms keyrings create github-sops --location global
gcloud kms keys create sample-secret-key --location global --keyring github-sops --purpose encryption
gcloud kms keys list --location global --keyring github-sops
```

2. Encrypt/Decrypt secrets specifying project 
```bash
$ sops --encrypt --gcp-kms projects/<project_id>/locations/global/keyRings/github-sops/cryptoKeys/sample-secret-key env  > env.enc
$ sops --decrypt env.enc
```

3. Setting up service account

- Creating service account

```bash
gcloud iam service-accounts create github-sample \
    --description="github-sample" \
    --display-name="github-sample"
```


- Giving access
```bash
gcloud kms keys add-iam-policy-binding sample-secret-key \
    --keyring github-sops \
    --location global \
    --member serviceAccount:github-sample@<project>.iam.gserviceaccount.com \
    --role roles/cloudkms.cryptoKeyEncrypterDecrypter

```

- Obtaining key

```bash
gcloud iam service-accounts keys create /tmp/github-account-key.json \
  --iam-account github-sample@<project>.iam.gserviceaccount.com
```

4. Creating and encrypting secrets 

```bash
sops --encrypt --gcp-kms projects/<project>/locations/global/keyRings/github-sops/cryptoKeys/sops-key secrets/env > env.enc
rm secrets/env
```

5. Running
```bash
docker pull docker.io/stefanm88/sample-secret-management
docker run -d -p 8000:8000 docker.io/stefanm88/sample-secret-management
curl localhost:8000
    DB_USERNAME=secretdbusername
    DB_PASSWORD=secretdbpassword
```

