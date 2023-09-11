module "ecs_cluster" {
  source           = "./modules/ecs"
  ecs_cluster_name = "quivr"
}


module "api" {
  source          = "./modules/load_balancer"
  api_domain_name = "api.quivr.app"
  subnets         = module.network.subnets_ids
}

module "quivr_backend" {
  source            = "./modules/ecs_task"
  cluster_id        = module.ecs_cluster.ecs_cluster_id
  vpc_id            = module.network.vpc_id
  load_balancer_arn = module.api.lb_arn

}

module "network" {
  source = "./modules/network"
}
