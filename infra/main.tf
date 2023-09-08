module "ecs_cluster" {
  source           = "./modules/ecs"
  ecs_cluster_name = "quivr"
}


module "api" {
  source          = "./modules/load_balancer"
  api_domain_name = "api.quivr.app"
}

module "quivr_backend" {
  source     = "./modules/ecs_task"
  cluster_id = module.ecs_cluster.ecs_cluster_id

}
