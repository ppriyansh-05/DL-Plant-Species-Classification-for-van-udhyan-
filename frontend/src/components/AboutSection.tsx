import React from 'react';
import { ExternalLink, HeartHandshake, Database } from 'lucide-react';

export const AboutSection: React.FC = () => {
  return (
    <section id="about" className="py-20 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <div className="pill-tag mb-3">ORIGIN & PROVENANCE</div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl text-white tracking-tight mb-4">
            Protecting Urban Habitats <br />
            <span className="text-gold-leaf-gradient italic">Through Plant Vision</span>
          </h2>
          <p className="text-sm sm:text-base text-slate-300/80 leading-relaxed">
            A collaborative deep learning initiative uniting computer vision engineers, 
            local arborists, and community biodiversity stewards in Pune.
          </p>
        </div>

        {/* Narrative Bento Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-12">
          
          {/* Main Story Card (8 cols) */}
          <div className="lg:col-span-8 bento-card p-7 sm:p-9 rounded-3xl relative overflow-hidden">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-2xl bg-[#52B788]/15 border border-[#52B788]/30 flex items-center justify-center">
                <HeartHandshake className="w-6 h-6 text-[#52B788]" />
              </div>
              <div>
                <span className="text-[10px] font-heading font-extrabold uppercase tracking-widest text-[#B7C56A]">
                  COMMUNITY COLLABORATION
                </span>
                <h3 className="font-display font-bold text-2xl text-white">
                  The RSWF Pune Partnership
                </h3>
              </div>
            </div>

            <p className="text-sm text-slate-300/90 leading-relaxed mb-4">
              Van Udyan is an ecological sanctuary maintained with meticulous care by the 
              <strong> Rural Social Welfare Foundation (RSWF)</strong> in Pune, Maharashtra. 
              The bio-reserve hosts a vibrant canopy of indigenous, medicinal, and keystone tropical trees 
              that mitigate the urban heat island effect and serve as migratory corridors for regional avifauna.
            </p>

            <p className="text-sm text-slate-300/90 leading-relaxed mb-6">
              This machine learning initiative was conceived to provide naturalists, student researchers, and 
              park visitors with an instant, trustworthy diagnostic tool to identify native trees in-situ, 
              fostering ecological literacy and systematic botanical monitoring across Pune's green belt.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-white/[0.08]">
              <div className="p-3 rounded-2xl bg-white/[0.03]">
                <div className="text-[11px] font-heading font-bold uppercase tracking-wider text-emerald-400">Location</div>
                <div className="text-xs text-white font-medium mt-0.5">Pune, Maharashtra</div>
              </div>
              <div className="p-3 rounded-2xl bg-white/[0.03]">
                <div className="text-[11px] font-heading font-bold uppercase tracking-wider text-[#B7C56A]">Affiliation</div>
                <div className="text-xs text-white font-medium mt-0.5">RSWF Bio-Reserves</div>
              </div>
              <div className="p-3 rounded-2xl bg-white/[0.03]">
                <div className="text-[11px] font-heading font-bold uppercase tracking-wider text-[#C9A227]">Target</div>
                <div className="text-xs text-white font-medium mt-0.5">Top-15 Keystone Flora</div>
              </div>
            </div>
          </div>

          {/* Dataset & Licensing Card (4 cols) */}
          <div className="lg:col-span-4 bento-card-sage p-7 sm:p-8 rounded-3xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-[#B7C56A]/15 border border-[#B7C56A]/30 flex items-center justify-center mb-6">
                <Database className="w-6 h-6 text-[#B7C56A]" />
              </div>

              <span className="text-[10px] font-heading font-extrabold uppercase tracking-widest text-[#B7C56A]">
                DATA PROVENANCE
              </span>
              <h3 className="font-display font-bold text-xl text-white mt-1 mb-3">
                Dataset Attribution & Licensing
              </h3>

              <div className="space-y-3 text-xs text-slate-200/90 leading-relaxed">
                <div className="p-3 rounded-2xl bg-black/30 border border-white/10">
                  <div className="font-bold text-white mb-0.5">1. In-Situ Field Photography</div>
                  <span>High-resolution leaf, canopy, and trunk photos captured on ground at Van Udyan.</span>
                </div>

                <div className="p-3 rounded-2xl bg-black/30 border border-white/10">
                  <div className="font-bold text-white mb-0.5">2. iNaturalist Research Observations</div>
                  <span>Curated under Creative Commons (CC-BY / CC-BY-NC) with verified community taxonomy.</span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-white/10 flex items-center justify-between text-xs text-slate-300">
              <span className="text-[11px] font-medium">Academic Open-Science</span>
              <a
                href="https://github.com/ppriyansh-05/DL-Plant-Species-Classification-for-van-udhyan-"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 text-emerald-400 hover:text-emerald-300 font-semibold"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
                <span>GitHub Repository</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
};
