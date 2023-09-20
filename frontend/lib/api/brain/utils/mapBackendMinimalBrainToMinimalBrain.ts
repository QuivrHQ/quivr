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
});
