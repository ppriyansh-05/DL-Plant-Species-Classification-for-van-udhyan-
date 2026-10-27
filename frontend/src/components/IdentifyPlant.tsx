import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  UploadCloud, 
  Camera, 
  Image as ImageIcon, 
  AlertTriangle, 
  RefreshCw, 
  Sparkles, 
  MapPin 
} from 'lucide-react';
import { 
  predictImage, 
  fetchSamples, 
  fetchSampleBlob, 
  type PredictionResponse, 
  type SampleItem 
} from '../lib/api';
import { ConfidenceRing } from './ConfidenceRing';

export const IdentifyPlant: React.FC = () => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [samples, setSamples] = useState<SampleItem[]>([]);
  const [loadingSample, setLoadingSample] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchSamples()
      .then((data) => setSamples(data.samples || []))
      .catch(() => setSamples([]));
  }, []);

  // Handle selected image file
  const handleProcessFile = async (file: File) => {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
    if (!validTypes.includes(file.type.toLowerCase())) {
      setErrorMessage('Please upload a valid image (JPEG, PNG, or WEBP).');
      return;
    }

    // Validate size (8MB)
    if (file.size > 8 * 1024 * 1024) {
      setErrorMessage(`File size (${(file.size / (1024 * 1024)).toFixed(1)} MB) exceeds maximum allowed size of 8 MB.`);
      return;
    }

    setPreviewUrl(URL.createObjectURL(file));
    setErrorMessage(null);
    setPrediction(null);
    setIsLoading(true);

    try {
      const result = await predictImage(file, 3);
      setPrediction(result);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 150);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to process image inference.');
    } finally {
      setIsLoading(false);
    }
  };

  // Quick test with sample photo
  const handleSelectSample = async (sample: SampleItem) => {
    setLoadingSample(true);
    setErrorMessage(null);
    try {
      const parts = sample.relative_path.split('/');
      const speciesName = parts[parts.length - 2];
      const filename = parts[parts.length - 1];
      const blob = await fetchSampleBlob(speciesName, filename);
      const file = new File([blob], filename, { type: 'image/jpeg' });
      await handleProcessFile(file);
    } catch (err: any) {
      setErrorMessage('Could not load benchmark sample image.');
    } finally {
      setLoadingSample(false);
    }
  };

  // Drag and drop handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleProcessFile(e.dataTransfer.files[0]);
    }
  };

  const handleReset = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setPrediction(null);
    setErrorMessage(null);
  };

  const topPrediction = prediction?.top_k[0];

  return (
    <section id="identify" className="py-20 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="pill-tag-green pill-tag mb-3">NEURAL SPECIES DIAGNOSIS</div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl text-white tracking-tight mb-4">
            Identify a Plant <span className="text-gold-leaf-gradient italic">Specimen</span>
          </h2>
          <p className="text-sm sm:text-base text-slate-300/80 leading-relaxed">
            Drop an in-situ leaf, bark, or canopy photograph. EfficientNetB0 evaluates 
            botanical textures against the 15 documented Pune Van Udyan species.
          </p>
        </div>

        {/* Uploader Card */}
        <div className="max-w-4xl mx-auto">
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`bento-card p-6 sm:p-10 rounded-3xl border-2 border-dashed transition-all relative ${
              isDragging 
                ? 'border-[#52B788] bg-[#52B788]/10 shadow-[0_0_40px_rgba(82,183,136,0.25)]' 
                : 'border-white/[0.15] hover:border-[#52B788]/50'
            }`}
          >
            {/* Hidden native inputs */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={(e) => e.target.files?.[0] && handleProcessFile(e.target.files[0])}
              accept="image/jpeg,image/png,image/webp"
              className="hidden"
            />
            <input
              type="file"
              ref={cameraInputRef}
              onChange={(e) => e.target.files?.[0] && handleProcessFile(e.target.files[0])}
              accept="image/*"
              capture="environment"
              className="hidden"
            />

            <div className="flex flex-col items-center justify-center text-center">
              <div className="w-16 h-16 rounded-3xl bg-gradient-to-br from-[#2D6A4F] to-[#0F2A1E] border border-[#52B788]/30 flex items-center justify-center mb-5 shadow-lg shadow-[#52B788]/15">
                <UploadCloud className="w-8 h-8 text-[#52B788]" />
              </div>

              <div className="font-heading font-extrabold text-lg sm:text-xl text-white mb-2">
                Drop your specimen photo here, or browse
              </div>

              <p className="text-xs sm:text-sm text-slate-400 max-w-md mb-6">
                JPG, PNG, or WEBP up to 8 MB. Automatically preprocessed to 224x224 RGB.
              </p>

              {/* Upload Action Buttons */}
              <div className="flex flex-wrap items-center justify-center gap-3 w-full sm:w-auto">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl bg-[#52B788] text-[#06140E] font-heading font-bold text-xs uppercase tracking-wider hover:bg-[#439B72] transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-[#52B788]/20"
                >
                  <ImageIcon className="w-4 h-4" />
                  <span>Choose Image File</span>
                </button>

                <button
                  type="button"
                  onClick={() => cameraInputRef.current?.click()}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl bg-white/[0.06] hover:bg-white/[0.12] border border-white/[0.15] text-white font-heading font-semibold text-xs uppercase tracking-wider transition-colors flex items-center justify-center gap-2 cursor-pointer"
                >
                  <Camera className="w-4 h-4 text-[#B7C56A]" />
                  <span>Take Photo (Camera)</span>
                </button>
              </div>

              {/* Field Photography Guidance Tips */}
              <div className="mt-8 pt-6 border-t border-white/[0.08] w-full grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
                <div className="flex items-center gap-2.5 p-2.5 rounded-xl bg-white/[0.02]">
                  <span className="w-2 h-2 rounded-full bg-[#52B788]" />
                  <span className="text-[11px] text-slate-300"><strong>Good Light:</strong> Avoid strong harsh shadows</span>
                </div>
                <div className="flex items-center gap-2.5 p-2.5 rounded-xl bg-white/[0.02]">
                  <span className="w-2 h-2 rounded-full bg-[#B7C56A]" />
                  <span className="text-[11px] text-slate-300"><strong>Single Leaf:</strong> Keep target centered in frame</span>
                </div>
                <div className="flex items-center gap-2.5 p-2.5 rounded-xl bg-white/[0.02]">
                  <span className="w-2 h-2 rounded-full bg-[#C9A227]" />
                  <span className="text-[11px] text-slate-300"><strong>Clean Backdrop:</strong> Contrast against background</span>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Benchmark Samples Selector */}
          {samples.length > 0 && (
            <div className="mt-6 p-4 rounded-2xl bg-[#0F2A1E]/40 border border-white/[0.06]">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2 text-xs font-heading font-bold uppercase tracking-wider text-[#B7C56A]">
                  <Sparkles className="w-3.5 h-3.5 text-[#C9A227]" />
                  <span>Or Test with Authentic Van Udyan Benchmark Photos</span>
                </div>
                {loadingSample && (
                  <span className="text-[11px] text-slate-400 flex items-center gap-1.5 animate-pulse">
                    <RefreshCw className="w-3 h-3 animate-spin text-emerald-400" />
                    Loading sample...
                  </span>
                )}
              </div>
              <div className="flex flex-wrap gap-2">
                {samples.slice(0, 6).map((s) => (
                  <button
                    key={s.id}
                    onClick={() => handleSelectSample(s)}
                    disabled={isLoading || loadingSample}
                    className="text-left px-3 py-1.5 rounded-lg bg-white/[0.04] hover:bg-emerald-500/15 border border-white/[0.08] hover:border-emerald-500/40 text-[11px] text-slate-300 hover:text-white transition-all cursor-pointer disabled:opacity-50"
                  >
                    <span className="font-semibold text-white">{s.common_name.split('/')[0].trim()}</span>
                    <span className="text-slate-400 text-[10px] ml-1.5 font-mono">({s.zone})</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Error Message */}
          {errorMessage && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 p-4 rounded-2xl bg-red-950/40 border border-red-500/40 text-red-300 flex items-start gap-3"
            >
              <AlertTriangle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
              <div>
                <div className="font-bold text-sm text-red-200">Inference Alert</div>
                <div className="text-xs text-red-300/90 mt-0.5">{errorMessage}</div>
              </div>
            </motion.div>
          )}

          {/* Loading Skeleton State */}
          {isLoading && (
            <div className="mt-8 bento-card p-8 rounded-3xl animate-pulse">
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                <div className="lg:col-span-5 h-64 rounded-2xl bg-white/[0.05]" />
                <div className="lg:col-span-7 space-y-4">
                  <div className="h-4 w-28 bg-[#52B788]/20 rounded-full" />
                  <div className="h-8 w-3/4 bg-white/[0.08] rounded-xl" />
                  <div className="h-4 w-1/2 bg-white/[0.05] rounded-lg" />
                  <div className="h-24 w-full bg-white/[0.04] rounded-2xl" />
                  <div className="space-y-2 pt-2">
                    <div className="h-8 w-full bg-white/[0.03] rounded-lg" />
                    <div className="h-8 w-full bg-white/[0.03] rounded-lg" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Prediction Result Display (Two-Column Layout) */}
          <div ref={resultsRef}>
            <AnimatePresence>
              {prediction && !isLoading && topPrediction && (
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.6, ease: 'easeOut' }}
                  className="mt-10"
                >
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                    
                    {/* Left Column: Image Preview Card */}
                    <div className="lg:col-span-5 bento-card p-5 rounded-3xl relative overflow-hidden">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-[10px] font-heading font-bold uppercase tracking-wider text-emerald-400 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                          Captured Specimen
                        </span>
                        <button
                          onClick={handleReset}
                          className="text-[11px] text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer transition-colors"
                        >
                          <RefreshCw className="w-3 h-3" />
                          <span>New Upload</span>
                        </button>
                      </div>

                      {previewUrl && (
                        <div className="rounded-2xl overflow-hidden border border-white/[0.1] bg-black/40 aspect-square relative flex items-center justify-center">
                          <img
                            src={previewUrl}
                            alt="Specimen preview"
                            className="w-full h-full object-cover"
                          />
                          <div className="absolute bottom-2 left-2 right-2 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 flex items-center justify-between text-[10px] text-slate-300">
                            <span>Resized to 224×224 RGB</span>
                            <span className="text-emerald-400 font-mono">{prediction.inference_ms}ms latency</span>
                          </div>
                        </div>
                      )}

                      {/* Botanical Ecological Snippet */}
                      <div className="mt-4 p-3.5 rounded-2xl bg-white/[0.03] border border-white/[0.05]">
                        <div className="text-[10px] font-heading font-extrabold uppercase tracking-wider text-[#B7C56A] mb-1">
                          Ecological Role
                        </div>
                        <p className="text-xs text-slate-300/90 leading-relaxed">
                          {topPrediction.ecological_role}
                        </p>
                      </div>
                    </div>

                    {/* Right Column: Prediction Details Card */}
                    <div className="lg:col-span-7 bento-card p-6 sm:p-8 rounded-3xl relative overflow-hidden">
                      
                      {/* Top Header: Badge + Zone Chip */}
                      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
                        <div className="pill-tag-green pill-tag">
                          TOP RANKED CANDIDATE
                        </div>
                        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#B7C56A]/15 border border-[#B7C56A]/30 text-[#B7C56A] text-xs font-bold font-heading">
                          <MapPin className="w-3.5 h-3.5" />
                          <span>{topPrediction.zone}</span>
                        </div>
                      </div>

                      {/* Specimen Names & Confidence Ring */}
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-6 border-b border-white/[0.08]">
                        <div>
                          <h3 className="font-display font-extrabold text-2xl sm:text-3xl text-white tracking-tight">
                            {topPrediction.common_name}
                          </h3>
                          <div className="text-sm text-emerald-400/90 italic font-serif mt-0.5">
                            {topPrediction.scientific_name}
                          </div>
                          {topPrediction.marathi_name && (
                            <div className="text-xs text-slate-400 font-medium mt-1">
                              स्थानिक नाव: <span className="text-slate-200">{topPrediction.marathi_name}</span>
                            </div>
                          )}
                          <div className="text-xs text-slate-400 mt-1">
                            Family: <span className="text-amber-200 font-mono">{topPrediction.family}</span>
                          </div>
                        </div>

                        {/* Animated Confidence Ring */}
                        <div className="shrink-0 flex justify-center sm:justify-end">
                          <ConfidenceRing percentage={topPrediction.confidence_pct} size={110} strokeWidth={9} />
                        </div>
                      </div>

                      {/* Low Confidence Warning Notice */}
                      {prediction.is_low_confidence && prediction.warning && (
                        <div className="mt-5 p-4 rounded-2xl bg-amber-950/40 border border-amber-500/40 text-amber-200 flex items-start gap-3">
                          <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                          <div>
                            <div className="font-bold text-xs uppercase tracking-wider text-amber-300">
                              Honest Scientific Notice: Low Confidence (&lt;40%)
                            </div>
                            <div className="text-xs text-amber-200/90 mt-1 leading-relaxed">
                              {prediction.warning}
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Top-3 Candidates Horizontal Bars */}
                      <div className="mt-6">
                        <div className="flex items-center justify-between text-xs font-heading font-extrabold tracking-wider uppercase text-slate-300 mb-3">
                          <span>Top 3 Candidates Trace</span>
                          <span className="text-[10px] text-slate-400 lowercase font-mono">softmax probability</span>
                        </div>

                        <div className="space-y-3">
                          {prediction.top_k.map((cand, idx) => (
                            <div
                              key={cand.class_name}
                              className="p-3 rounded-2xl bg-white/[0.03] border border-white/[0.05] hover:border-white/[0.12] transition-colors"
                            >
                              <div className="flex items-center justify-between text-xs mb-1.5">
                                <div className="flex items-center gap-2">
                                  <span className="font-mono text-[10px] w-4 h-4 rounded-full bg-white/[0.08] flex items-center justify-center font-bold text-slate-300">
                                    {idx + 1}
                                  </span>
                                  <span className="font-semibold text-white">
                                    {cand.common_name.split('/')[0]}
                                  </span>
                                  <span className="text-slate-400 italic text-[11px] hidden sm:inline">
                                    ({cand.scientific_name})
                                  </span>
                                </div>
                                <span className="font-heading font-extrabold text-xs text-[#52B788]">
                                  {cand.confidence_pct.toFixed(1)}%
                                </span>
                              </div>

                              {/* Horizontal Bar */}
                              <div className="w-full h-2 rounded-full bg-white/[0.06] overflow-hidden">
                                <motion.div
                                  className="h-full rounded-full bg-gradient-to-r from-[#2D6A4F] to-[#52B788]"
                                  initial={{ width: 0 }}
                                  animate={{ width: `${Math.min(cand.confidence_pct, 100)}%` }}
                                  transition={{ duration: 0.8, delay: idx * 0.15 }}
                                />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                    </div>

                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

        </div>

      </div>
    </section>
  );
};
