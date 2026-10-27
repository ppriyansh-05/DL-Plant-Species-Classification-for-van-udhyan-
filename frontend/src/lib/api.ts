/**
 * Typed API Client for Van Udyan Plant AI Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export interface PredictionCandidate {
  class_name: string;
  scientific_name: string;
  common_name: string;
  marathi_name: string;
  family: string;
  zone: string;
  zones: string[];
  ecological_role: string;
  foliage?: string;
  blooming_season?: string;
  confidence: number;
  confidence_pct: number;
}

export interface PredictionResponse {
  top_k: PredictionCandidate[];
  inference_ms: number;
  is_low_confidence: boolean;
  warning: string | null;
  is_real_model: boolean;
}

export interface SpeciesItem {
  id: number;
  class_name: string;
  scientific_name: string;
  common_name: string;
  marathi_name: string;
  family: string;
  zone: string;
  zones: string[];
  ecological_role: string;
  foliage: string;
  blooming_season: string;
}

export interface SpeciesResponse {
  total: number;
  species: SpeciesItem[];
}

export interface Experiment1Metrics {
  backbone: string;
  classes: number;
  train_images: number;
  val_images: number;
  held_out_test_accuracy: number;
  held_out_test_top3_accuracy: number;
  van_udyan_benchmark_accuracy: number;
  van_udyan_benchmark_top3_accuracy: number;
  test_images_count: number;
  benchmark_images_count: number;
}

export interface Experiment2Metrics {
  backbone_selected: string;
  backbone_candidate_1_mobilenet_val_acc: number;
  backbone_candidate_2_effnet_val_acc: number;
  classes: number;
  train_images: number;
  val_images: number;
  held_out_test_images: number;
  van_udyan_benchmark_images: number;
  held_out_test_top1_accuracy: number;
  held_out_test_top3_accuracy: number | null;
  van_udyan_benchmark_top1_accuracy: number;
  van_udyan_benchmark_top3_accuracy: number;
  macro_f1_score: number | null;
  weighted_f1_score: number | null;
  note: string;
}

export interface MetricsResponse {
  model_name: string;
  checkpoint_file: string;
  num_classes: number;
  experiments: {
    experiment_1_38_class_baseline: Experiment1Metrics;
    experiment_2_top15_focused: Experiment2Metrics;
  };
  classes: string[];
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  model_loaded: boolean;
  model_name: string;
  num_classes: number;
  load_error: string | null;
}

export interface SampleItem {
  id: string;
  filename: string;
  species_name: string;
  common_name: string;
  zone: string;
  relative_path: string;
}

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/api/health`);
  if (!res.ok) {
    throw new Error(`Health check failed with status: ${res.status}`);
  }
  return res.json();
}

export async function fetchSpecies(): Promise<SpeciesResponse> {
  const res = await fetch(`${API_BASE_URL}/api/species`);
  if (!res.ok) {
    throw new Error(`Failed to load species: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchMetrics(): Promise<MetricsResponse> {
  const res = await fetch(`${API_BASE_URL}/api/metrics`);
  if (!res.ok) {
    throw new Error(`Failed to load metrics: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchSamples(): Promise<{ samples: SampleItem[] }> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/samples`);
    if (!res.ok) return { samples: [] };
    return res.json();
  } catch {
    return { samples: [] };
  }
}

export async function fetchSampleBlob(species: string, filename: string): Promise<Blob> {
  const res = await fetch(`${API_BASE_URL}/api/samples/image/${encodeURIComponent(species)}/${encodeURIComponent(filename)}`);
  if (!res.ok) {
    throw new Error(`Failed to load sample image`);
  }
  return res.blob();
}

export async function predictImage(file: File, topK: number = 3): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/api/predict?top_k=${topK}`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    let errorDetail = 'Inference request failed';
    try {
      const errJson = await res.json();
      errorDetail = errJson.detail || errorDetail;
    } catch {
      errorDetail = `Server returned status ${res.status} ${res.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return res.json();
}
