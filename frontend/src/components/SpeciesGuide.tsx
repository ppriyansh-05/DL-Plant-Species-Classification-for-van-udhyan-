import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, MapPin, Leaf, ArrowRight, Filter } from 'lucide-react';
import type { SpeciesItem } from '../lib/api';
import { SpeciesModal } from './SpeciesModal';

interface SpeciesGuideProps {
  speciesList: SpeciesItem[];
}

export const SpeciesGuide: React.FC<SpeciesGuideProps> = ({ speciesList }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedZone, setSelectedZone] = useState('All');
  const [selectedSpecies, setSelectedSpecies] = useState<SpeciesItem | null>(null);

  const zones = ['All', 'Zone 1', 'Zone 2', 'Zone 3'];

  // Filter species based on search query and selected zone
  const filteredSpecies = speciesList.filter((s) => {
    const matchesSearch =
      s.common_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.scientific_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.marathi_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.family.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesZone =
      selectedZone === 'All' || s.zones.includes(selectedZone);

    return matchesSearch && matchesZone;
  });

  return (
    <section id="species" className="py-20 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10">
          <div>
            <div className="pill-tag-green pill-tag mb-3">BOTANICAL FIELD REPOSITORY</div>
            <h2 className="font-display font-extrabold text-3xl sm:text-5xl text-white tracking-tight">
              Van Udyan <span className="text-gold-leaf-gradient italic">Species Guide</span>
            </h2>
          </div>
          <p className="mt-4 md:mt-0 text-sm text-slate-300/80 max-w-md">
            Explore all 15 native urban tree species cataloged across the Pune reserve zones.
          </p>
        </div>

        {/* Filter & Search Bar */}
        <div className="bento-card p-4 sm:p-5 rounded-3xl mb-10 flex flex-col sm:flex-row gap-4 items-center justify-between">
          
          {/* Search Box */}
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by name, Marathi, or family..."
              className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-white/[0.05] border border-white/[0.1] text-xs text-white placeholder-slate-400 focus:outline-none focus:border-[#52B788]/60 transition-colors"
            />
          </div>

          {/* Zone Filter Chips */}
          <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
            <div className="flex items-center gap-1 text-[11px] font-heading font-bold uppercase tracking-wider text-slate-400 mr-2 shrink-0">
              <Filter className="w-3 h-3 text-[#52B788]" />
              <span>Zone:</span>
            </div>
            {zones.map((zone) => {
              const active = selectedZone === zone;
              return (
                <button
                  key={zone}
                  onClick={() => setSelectedZone(zone)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                    active
                      ? 'bg-[#52B788] text-[#06140E] shadow-md shadow-[#52B788]/20'
                      : 'bg-white/[0.04] text-slate-300 hover:bg-white/[0.08] hover:text-white border border-white/[0.06]'
                  }`}
                >
                  {zone === 'All' ? 'All Zones (1-3)' : zone}
                </button>
              );
            })}
          </div>

        </div>

        {/* Species Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredSpecies.map((item, idx) => (
            <motion.div
              key={item.class_name}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: idx * 0.05 }}
              className="bento-card p-6 rounded-3xl flex flex-col justify-between group hover:-translate-y-1 transition-all"
            >
              <div>
                {/* Top Badges */}
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[10px] font-mono uppercase px-2.5 py-0.5 rounded-md bg-white/[0.06] border border-white/[0.08] text-amber-200">
                    {item.family}
                  </span>
                  <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#B7C56A]">
                    <MapPin className="w-3 h-3" />
                    <span>{item.zone}</span>
                  </span>
                </div>

                {/* Common & Scientific Names */}
                <h3 className="font-display font-bold text-xl text-white group-hover:text-[#52B788] transition-colors mb-0.5">
                  {item.common_name}
                </h3>
                <div className="text-xs text-emerald-400 italic font-serif mb-2">
                  {item.scientific_name}
                </div>

                {item.marathi_name && (
                  <div className="text-[11px] text-slate-300 mb-3">
                    मराठी: <span className="text-slate-100 font-medium">{item.marathi_name}</span>
                  </div>
                )}

                <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
                  {item.ecological_role}
                </p>
              </div>

              {/* Action Button */}
              <button
                onClick={() => setSelectedSpecies(item)}
                className="w-full mt-2 pt-3 border-t border-white/[0.06] flex items-center justify-between text-xs text-slate-300 group-hover:text-emerald-300 transition-colors cursor-pointer"
              >
                <span className="font-heading font-semibold text-[11px] uppercase tracking-wider">
                  Botanical Profile
                </span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </motion.div>
          ))}
        </div>

        {filteredSpecies.length === 0 && (
          <div className="bento-card p-12 rounded-3xl text-center text-slate-400">
            <Leaf className="w-8 h-8 text-slate-500 mx-auto mb-3" />
            <div className="font-bold text-white text-base">No species matched your search</div>
            <p className="text-xs text-slate-400 mt-1">Try resetting the zone filter or clearing the search keyword.</p>
          </div>
        )}

      </div>

      {/* Detail Modal */}
      <SpeciesModal
        species={selectedSpecies}
        onClose={() => setSelectedSpecies(null)}
      />
    </section>
  );
};
