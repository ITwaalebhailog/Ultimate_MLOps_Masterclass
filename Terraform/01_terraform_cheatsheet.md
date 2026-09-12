# Terraform Cheat Sheet

Terraform is used for **Infrastructure as Code (IaC)** to manage cloud infrastructure.

---

# 1. Terraform Basics

Check version

~~~bash
terraform version
~~~

Initialize project

~~~bash
terraform init
~~~

Validate configuration

~~~bash
terraform validate
~~~

Format code

~~~bash
terraform fmt
~~~

---

# 2. Terraform Workflow

Preview changes

~~~bash
terraform plan
~~~

Apply changes

~~~bash
terraform apply
~~~

Destroy infrastructure

~~~bash
terraform destroy
~~~

---

# 3. State Management

View state

~~~bash
terraform show
~~~

List resources

~~~bash
terraform state list
~~~

Remove resource from state

~~~bash
terraform state rm resource_name
~~~

---

# 4. Variables

Define variable

~~~hcl
variable "region" {
 default = "us-east-1"
}
~~~

Use variable

~~~hcl
provider "aws" {
 region = var.region
}
~~~

---

# 5. Outputs

~~~hcl
output "instance_ip" {
 value = aws_instance.web.public_ip
}
~~~

---

# 6. Modules

Call module

~~~hcl
module "vpc" {
 source = "./modules/vpc"
}
~~~

---

# 7. Terraform Providers

Example AWS provider

~~~hcl
provider "aws" {
 region = "us-east-1"
}
~~~

---

# 8. Useful Commands

Show graph

~~~bash
terraform graph
~~~

Refresh state

~~~bash
terraform refresh
~~~
