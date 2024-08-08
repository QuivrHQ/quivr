import {
  BackendMinimalBrainForUser,
  MinimalBrainForUser,
} from "@/lib/context/BrainProvider/types";

export const mapBackendMinimalBrainToMinimalBrain = (
  backendMinimalBrain: BackendMinimalBrainForUser
): MinimalBrainForUser => ({
  id: backendMinimalBrain.id,
  name: backendMinimalBrain.name,
  role: backendMinimalBrain.rights,
  status: backendMinimalBrain.status,
  brain_type: backendMinimalBrain.brain_type,
  description: backendMinimalBrain.description,
  integration_logo_url: backendMinimalBrain.integration_logo_url,
  max_files: backendMinimalBrain.max_files,
  allow_model_change: backendMinimalBrain.allow_model_change,
  image_url: backendMinimalBrain.image_url,
  display_name: backendMinimalBrain.display_name,
});
