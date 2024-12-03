variable "db_instance_id" {
  description = "The ID of the RDS instance"
  type        = string
}

variable "db_username" {
  description = "The username for the RDS instance"
  type        = string
}

variable "db_password" {
  description = "The password for the RDS instance"
  type        = string
}

variable "db_name" {
  description = "The database name"
  type        = string
}

variable "db_instance_type" {
  description = "The type of the DB instance"
  type        = string
  default     = "db.t3.micro"
}

variable "db_engine" {
  description = "The engine to use for the RDS instance"
  type        = string
  default     = "mysql"
}
