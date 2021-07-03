# Cloud infrastructure for the weather server components

This project is providing the infrastructure as-code in Google Cloud Platform (GCP) for the weather server
components. The infrastructure is automatically deployed by GitLab CI/CD using Terraform.

# Seed project

The infrastructure will be deployed into a separate GCP-project, it needs however a service account that has all
required permissions. It should be provided in a separate *seed project* in GCP.

Create a service account such as `terraform@seed-project-123356.iam.gserviceaccount.com` in this project and assign it
the following roles:

* `Cloud SQL Admin`
* `Editor`
* `Cloud Run Admin`
* `Storage Admin`
* `Viewer`

The *seed project* requires the same APIs being activated as the project running the server components. These are:

* `secretmanager.googleapis.com`
* `containerregistry.googleapis.com`
* `run.googleapis.com`
* `sqladmin.googleapis.com`

## Usage

By committing to *branches* or *tags* of this repository, the infrastructure is deployed to the *testing project* in
GCP. If committing to the *main branch*, the infrastructure of the *production project* is deployed.

The infrastructure-as-code description is providing the complete infrastructure required by the weather server
components. They can be deployed directly in these projects using the GitLab CI/CD of their subproject.

## Destruction of the testing infrastructure

The *testing infrastructure* can only be destructed by running the respective job in its pipeline.

## Required GitLab CI/CD variables

A number of variables need to be defined to configure the CI/CD pipeline:

| Variable                           | Example value             | Description                         |
|------------------------------------|---------------------------|-------------------------------------| 
| **GCP_PROJECT_ID_PRODUCTION**      | weather-production-123456 | the GCP production project ID       |
| **GCP_PROJECT_ID_TESTING**         | weather-testing-123456    | the GCP testing project ID          |
| **GOOGLE_APPLICATION_CREDENTIALS** | a JSON object             | the GCP service account credentials |
| **TF_VAR_GCP_DATABASE_TIER**       | db-f1-micro               | the SQL database machine type       |
| **TF_VAR_GCP_DATABASE_VERSION**    | POSTGRES_13               | the SQL database version            |
| **GCP_REGION_ID**                  | europe-west3              | the GCP region of deployment        |
| **TF_VAR_GCP_SQL_BACKUP_REGION**   | eu                        | the GCP SQL backup region           |
