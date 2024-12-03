resource "aws_security_group" "db_sg" {
  name        = "rds-db-sg"
  description = "Security group for RDS instance"

  ingress {
    from_port   = 3306  # MySQL port, change for PostgreSQL if needed
    to_port     = 3306  # MySQL port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all IPs for testing; restrict in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-db-sg"
  }
}

# Now, your aws_db_instance should reference this security group
resource "aws_db_instance" "default" {
  allocated_storage    = 20    # Size of your database storage (in GB)
  instance_class       = var.db_instance_type  # e.g., db.t3.micro
  engine               = var.db_engine  # mysql or postgres
  engine_version       = "8.0"  # MySQL version; change based on your engine
  db_name              = var.db_name
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true  # Set to false in production to create backups
  multi_az             = false  # Set to true for high availability
  storage_type         = "gp2"
  publicly_accessible  = true   # Set to false for internal use only

  # Reference the created security group
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  tags = {
    Name = var.db_instance_id
  }

  final_snapshot_identifier = "${var.db_instance_id}-final-snapshot"
}
output "db_endpoint" {
  value = aws_db_instance.default.endpoint
}

output "db_username" {
  value = var.db_username
}

output "db_password" {
  value = var.db_password
}

output "db_name" {
  value = var.db_name
}


resource "aws_db_subnet_group" "default" {
  name        = "marketplace-db-subnet-group"
  description = "Subnet group for marketplace RDS instance"
  
  # Use the identified subnet IDs
  subnet_ids = [
    "subnet-0a0a309c818e5298f",  # Subnet in the first AZ (e.g., us-east-1a)
    "subnet-09d069fee52f574e9"   # Subnet in the second AZ (e.g., us-east-1b)
  ]
  
  tags = {
    Name = "marketplace-db-subnet-group"
  }
}
