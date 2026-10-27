import React, { useEffect } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';
import { Camera, Sparkles, BarChart3, ArrowRight, ShieldCheck } from 'lucide-react';
import heroLeavesSvg from '../assets/leaves-hero.svg';

interface HeroProps {
  onIdentifyClick: () => void;
  onPerformanceClick: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onIdentifyClick, onPerformanceClick }) => {
  // Parallax tracking
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // Smooth springs for natural organic drift
  const springConfig = { damping: 25, stiffness: 120 };
  const leafX = useSpring(mouseX, springConfig);
  const leafY = useSpring(mouseY, springConfig);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const { innerWidth, innerHeight } = window;
      const x = (e.clientX / innerWidth - 0.5) * 35;
      const y = (e.clientY / innerHeight - 0.5) * 35;
      mouseX.set(x);
      mouseY.set(y);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  return (
    <section className="relative min-h-[90vh] flex items-center pt-24 pb-16 overflow-hidden">
      {/* Ambient background glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[#52B788]/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-[500px] h-[500px] bg-[#C9A227]/8 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Column: Hero Typography & CTA */}
          <motion.div
            className="lg:col-span-7 flex flex-col items-start"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          >
            {/* Pill Label */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#183B2B]/70 border border-[#52B788]/30 shadow-inner mb-6 backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-[#52B788] animate-pulse" />
              <span className="font-heading font-extrabold text-[11px] tracking-widest text-[#B7C56A] uppercase">
                URBAN BIODIVERSITY AI
              </span>
            </div>

            {/* Giant Display Headline with Gold-to-Green Gradient */}
            <h1 className="font-display font-extrabold text-5xl sm:text-6xl md:text-7xl lg:text-7xl tracking-tight leading-[1.08] mb-4 text-white">
              Van Udyan <br />
              <span className="text-gold-leaf-gradient italic">Plant AI</span>
            </h1>

            {/* Tiny uppercase subtitle */}
            <div className="font-heading font-bold text-xs uppercase tracking-[0.25em] text-[#7FA38A] mb-5">
              RSWF PUNE • IN-SITU CANOPY & LEAF RECOGNITION
            </div>

            {/* Tagline */}
            <p className="text-base sm:text-lg text-slate-300/90 leading-relaxed max-w-xl mb-8">
              Trained on authentic ecological field photographs and research-grade botanical archives. 
              Real-time deep learning diagnosis for 15 native urban tree species across Pune's bio-reserve.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-4 w-full sm:w-auto">
              <button
                onClick={onIdentifyClick}
                className="w-full sm:w-auto px-7 py-4 rounded-2xl bg-gradient-to-r from-[#52B788] to-[#3E9B6E] text-[#06140E] font-heading font-bold text-sm tracking-wide shadow-xl shadow-[#52B788]/20 hover:shadow-[#52B788]/35 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2.5 group cursor-pointer"
              >
                <Camera className="w-4 h-4 text-[#06140E] group-hover:rotate-6 transition-transform" />
                <span>Identify a Plant</span>
                <ArrowRight className="w-4 h-4 text-[#06140E] group-hover:translate-x-1 transition-transform" />
              </button>

              <button
                onClick={onPerformanceClick}
                className="w-full sm:w-auto px-7 py-4 rounded-2xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.12] text-white font-heading font-semibold text-sm tracking-wide hover:border-[#52B788]/40 transition-all flex items-center justify-center gap-2 cursor-pointer backdrop-blur-md"
              >
                <BarChart3 className="w-4 h-4 text-[#B7C56A]" />
                <span>View Performance</span>
              </button>
            </div>

            {/* Trust Pill */}
            <div className="mt-8 flex items-center gap-3 text-xs text-slate-400">
              <ShieldCheck className="w-4 h-4 text-[#52B788]" />
              <span>Zero hallucinations • 100% genuine EfficientNetB0 neural inference</span>
            </div>
          </motion.div>

          {/* Right Column: Layered Botanical Leaves Art with Parallax */}
          <div className="lg:col-span-5 relative flex items-center justify-center">
            {/* Dark gradient overlay on mobile/desktop to ensure text legibility */}
            <div className="absolute inset-0 bg-gradient-to-l from-transparent via-[#06140E]/40 to-[#06140E] lg:hidden z-10 pointer-events-none" />

            {/* Interactive Parallax Leaf Container */}
            <motion.div
              style={{ x: leafX, y: leafY }}
              className="relative w-full max-w-md lg:max-w-lg aspect-square flex items-center justify-center select-none"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1.2, ease: 'easeOut', delay: 0.2 }}
            >
              {/* Backing Glow Ring */}
              <div className="absolute w-72 h-72 rounded-full border border-[#52B788]/20 bg-gradient-to-tr from-[#52B788]/10 via-transparent to-[#C9A227]/10 blur-xl" />

              {/* Master Botanical Illustration */}
              <img
                src={heroLeavesSvg}
                alt="Botanical Leaf Specimen"
                className="w-full h-full object-contain filter drop-shadow-[0_25px_35px_rgba(0,0,0,0.7)]"
                loading="eager"
              />

              {/* Floating Bento Badge Overlay */}
              <motion.div
                className="absolute bottom-6 left-2 sm:left-6 bento-card p-3 sm:p-4 rounded-2xl flex items-center gap-3 border border-white/10 shadow-2xl backdrop-blur-xl"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 }}
              >
                <div className="w-9 h-9 rounded-xl bg-[#52B788]/20 border border-[#52B788]/40 flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-[#52B788]" />
                </div>
                <div>
                  <div className="text-[11px] font-heading font-extrabold text-white uppercase tracking-wider">
                    RSWF Bio-Grid
                  </div>
                  <div className="text-[10px] text-[#B7C56A] font-medium">
                    15 Flora Classes • Pune Zones 1-3
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>

        </div>
      </div>
    </section>
  );
};
