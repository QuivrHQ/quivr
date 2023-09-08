output "vpc_id" {
  value = data.aws_vpc.selected.id
}

output "subnets_ids" {
  value = data.aws_subnet.this
}
