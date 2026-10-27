import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, MapPin, Calendar, Leaf, Award, Compass } from 'lucide-react';
import type { SpeciesItem } from '../lib/api';

interface SpeciesModalProps {
  species: SpeciesItem | null;
  onClose: () => void;
}

export const SpeciesModal: React.FC<SpeciesModalProps> = ({ species, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!species) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/80 backdrop-blur-md"
        />

        {/* Modal Window */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
          className="relative w-full max-w-2xl bento-card p-6 sm:p-8 rounded-3xl border border-white/15 shadow-2xl z-10 my-8 overflow-hidden"
        >
          {/* Top Bar */}
          <div className="flex items-start justify-between gap-4 mb-6">
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="pill-tag-green pill-tag">
                  {species.family}
                </span>
                <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-[#B7C56A]/15 border border-[#B7C56A]/30 text-[#B7C56A] text-xs font-bold font-heading">
                  <MapPin className="w-3 h-3" />
                  <span>{species.zone}</span>
                </span>
              </div>
              <h3 className="font-display font-extrabold text-2xl sm:text-3xl text-white">
                {species.common_name}
              </h3>
              <div className="text-emerald-400 italic text-base font-serif mt-0.5">
                {species.scientific_name}
              </div>
              {species.marathi_name && (
                <div className="text-xs text-slate-300 font-medium mt-1">
                  स्थानिक नाव: <span className="text-amber-300 font-semibold">{species.marathi_name}</span>
                </div>
              )}
            </div>

            <button
              onClick={onClose}
              className="p-2.5 rounded-2xl bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.08] text-slate-300 hover:text-white transition-colors cursor-pointer"
              aria-label="Close modal"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Grid of Botanical Characteristics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            
            <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
              <div className="flex items-center gap-2 text-xs font-heading font-extrabold uppercase tracking-wider text-[#B7C56A] mb-1.5">
                <Leaf className="w-4 h-4 text-[#52B788]" />
                <span>Foliage & Texture</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {species.foliage || 'Distinct morphological leaf structure suited for drought resilience and tropical urban microclimates.'}
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
              <div className="flex items-center gap-2 text-xs font-heading font-extrabold uppercase tracking-wider text-[#F5C542] mb-1.5">
                <Calendar className="w-4 h-4 text-[#F5C542]" />
                <span>Phenology & Bloom</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {species.blooming_season || 'Seasonal flowering and fruiting cycles coinciding with Maharashtra monsoon and dry seasons.'}
              </p>
            </div>

          </div>

          {/* Ecological Role in Pune Urban Bio-Reserve */}
          <div className="p-5 rounded-2xl bg-[#0F2A1E]/80 border border-[#52B788]/20 mb-6">
            <div className="flex items-center gap-2 text-xs font-heading font-extrabold uppercase tracking-wider text-[#52B788] mb-2">
              <Award className="w-4 h-4 text-[#52B788]" />
              <span>Ecological Value & Urban Forestry Role</span>
            </div>
            <p className="text-xs sm:text-sm text-slate-200/90 leading-relaxed">
              {species.ecological_role}
            </p>
          </div>

          {/* Zone Distribution Breakdown */}
          <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.05] flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-xs text-slate-300">
              <Compass className="w-4 h-4 text-emerald-400" />
              <span>RSWF Van Udyan Verified Zones:</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {species.zones.map((z) => (
                <span
                  key={z}
                  className="px-2.5 py-1 rounded-lg bg-[#52B788]/15 border border-[#52B788]/30 text-[11px] font-semibold text-emerald-300"
                >
                  {z}
                </span>
              ))}
            </div>
          </div>

        </motion.div>
      </div>
    </AnimatePresence>
  );
};
