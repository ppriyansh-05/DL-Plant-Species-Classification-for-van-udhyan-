import React from 'react';
import { Leaf, Heart, Shield } from 'lucide-react';

interface FooterProps {
  onNavigate: (id: string) => void;
}

export const Footer: React.FC<FooterProps> = ({ onNavigate }) => {
  return (
    <footer className="border-t border-white/[0.08] bg-[#040D09]/90 relative z-20 pt-16 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          
          {/* Brand Info */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#2D6A4F] to-[#0F2A1E] border border-[#52B788]/30 flex items-center justify-center">
                <Leaf className="w-5 h-5 text-[#52B788]" />
              </div>
              <span className="font-heading font-extrabold text-base tracking-widest uppercase text-white">
                Van Udyan <span className="text-[#C9A227]">Plant AI</span>
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 max-w-md leading-relaxed mb-4">
              Urban Biodiversity Computer Vision system designed for the Rural Social Welfare Foundation (RSWF) 
              sanctuary in Pune, Maharashtra. Built to preserve and document regional native flora.
            </p>
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span>Strict academic evaluation standard • EfficientNetB0 Keras 3</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <div className="text-xs font-heading font-extrabold uppercase tracking-widest text-[#B7C56A] mb-4">
              Navigation
            </div>
            <ul className="space-y-2.5 text-xs text-slate-400">
              <li>
                <button
                  onClick={() => onNavigate('identify')}
                  className="hover:text-white transition-colors cursor-pointer"
                >
                  Plant Identifier
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('performance')}
                  className="hover:text-white transition-colors cursor-pointer"
                >
                  Benchmark Metrics
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('species')}
                  className="hover:text-white transition-colors cursor-pointer"
                >
                  15 Species Catalog
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('about')}
                  className="hover:text-white transition-colors cursor-pointer"
                >
                  Project Provenance
                </button>
              </li>
            </ul>
          </div>

          {/* Technology & Partners */}
          <div>
            <div className="text-xs font-heading font-extrabold uppercase tracking-widest text-[#F5C542] mb-4">
              Stack & Open Science
            </div>
            <ul className="space-y-2.5 text-xs text-slate-400">
              <li>FastAPI • Python 3 ASGI</li>
              <li>React 19 + TypeScript + Vite</li>
              <li>Tailwind CSS • Bento Design</li>
              <li>RSWF Pune Bio-Reserve Grid</li>
              <li>
                <a
                  href="https://github.com/ppriyansh-05/DL-Plant-Species-Classification-for-van-udhyan-"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-emerald-400 hover:text-emerald-300 font-semibold"
                >
                  <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                  </svg>
                  <span>View on GitHub</span>
                </a>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/[0.06] flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-400">
          <div>
            © {new Date().getFullYear()} Van Udyan Plant AI • RSWF Pune Botanical Preservation.
          </div>
          <div className="flex items-center gap-1">
            <span>Developed for Pune urban bio-conservation with</span>
            <Heart className="w-3.5 h-3.5 text-red-400 inline" />
          </div>
        </div>
      </div>
    </footer>
  );
};
