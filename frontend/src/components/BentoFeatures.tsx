import React from 'react';
import { motion } from 'framer-motion';
import { 
  Zap, 
  MapPin, 
  ShieldAlert, 
  Leaf, 
  Smartphone, 
  ArrowUpRight 
} from 'lucide-react';

export const BentoFeatures: React.FC = () => {
  const features = [
    {
      id: 'inference',
      title: 'Real-Time Neural Inference',
      subtitle: 'SUB-100MS CPU LATENCY',
      desc: 'Powered by an EfficientNetB0 backbone fine-tuned on native Indian flora. Evaluates complex leaf venation, lobe geometries, and compound leaf structures.',
      icon: Zap,
      theme: 'green',
      colSpan: 'col-span-1 md:col-span-2 lg:col-span-2',
      badge: 'EfficientNetB0',
    },
    {
      id: 'zoning',
      title: 'RSWF Pune Van Udyan',
      subtitle: 'LOCAL BIO-DIVERSITY GRID',
      desc: 'Mapped directly across Pune bio-zones 1, 2, and 3, assisting arborists, park rangers, and nature enthusiasts in tracking urban forest succession.',
      icon: MapPin,
      theme: 'sage',
      colSpan: 'col-span-1 md:col-span-1 lg:col-span-1',
      badge: 'Zones 1 - 3',
    },
    {
      id: 'transparency',
      title: 'Uncompromised Integrity',
      subtitle: 'ZERO PSEUDO-METRICS',
      desc: 'Tested on both held-out test splits and authentic uncurated field benchmark photos with harsh outdoor lighting, shadow occlusions, and wind jitter.',
      icon: ShieldAlert,
      theme: 'terracotta',
      colSpan: 'col-span-1 md:col-span-1 lg:col-span-1',
      badge: 'Empirical Audit',
    },
    {
      id: 'species',
      title: '15 Keystone Native Species',
      subtitle: 'CANOPY & MEDICINAL TREES',
      desc: 'From sacred Ficus and nitrogen-fixing Bauhinia to endangered Dalbergia latifolia (Rosewood) and Triphala-yielding Terminalia bellirica.',
      icon: Leaf,
      theme: 'green',
      colSpan: 'col-span-1 md:col-span-1 lg:col-span-1',
      badge: '15 Classes',
    },
    {
      id: 'mobile',
      title: 'In-Situ Mobile Camera Ready',
      subtitle: 'FIELD AUDIT OPTIMIZED',
      desc: 'Tap and snap directly via smartphone back-camera while navigating tree trails. Built-in client validation guarantees snappy responsive uploads.',
      icon: Smartphone,
      theme: 'sage',
      colSpan: 'col-span-1 md:col-span-1 lg:col-span-1',
      badge: 'Capture API',
    },
  ];

  return (
    <section className="py-16 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-10">
          <div>
            <div className="pill-tag mb-3">SYSTEM ARCHITECTURE</div>
            <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-white tracking-tight">
              Crafted for Real-World <br />
              <span className="text-gold-leaf-gradient italic">Botanical Monitoring</span>
            </h2>
          </div>
          <p className="mt-4 md:mt-0 text-sm text-slate-300/80 max-w-md">
            A cohesive bento arrangement combining deep learning precision, urban habitat zoning, and open scientific data.
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((item, idx) => {
            const Icon = item.icon;
            let cardClass = 'bento-card';
            let iconColor = 'text-[#52B788]';
            let iconBg = 'bg-[#52B788]/15 border-[#52B788]/30';

            if (item.theme === 'terracotta') {
              cardClass = 'bento-card-terracotta';
              iconColor = 'text-[#DDA15E]';
              iconBg = 'bg-[#DDA15E]/15 border-[#DDA15E]/30';
            } else if (item.theme === 'sage') {
              cardClass = 'bento-card-sage';
              iconColor = 'text-[#B7C56A]';
              iconBg = 'bg-[#B7C56A]/15 border-[#B7C56A]/30';
            }

            return (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.08 }}
                className={`${cardClass} ${item.colSpan} p-6 sm:p-7 rounded-3xl flex flex-col justify-between relative group overflow-hidden`}
              >
                <div>
                  {/* Top Bar inside Card */}
                  <div className="flex items-center justify-between mb-6">
                    <div className={`w-12 h-12 rounded-2xl ${iconBg} border flex items-center justify-center`}>
                      <Icon className={`w-5 h-5 ${iconColor}`} />
                    </div>
                    <span className="text-[10px] font-heading font-extrabold tracking-wider uppercase px-3 py-1 rounded-full bg-white/[0.06] border border-white/[0.08] text-slate-300">
                      {item.badge}
                    </span>
                  </div>

                  <div className="font-heading font-bold text-[10px] uppercase tracking-[0.2em] text-[#7FA38A] mb-1.5">
                    {item.subtitle}
                  </div>
                  <h3 className="font-display font-bold text-xl sm:text-2xl text-white mb-3">
                    {item.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-300/80 leading-relaxed">
                    {item.desc}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-white/[0.06] flex items-center justify-between text-xs text-slate-400 group-hover:text-white transition-colors">
                  <span className="font-medium text-[11px]">Explore capability</span>
                  <ArrowUpRight className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                </div>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
