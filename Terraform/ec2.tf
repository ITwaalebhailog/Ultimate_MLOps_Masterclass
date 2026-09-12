resource "aws_security_group" "ec2_sg" {
  name   = "tf-ec2-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2" {
  count                  = 2
  ami                    = "ami-0f58b397bc5c1f2e8" # Amazon Linux 2 (Mumbai)
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public_1a.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name               = "linux-1"

  tags = {
    Name = "tf-ec2-${count.index}"
  }
}


