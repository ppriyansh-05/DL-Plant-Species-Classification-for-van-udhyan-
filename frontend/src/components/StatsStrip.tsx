import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Trees, Compass, Database, Cpu } from 'lucide-react';
import type { MetricsResponse, SpeciesResponse } from '../lib/api';

interface StatsStripProps {
  metrics: MetricsResponse | null;
  speciesData: SpeciesResponse | null;
}

function AnimatedNumber({ value, suffix = '' }: { value: number; suffix?: string }) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 1200; // ms
    const stepTime = 20;
    const steps = duration / stepTime;
    const increment = value / steps;

    const timer = setInterval(() => {
      start += increment;
      if (start >= value) {
        setDisplayValue(value);
        clearInterval(timer);
      } else {
        setDisplayValue(Math.floor(start));
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <span>
      {displayValue.toLocaleString()}
      {suffix}
    </span>
  );
}

export const StatsStrip: React.FC<StatsStripProps> = ({ metrics, speciesData }) => {
  const speciesCount = speciesData?.total || metrics?.num_classes || 15;
  const exp2 = metrics?.experiments?.experiment_2_top15_focused;
  const totalImages = exp2
    ? exp2.train_images + exp2.val_images + exp2.held_out_test_images + exp2.van_udyan_benchmark_images
    : 1008;

  const stats = [
    {
      id: 'species',
      icon: Trees,
      label: 'Supported Native Species',
      value: speciesCount,
      suffix: '',
      color: 'text-[#52B788]',
      accentBg: 'bg-[#52B788]/15 border-[#52B788]/30',
      description: 'Hand-curated botanical classes',
    },
    {
      id: 'zones',
      icon: Compass,
      label: 'Urban Bio-Zones',
      value: 3,
      suffix: ' Zones',
      color: 'text-[#B7C56A]',
      accentBg: 'bg-[#B7C56A]/15 border-[#B7C56A]/30',
      description: 'RSWF Pune Van Udyan grid',
    },
    {
      id: 'images',
      icon: Database,
      label: 'Curated Dataset Images',
      value: totalImages,
      suffix: '+',
      color: 'text-[#F5C542]',
      accentBg: 'bg-[#C9A227]/15 border-[#C9A227]/30',
      description: 'In-situ photos & iNaturalist CC',
    },
    {
      id: 'architecture',
      icon: Cpu,
      label: 'Vision Backbone',
      isText: true,
      textValue: 'EfficientNetB0',
      subText: '224x224 RGB • ImageNet',
      color: 'text-[#52B788]',
      accentBg: 'bg-[#52B788]/15 border-[#52B788]/30',
      description: 'Top-15 fine-tuned transfer head',
    },
  ];

  return (
    <section className="py-8 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {stats.map((item, index) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bento-card p-5 sm:p-6 rounded-3xl relative overflow-hidden group hover:-translate-y-1 transition-transform"
              >
                {/* Subtle top accent gradient */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-[#52B788]/20 to-transparent" />

                <div className="flex items-center justify-between mb-4">
                  <div className={`w-11 h-11 rounded-2xl ${item.accentBg} border flex items-center justify-center`}>
                    <Icon className={`w-5 h-5 ${item.color}`} />
                  </div>
                  <span className="text-[10px] font-heading font-bold uppercase tracking-wider text-slate-400/80">
                    Verified
                  </span>
                </div>

                <div className="font-heading font-extrabold text-2xl sm:text-3xl text-white mb-1 tracking-tight">
                  {item.isText ? item.textValue : <AnimatedNumber value={item.value!} suffix={item.suffix} />}
                </div>

                <div className="text-xs font-semibold text-slate-200 mb-1">
                  {item.label}
                </div>

                <div className="text-[11px] text-slate-400">
                  {item.isText ? item.subText : item.description}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
